# Kubernetes1.6的扩展性：5000node，150000pod集群
=============================================

编者按：这篇文章是关于Kubernetes 1.6新功能深入解析系列的第二篇文章。

去年夏天我们分享了关于Kubernetes扩展能力的一些更新，从那之后我们一直在努力，今天我们非常自豪地宣布：Kubernetes 1.6可处理5000个节点，150000个pod集群。而且这些集群的端到端pod启动时间比之前1.3版本2000个节点的集群更快；API调用时间延时可保持在1秒(SLO)之内。

译者注：集群支持2000个节点和API延时SLO请参考往期文章：《》。

本篇文章中我们将回顾在测试中所得到的一些指标，描述Kubernetes 1.6的性能测试结果。同时将讨论为达到系统能力更新所做的变动，和之后版本中对系统可伸缩性方面的一些计划。

### X-节点集群 - 意味着什么？
------------------------------

既然Kubernetes 1.6已发布，那现在是个很好的时间去回顾当我们说“支持”X-节点集群时到底意味着什么。在之前发布的文章中我们已有详细介绍目前有两个性能相关的服务层面指标(SLO)：

- API-响应：99%的API调用在小于1秒内返回。

- Pod启动时间：99%的pod以及他们的容器(和预拉取的镜像)在5秒内启动。

和以前一样，部署的集群超过5000节点是有可能的，有些用户也试验过，但是性能可能会下降，也许不能满足以上两个指标。

我们知道这些SLO的范围有限。在系统中的许多方面他们并不适用。比如说，我们不衡量一个服务中的新pod在启动之后能多快可以通过服务IP地址可达。如果你正考虑使用大型Kubernetes集群，并且有性能指标没包括在我们的SLO中，请联系Kubernetes Scalability SIG，可以帮助你了解目前Kubernetes是否可支持你的负载。

我们知道这些SLO的范围有限。在系统中的许多方面他们并不适用。比如说，我们不衡量一个服务中的新pod在启动之后能多快可以通过服务IP地址可达。如果你正考虑使用大型Kubernetes集群，并且有性能指标没包括在我们的SLO中，请联系Kubernetes Scalability SIG，可以帮助你了解目前Kubernetes是否可支持你的负载。

Kubernetes未来版本中与系统可伸缩性相关的最优先的事情是，通过以下方法来加强关于支持X-节点的定义：

- 改进现有的SLO

- 增加更多SLO(覆盖Kubernetes的不同领域，包括networking)

### Kubernetes 1.6既定规模的性能指标
------------------------------

Kubernetes 1.6中大规模集群的性能如何？以下图片是2000节点集群和5000节点集群中端到端pod启动时间延时。为了对比，我们也展示了相同指标在Kubernetes 1.3中结果，此结果发布在之前的系统可伸缩性文章中(支持2000节点的集群)。你可以看到，相对于2000节点的Kubernetes 1.3，2000节点和5000节点的Kubernetes 1.6 pod启动更快。

![](https://lh6.googleusercontent.com/LdjAOmsLGdxLNTo222uif1V0Eupoyaq6dY-leg1FBGkyQxUNt5ROjrFh_XzW27P7nP865FYUVwTOaUpDEnirdHSBKvh9xl8PsBNEFlVWpJUbnj0FEdLX4MywqbjwK9oc8avLRNAX)

下一个图片是5000节点的Kubernetes 1.6集群API响应延时。所有延时都小于500毫秒，甚至90%的响应都小于100毫秒。

![](https://lh6.googleusercontent.com/RFGwgw9hvRshHH11vrUxGwl-X8vXdCvyd8ETdWS9Ud5_OFpG4WctzZbCy2ad4Ao_neYaMMDz46Z2JCQUzRI1jdk6OABTFIOyvZysZpDCAfr7Ztj-EM7v25sfHxf6dOe59fncDnra)

### 我们是如何做到的？
------------------------------

过去的9个月中(自从上一篇系统可伸缩性文章发表后)，Kubernetes关于性能与扩展性的有了巨大的变化。在本篇文章中我们将着重介绍两个最大的，并简单介绍一些其它变化。

#### etcd v3
------------------------------

在Kubernetes 1.6中我们将默认存储后端(key-value存储，也是整个集群状态存储的地方)从etcd v2 转向etcd v3。最初这个转变是从1.3版本开始的。你也许会奇怪为什么这个转变花了我们这么长时间，鉴于：

- etcd的第一个支持v3 API的稳定版本于2016年6月30日宣布

- 与Kubernetes团队一起设计了新API，以支持我们的需求(从功能和可伸缩性角度)

- etcd v3与Kubernetes的整合在etcd v3宣布时就已接近完成(毕竟CoreOS使用Kubernetes作为新etcd v3 API的概念验证)

事实上，这有很多原因。我们将说明以下几个重要原因。

- 以向后不兼容的方式改变存储是一个重大的变化，从etcd v2 到 v3的迁移正是如此。因为如此我们需要有力的论证。9月份时我们找到这个证据 —— 我们确定，如果继续使用etcd v2 我们不能够扩容至5000节点的集群（kubernetes/32361 中包含一些关于它的讨论）。特别是 etcd v2中watch的执行问题。在一个5000节点的集群中，我们需要能够做到每秒至少发送500个watch事件给单个watcher，而这在etcd v2中是不可能的。

- 一旦我们有了强烈的愿望想升级至etcd v3，我们就开始了全面测试。也许你想像的到，我们遇到了一些问题。Kubernetes中有一些小的bug，同时我们也要求了etcd v3 中watch部署的性能提升（watch是etcd v2中的主要瓶颈）。这就促成了3.0.10 etcd patch的发布。

- 一旦这些变化完成之后，我们确信新的Kubernetes集群将与etcd v3一起协作。但是迁移现有集群仍是一个巨大挑战。为此我们需要将迁移过程自动化，全面测试底层CoreOS etcd 升级工具，并做出从v3 到 v2的应急回滚计划。

最终我们还是自信的说，这个变化可行。

#### 将存储数据格式转为protobuf
------------------------------

在Kubernetes 1.3 版本中，我们启用了protobufs  作为Kubernetes 组件的数据格式，用以与API server沟通 (同时保持对JSON的支持)。这对性能起了很大的提升。

然而，我们仍然使用JSON作为etcd中数据存储的格式，尽管从技术上讲我们完成可以改变它。推迟这个改变的原因与我们的etcd v3迁移计划有关。也许你正在奇怪，这个变化是如何与etcd v3迁移产生依赖的。原因是etcd v2 中我们确实不能以二进制格式存储数据(为解决它 我们另外以base64对数据进行了编码 )，而在etcd v3中我们却可以。所以为了简化etcd v3迁移，同时避免迁移中对存储于etcd中的数据的重要转换，我们决定推迟将存储数据格式转为protobufs，直至etcd v3存储后端的迁移完成。

#### 其它的一些优化
------------------------------

在过去的三个版本中，我们对Kubernetes代码库做了几十项优化，包括：

- 优化scheduler（产生5至10倍的scheduling吞吐量）

- 使用共享informers将所有controllers转至一个新型的设计模式，这降低了controller-manager对资源的消耗 — 参考文章请点击 this document

- 优化了API server中的单个操作（conversions, deep-copies, patch）

- 减少了API server中的内存分配（这对API 调用延时的影响非常大）

我们想强调的是，对过去几个版本的优化工作(贯穿整个项目的历史)，是由很多公司和来自Kubernetes社区的个人共同努力的结果。

接下来会是什么？

人们经常问在提升Kubernetes可扩展性的道路上我们会走多远。目前我们没有计划在后续的几个版本中发展节点超过5000个的集群（在SLO内）。如果你需要集群超过5000节点，我们建议使用federation 来聚合多个Kubernetes集群。

然而，这并不意味着我们将停止对可扩展性和性能的工作。在本文开始时我们提到过，我们最优先的事情是改进现有的两个SLO以及引进新的能够覆盖更多领域的指标，比如networking。这项工作已经在Scalability SIG开始进行了。关于该如何定义性能SLO，我们已取得了很大进展。下个月这项工作应该可以结束。


#### 加入我们
------------------------------

如果你对可扩展性和性能感兴趣，请加入我们的社区，帮助我们共同打造Kubernetes，你可以：

- 在Kubernetes Slack scalability channel 中与我们讨论

- 加入我们的特别兴趣小组， SIG-Scalability, 每周四9:00 AM PST聚会

感谢支持与贡献！阅读更多关于Kubernetes 1.6新特性的深度文章 请点击here.
