Kubernetes Events之捉妖记（下）
==================

经过前两回的坚持探索，一个完整的Events原形逐渐浮出水面。我们已经摸清了它的由来和身世，本回将是系列最后一篇，一起探索Events的去向。

#### 去脉知所踪

前面已经了解到，Event是由一个叫EventRecorder的东西产生的。通过研究源码发现，在Kubelet启动的时候，它会先获得一个EventBroadcaster的实例，这个实例进一步为KubeletConfig初始化一个EventRecorder。EventRecorder自不必多说，EventBroadcaster是用来接收Event并且把它们转交给EventSink、Watcher和Log。

EventBroadcaster定义了包括四个方法的一组接口，分别是：

```golang
    // 将收到的Events交于相应的处理函数
    StartEventWatcher(eventHandler func(*api.Event)) watch.Interface

    // 将收到的Events交于Sink
    StartRecordingToSink(sink EventSink) watch.Interface

    // 将收到的Events交于相应的Log供日志输出
    StartLogging(logf func(format string, args ...interface{})) watch.Interface

    // 初始化一个EventRecorder，并向EventBroadcaster发送Events
    NewRecorder(source api.EventSource) EventRecorder
```

EventBroadcaster由NewBroadcaster()方法进行初始化，它定义在kubernetes/pkg/client/record/event.go里，实际由eventBroadcasterImpl实现，调用kubernetes/pkg/watch/mux.go里的NewBroadcaster方法。每一个EventBroadcaseter都包含一列watcher，而对于每个watcher，都监视同一个长度为1000的Events Queue，由此保证分发时队列里Events跟Events发生时顺序相同。但是同一个Events发送至Watcher的顺序得不到保证。为了防止短时间内涌入的Events来不及处理，每个EventBroadcaster都拥有一个25元素长的缓冲区Incoming，定义的最后指定了队列满时的操作。

初始化并加入waitGroup之后，EventBroadcaster便进入无限循环。在这个循环中，Broadcaster会不停地从incoming队列里取走Event，获取失败就将循环退出，并清空所有的watcher。获取成功就将该event分发至各个watcher。

分发时需要加锁。在分发的时候，如果队列已满则不会阻塞，直接跳过到下一个watcher。如果队列未满，则会阻塞，直到写入后再进行下一个watcher。

在Kubelet运行过程初始化EventBroadcaster之后，如果KubeletConfig里的EventClient不为空，即指定对应的Sink接收器(EventSink是一组接口，包含存储Events的Create、Update、Patch方法，实际由对应的Client实现):

```golang
    eventBroadcaster.StartRecordingToSink(&unversionedcore.EventSinkImpl{Interface: kcfg.EventClient.Events("")})
```

StartRecordingToSink()方法先根据当前时间生成一个随机数发生器randGen，接着实例化一个EventCorrelator，最后将recordToSink()函数作为处理函数，实现了StartEventWatcher。StartLogging()类似地，将用于输出日志的匿名函数作为处理函数，实现了StartEventWatcher。


#### StartEventWatcher()

StartEventWatcher()首先实例化watcher，每个watcher都被塞入该Broadcaster的watcher列表中，并且新实例化的watcher只能获得后续的Events，不能获取整个Events历史。入列的时候加锁以保证安全。接着启动一个goroutine监视Broadcaster发来的Events。所有的Events都会被送入这个ResultChan。watcher不断从ResultChan取走每个Event，如果获取过程发送错误，将Crash并记录日志。否则在获得该Events后，交于对应的处理函数进行处理。

StartEventWatcher()方法使用recordToSink()函数作为处理。因为同一个Event可能被多个监听，所以在对Events进行处理前，先要拷贝一份备用。接着同样使用EventCorrelator对Events进行整理，然后在有限的重试次数里通过recordEvent()方法对该Event进行记录。

recordEvent()方法试着将Event写到对应的Sink里，如果写成功或被无视将返回true，如需重试则返回false。如果要写入的Event已经存在，就将它更新，否则创建一个新的Event。在这个过程中如果出错，不管是构造新的Event失败，还是服务器拒绝了这个event，都属于可无视的错误，将返回true。而HTTP传输错误，或其他不可预料的对象错误，都会返回false，并在上一层函数里进行重试。在kubernetes/pkg/client/record/event.go里指定了单个Event的最大重试次数为12次。另外，为了避免在master挂掉之后所有的Event同时重试导致不能同步，所以每次重试的间隔时间将随机产生(第一次间隔由前面的随机数发生器randGen生成)。

#### EventCorrelator

EventCorrelator定义包含了三个成员，分别是过滤Events的filterFunc，进行Event聚合的aggregator以及记录Events的logger。它负责处理收到的所有Events，并执行聚合等操作以防止大量的Events冲垮整个系统。它会过滤频繁发生的相似Events来防止系统向用户发送难以区分的信息。它会执行去重操作，以使相同的Events被压缩为单个，并增加计数。

aggregator是类型EventAggregator的一个实例，定义如下：

```golang
type EventAggregator struct {
    // 读写锁
    sync.RWMutex

    // 存放整合状态的Cache
    cache *lru.Cache

    // 用来对Events进行分组的函数、
    keyFunc EventAggregatorKeyFunc

    // 为整合的Events生成消息的函数
    messageFunc EventAggregatorMessageFunc

    // 每个时间间隔里可统计的最大Events数
    maxEvents int

    // 相同的Events间最大时间间隔以及一个时钟
    maxIntervalInSeconds int

    clock clock.Clock
}

```

EventCorrelator通过NewEventCorrelator()函数进行实例化:

```golang
func NewEventCorrelator(clock clock.Clock) *EventCorrelator {
    cacheSize := maxLruCacheEntries
    return &EventCorrelator{
        // 默认对于所有的Events均返回false，表示不可忽略
        filterFunc: DefaultEventFilterFunc,
        aggregator: NewEventAggregator(
            // 大小为4096
            cacheSize,
            // 通过相同的Event域来进行分组
            EventAggregatorByReasonFunc,
            // 生成"根据同样的原因进行分组"消息
            EventAggregatorByReasonMessageFunc,
            // 每个时间间隔里最多统计10个Events
            defaultAggregateMaxEvents,
            // 最大时间间隔为10mins
            defaultAggregateIntervalInSeconds,
            clock),
        logger: newEventLogger(cacheSize, clock),
    }
}
```

EventCorrelator的主要方法是EventCorrelate()，每次收到一个Event首先判断它是否可用被跳过(前面提过默认均不可忽略)。然后对该Event进行Aggregate处理。

EventAggregate()方法首先使用初始化时确定的分组方法EventAggregatorByReasonFunc进行分组，它按照event.Source、event.InvolvedObject、event.Type和event.Reason精确匹配并分组。这些项目拼接成的aggregateKey和event.message构成的locakKey。由aggregateRecord记录每次聚合，并作出下次聚合的决定。然后在Cache里寻找是否有满足aggregate的event，如果找到就读取它的aggregateRecord。从收到Event到到现在经过的时间如果超过了最大时间间隔，就作为新的aggretateRecord。并把刚才取得的localKey插入和把该记录放入Cache。如果该记录的数量没超过上限，就作为新的event返回。否则从取走任意一个localKey，并把创建拥有相同属性的新Event，置计数为1，表示该Event第一次出现。

接着eventObserve()记录这个Event，并根据对应EventKey在Cache里寻找最后一次见到的Event。lastEventObservationFromCache()方法返回eventLog类型的结果，它记录了该Event出现的频率。如果这个Event不是首次出现，那么需要更新它，并制作相应的补丁，最后将结果放入Cache。








