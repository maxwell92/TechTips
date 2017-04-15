Kubernetes 1.6新特性系列 | 高级调度
===================================


> 导读：*Kubernetes 1.6*高级调度的新特性主要集中在三个方面：
>   * Node的亲和性和反亲和性(*Affinity/Anti-Affinity*)
>   * Node的污点和容忍(*Taints and Tolerations*)
>   * Pod的亲和性和反亲和性(*Affinity/Anti-Affinity*)
>   * 自定义调度

作者注：这是深入*Kubernetes 1.6*特性系列的第四篇。

*Kubernetes*的调度器在大多数情况下能过运行的很好，例如：它能够将*Pod*调度到有充足资源的*Node*上；它能够将一组*Pod*(*ReplicaSet*, *StatefulSet*,等)均匀的调度到不同的*Node*上；它尽力平衡各个节点的资源使用率等。

但有些时候你会想控制你的Pod如何调度，例如：可能你想让一些Pod被确定调度到某些使用特殊硬件的节点上，或者你想让交互频繁的服务一起调度，或者你想让一些*Node*只给特性的一些用户提供服务等等。最终，你对于应用程序调度和部署的需求永远要比*Kubernetes*提供的多。因此，*Kubernetes 1.6*提供了四个高级高级调度功能：**节点亲和性和反亲和性**，**污点和容忍**，**Pod亲和性/反亲和性**和**自定义调度**。这四个特性在*Kubernetes 1.6*版本中都是*beta*版。


### *Node*亲和性/反亲和性
---------------------------

[*Node*亲和性/反亲和性](https://kubernetes.io/docs/user-guide/node-selection/#node-affinity-beta-feature)是在*Node*上设置如何被*Scheduler*选择的规则一种方式。此功能是自*Kubernetes 1.0*版本以来在*Kubernetes*中的*nodeSelector*的功能的通用化。规则是使用在*Pod*中指定和选择器上自定义的标签等用户熟悉的概念定义的，并且他们是必须的或者首选的，这取决于你希望调度程序强制执行他们的严格程度。

只有满足必需的规则的*Pod*才会被调度到特定的*Node*上。如果没有*Node*匹配条件(加上所有其他所有正常的条件，例如为*Pod*请求提供足够的可用资源），否则*Pod*不会被调度。必需满足的规则在*nodeAffinity*的`requiredDuringSchedulingIgnoredDuringExecution`字段中指定。

例如，如果我们要求在多可用区域(*Multiple Zones)的*us-central1-GCE*区域中的节点上进行调度，则可以将以下的关联规则指定为*Pod*规范(*Spec*)的一部分：

```yaml

