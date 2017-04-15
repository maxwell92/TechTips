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

[*Node*亲和性/反亲和性](https://kubernetes.io/docs/user-guide/node-selection/#node-affinity-beta-feature)是在*Node*上设置如何被*Scheduler*选择的规则一种方式。此功能是自*Kubernetes 1.0*版本以来在*Kubernetes*中的*nodeSelector*的功能的通用化。规则是使用在*Pod*中指定和选择器上自定义的标签等用户熟悉的概念定义的，并且他们是**必需的**或者**首选**的，这取决于你希望调度程序强制执行他们的严格程度。

#### 必需的规则(Required)
---------------------------
只有满足必需的规则的*Pod*才会被调度到特定的*Node*上。如果没有*Node*匹配条件(加上所有其他所有正常的条件，例如为*Pod*请求提供足够的可用资源），否则*Pod*不会被调度。必需满足的规则在*nodeAffinity*的`requiredDuringSchedulingIgnoredDuringExecution`字段中指定。

例如，如果我们要求在多可用区域(*Multiple Zones*)的`us-central1-a`(*GCE*)区域中的节点上进行调度，则可以将以下的关联规则指定为*Pod*规范(*Spec*)的一部分：

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
          - key: "failure-domain.beta.kubernetes.io/zone"
            operator: In
            values: ["us-central1-a"]
```

`"IgnoredDuringExecution"`意味着如果*Node*上的标签发生更改，并且亲和性的规则不再满足。这个在未来会计划实现。

`"requiredDuringSchedulingRequiredDuringExecution"`意味着一旦他们不满足节点亲和性规则，将从*Node*上驱逐不再匹配规则的*Pod*。

#### 首选的规则
----------------------

首选规则意味着如果节点与规则匹配，则将优先选择它们，并且仅当没有优选节点可用时才选择非优选节点。 您可以选择使用**首选**规则，而不是通过**必需**规则强制将*Pod*部署到我们在*GCE*的`us-central1-a`区域的节点上。选择首选规则，则需使用`preferredDuringSchedulingIgnoredDuringExecution`：

```yaml
affinity:
  nodeAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
          - key: "failure-domain.beta.kubernetes.io/zone"
            operator: In
            values: ["us-central1-a"]
```

*Node*的反亲和性能够使用负操作符(*NotIn*, *DoesNotExist*等)来表示。下面的例子说明了如何禁止您的*Pod*被调度到`us-central1-a`的区域中：

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
          - key: "failure-domain.beta.kubernetes.io/zone"
            operator: NotIn
            values: ["us-central1-a"]
```

可以使用的操作符有：*In*, *NotIn*, *Exists*, *DoesNotExist*, *Gt*, 和*Lt*。

这个特性还有一些另外的使用场景，比如需要在调度上严格区别*Node*上的**硬件架构**，**操作系统版本**，或者**专用的硬件**等。 

*Node*的亲和性和反亲和性在*Kubernetes 1.6*版本中是*Beta*版。


### 污点和容忍(*Taints and Tolerations*)
--------------------

此功能允许您标记一个*Node*(“受污染”，“有污点”），以便没有*Pod*可以被调度到此节点上，除非*Pod*明确地“容忍”污点。标记的是*Node*而不是*Pod*（如节点的亲和性和反亲和性），对于集群中大多数*Pod*应该避免调度到特定的节点上的功能特别有用，例如，您可能希望主节点（*Master*）标记为仅可调度*Kubernetes*系统组件，或将一组节点专用于特定的用户组，或者让常规的*Pod*远离具有特殊硬件的*Node*，以便为有特殊硬件需求的*Pod*留出空间。

使用`kubectl`命令可以设置节点的“污点”，例如：

```bash
kubectl taint nodes node1 key=value:NoSchedule
```

创建一个污点并标记到*Node*，那些没有设置容忍的*Pod*（通过*key-value*方式设置*NoSchedule*，这是其中一个选项）不能调度到该*Node*上。其他污点的选项是*PerferredNoSchedule*，这是*NoSchedule*首选版本；还有*NoExecute*，这个选项意味着在当*Node*被标记有污点时，该*Node*上运行的任何没有设置容忍的*Pod*都将被驱逐。容忍将被添加到*PodSpec*中，看起来像这样：

```
