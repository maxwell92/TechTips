Kubernetes Events之捉妖记
==================

师出有名
--------
前些天群里有位同学提问说怎么通过API得到`kubectl describe pod`的结果，我立刻找到了Kubernetes相关的API并回复他，但他说这不是他要的东西。经过一番描述，我才了解到他想要的是原来如下图中红框里的信息：

![](kube-events.png)

Message属于Kubernetes的一种特殊的资源：Events。老实讲，我以前是没有怎么注意过这个Events是怎么来的，甚至一直觉得它应该是Pod的一部分。那么这个Events到底是什么样的资源？`kubectl`是怎么得到它的？它又该如何被API访问？下面我们一起探究Events的身世之谜。

同样都是资源，Events有什么特别？

#### 真身难觅 
熟悉Kubernetes的小伙伴应该对于它的资源比较有体会，作为调度基本单元的Pod是一种资源，控制Pod更新、扩容、数量的ReplicaSet是一种资源，作为发布单位的Deployment是一种资源，哦，还有Service，Endpoints等等。它们有这么一些共同点：

* 都可以通过`kubectl get $ResourceName`的方式获取
* 都有对应的RESTful API定义

Events亦如此，`kubectl get events`的结果为下图：

![](kubectl-get-events)

就像`kubectl get pods`一样，通过`kubectl get events`获得是当前命名空间下所有Events的列表。如果想查看某条Events的详细信息，是否也可以使用`kubectl describe events $EventsName`进行获取呢？我尝试了下，得到了下面的失败信息：

![](kubectl-describe-events-err03)

甚至连`kubectl get events $EventsName`也变得没那么好使了：

![](kubect-describe-events-err01)

另外，Events的RESTful API为下图：

![](Events-restapi)

而通过最朴素的*curl 之刃*也没能找出Events的真身：

![](curl-events-err)

这着实让人“大吃一斤”。 

#### 踏破铁鞋
那么这个Events到底是何方神圣？常规手段居然拿它没一丁点办法了？不，还有一招*json宝典*待我祭出使用。我们知道`kubectl get`一些资源的时候可以通过它的`-o json`参数得到该资源的json格式的信息描述，那么对上面的Events进行`kubectl get events -o json > /tmp/events.json`，得到了一个json数组，里面的每一条都对应着一个Events对象：

![](events-json)

Bingo!这就是我们要找的Events对应的实体json。仔细观察，图中红框里的名字正是`kubectl get events`里得到的Events名字，然而实际上它并不是真正的Events的名字。这是为何？在Kubernetes资源的数据结构定义中，一般都会包含一个`metav1.TypeMeta`和一个`ObjectMeta`成员，比如：

![](deployment-define)
![](pod-define)

`TypeMeta`里定义了该资源的类别和版本，对应我们平时写json文件或者yaml文件时的`kind: Pod`和`apiVersion: v1`。
`OjbectMeta`里定义了该资源的元信息，包括名称、命名空间、UID、创建时间、标签组等。

Events的数据结构定义里同样包含了`metav1.TypeMeta`和`ObjectMeta`，那么从前面的json图中可以确定红框里的名字并不是该Events对象的真实名字，它对应的是`InvolvedObject`的名字，而蓝框里对应的才是Events的真实名字。然后使用`kubectl get`和`curl`进行验证：

![](kubect-get-events-succ)
![](curl-events-succ)

到此，我们已经探明了Events的真名。

####





#### 火眼金睛





 





### 参考资料及说明

本文中出现的*curl 之刃*、*json宝典*、*源码大法*均属于为了轻松阅读体验而凭空捏造的词汇，分别对应*用命令行工具curl进行访问和实验*、*查看该对象的json信息*、*阅读源码寻找答案释疑*。
