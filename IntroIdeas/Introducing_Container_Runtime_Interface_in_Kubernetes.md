Introducing Container Runtime Interface(CRI) in Kubernetes
============================================================
[](http://blog.kubernetes.io/2016/12/container-runtime-interface-cri-in-kubernetes.html)

Kubernetes容器运行时接口(CRI)简介
===============================
编者注：这篇文章属于Kubernetes 1.5 新特性深度解析系列文章。

Kubernetes节点的最底层是一个负责容器启停的软件，我们把它叫做“容器运行时”。最广为人知的容器运行时就是Docker了，但并不是只有它。事实上，容器运行时这个领域发展迅速。为了使Kubernetes变得更容易扩展，我们一直在打磨Kubernetes支持容器运行时的插件API：CRI。

### 什么是CRI？为什么Kubernetes需要它？

每种容器运行时各有所长，许多用户都希望Kubernetes支持更多的运行时。在Kubernetes 1.5发布版里，我们引入了容器运行时接口（Container Runtime Interface，CRI）--一个能让kubelet无需编译就可以支持多种容器运行时的插件接口。CRI包含了一组[protocol buffers](https://developers.google.com/protocol-buffers/)，和[gRPC API](http://www.grpc.io/)，相关的[库](https://github.com/kubernetes/kubernetes/tree/release-1.5/pkg/kubelet/server/streaming)，以及正在活跃开发下的额外规范和工具。CRI目前是Alpha版本。

支持内部改变的容器运行时并不是Kubernetes中的新概念。在1.3发布版里，我们介绍了[rktnetes](http://blog.kubernetes.io/2016/07/rktnetes-brings-rkt-container-engine-to-Kubernetes.html)项目，它使得[rkt容器引擎](https://github.com/coreos/rkt)作为Docker容器运行时的一个选项。然而，不管是Docker还是Rkt都被通过内部和不稳定的接口直接集成到了kubelet的源码中了。这样的集成过程要求对kubelet内部十分熟悉，并且会在Kubernetes社区引发巨大的维护反应。通过提供一个清晰定义的抽象层，我们消除了这些障碍，开发者可以专注于构建他们的容器运行时了。这是很小的一步，但对于真正提供可插拔的容器运行时和构建一个更健康的生态系统意义非凡。

### CRI总览

通过Unix 套接字或者gRPC框架，Kubelet与容器运行时通信（或者是CRI插件填充了容器运行时），这时Kubelet就像是客户端，而CRI插件就像对应的服务器。

![](https://github.com/maxwell92/TechTips/blob/master/IntroIdeas/pics/overview-cri.png)

protocol buffers [API](https://github.com/kubernetes/kubernetes/blob/release-1.5/pkg/kubelet/api/v1alpha1/runtime/api.proto)包含了两个gRPC服务：ImageService和RuntimeService。ImageService提供了从镜像仓库拉镜像的RPC，查看，和移除镜像。RuntimeSerivce包含了管理Pods和容器生命周期的RPC，以及跟容器交互的调用(exec/attach/port-forward)。一个单块的容器运行时能够管理镜像和容器（例如：Docker和Rkt），并且通过同一个套接字同时提供这两种服务。这个套接字可以在Kubelet里通过标识--container-runtime-endpoint和--image-service-endpoint标识进行设置。

### Pod和容器生命周期管理

```go
    // Sandbox operations.
    rpc RunPodSandbox(RunPodSandboxRequest) returns (RunPodSandboxResponse) {}
    rpc StopPodSandbox(StopPodSandboxRequest) returns (StopPodSandboxResponse) {}
    rpc RemovePodSandbox(RemovePodSandboxRequest) returns (RemovePodSandboxResponse) {}
    rpc PodSandboxStatus(PodSandboxStatusRequest) returns (PodSandboxStatusResponse) {}
    rpc ListPodSandbox(ListPodSandboxRequest) returns (ListPodSandboxResponse) {}
    // Container operations.
    rpc CreateContainer(CreateContainerRequest) returns (CreateContainerResponse) {}
    rpc StartContainer(StartContainerRequest) returns (StartContainerResponse) {}
    rpc StopContainer(StopContainerRequest) returns (StopContainerResponse) {}
    rpc RemoveContainer(RemoveContainerRequest) returns (RemoveContainerResponse) {}
    rpc ListContainers(ListContainersRequest) returns (ListContainersResponse) {}
    rpc ContainerStatus(ContainerStatusRequest) returns (ContainerStatusResponse) {}
    ...
}
```

一个Pod由资源受限的隔离环境里的一组应用容器组成。在CRI，这个环境被称为PodSandbox。我们故意留下一些空间，让容器运行时根据它们内部不同的原理来产生不同的PodSandbox。对于基于hypervisor的运行时，PodSandbox可能代表的是虚拟机。对于其他的，比如Docker，它可能是Linux命名空间。这个PodSandbox一定遵循着Pod的资源定义。在v1alpha1版API里，这通过由kubelet创建和传递给运行时的pod级的cgroup限制下的一组进程来实现，

在Pod启动前，kubelet调用RuntimeService.RunPodSandbox来创建这个环境。这包括为Pod设置网络（例如：分配IP）。当PodSandbox启动后，独立的容器就可以被分别创建/启动/停止/移除。为了删除Pod，kubelet会在停止和移除所有容器前先停止和移除PodSandbox。

Kubelet负责通过RPC来进行容器生命周期的管理，测试容器生命周期钩子和健康/可读性检查，同时为Pod提供重启策略。

### 为什么需要容器中心的接口？

Kubernetes拥有对Pod资源的声明式API。我们认为一个可能的设计是为了CRI能够在它的抽象里重用这个声明式的Pod对象，给容器运行时实现和测试达到期望状态的逻辑的自由。这会极大地简化API，并让CRI可以兼容更广泛的运行时。在早期的设计阶段我们讨论过这个方法，并且由于几个原因否决了它。首先，Kubelet有许多Pod级的特性和特定的技术（比如crash-loop backoff逻辑），这会成为所有运行时重新实现时的巨大负担。其次，越来越重要的是，Pod定义快速更新。只要kubelet直接管理容器，那么许多新特性（比如init container）不需要底层容器运行时做任何改变。CRI包含了一个必要的容器级接口，这样运行时就可以共享这些特性，拥有更快的开发速度。这并不意味着我们偏离了"level triggered"哲学。kubelet负责保证实际状态到期望状态的变化。

### Exec/attach/port-forward requests

```go
service RuntimeService {
    ...
    // ExecSync runs a command in a container synchronously.
    rpc ExecSync(ExecSyncRequest) returns (ExecSyncResponse) {}
    // Exec prepares a streaming endpoint to execute a command in the container.
    rpc Exec(ExecRequest) returns (ExecResponse) {}
    // Attach prepares a streaming endpoint to attach to a running container.
    rpc Attach(AttachRequest) returns (AttachResponse) {}
    // PortForward prepares a streaming endpoint to forward ports from a PodSandbox.
    rpc PortForward(PortForwardRequest) returns (PortForwardResponse) {}
    ...
}
```

Kubernetes提供了一些特性（例如kubectl exec/attach/port-forward），用户可以与一个Pod和里面的容器进行交互。Kubelet现在通过调用容器原生的方法或使用节点上可用的工具（例如nsenter和socat）来支持这些特性。在节点上使用这些工具不是一个可移植的好办法，因为这些工具的大部分假定Pod是通过Linux命名空间进行隔离的。在CRI，我们显式定义了这些调用，允许特定的运行时实现。

另外一个潜在的问题是，kubelet如今的实现是kubelet操作所有流的连接请求。所以这会给节点的网络流量带来瓶颈。在设计CRI的时候，我们采纳了这个反馈，支持运行时防范中间人。容器运行时可以启动一个请求上的单独流服务器（甚至可能为Pod审计资源使用），并且返回服务器的地址给Kubelet。Kubelet然后将这个信息返回给Kubernetes API Server，它会打开直接与运行时提供的服务器相连的流连接，并将它跟客户端连通。

CRI还有许多方面没有被包含在这篇博文里。更多细节请参考[设计文档和建议](https://github.com/kubernetes/community/blob/master/contributors/devel/container-runtime-interface.md#design-docs-and-proposals)。

### 当前状态

尽管CRI还处于早期阶段，已经有不少使用CRI来集成容器运行时的项目在开发中。下面是一些列子：

* [cri-o](https://github.com/kubernetes-incubator/cri-o): OCI运行时
* [rktlt](https://github.com/kubernetes-incubator/rktlet): rkt容器运行时
* [frakti](https://github.com/kubernetes/frakti): 基于hypervisor的容器运行时
* [docker CRI shim](https://github.com/kubernetes/kubernetes/tree/release-1.5/pkg/kubelet/dockershim)

如果你对上面列出的这些运行时感兴趣，你可以关注这些独立的github仓库，获取最新的进展和说明。

对集成新的容器运行时感兴趣的开发者，请参考[开发指南](https://github.com/kubernetes/community/blob/master/contributors/devel/container-runtime-interface.md)了解这些API的限制和问题。我们会从早期的开发者那里积极采纳反馈来提升API。开发者可能会遇到API的一些意外改动（毕竟是Alpha版）。

### 试着集成CRI-Docker

Kubelet至今还没有默认使用CRI，但我们仍在这上面积极地推动。第一步就是使用CRI重新集成Docker到kubelet里。在1.5发布版里，我们扩展了Kubelet来支持CRI，并且为Docker添加了内置的CRI插件。这让kubelet启动一个gRPC服务器，这代表Docker。尝试新的kubelet-CRI-Docker集成，你可能会仅仅使用--feature-gates=StreamingProxyRedirects=true来打开Kubernetes API Server，来启动新的流重定向特性，并且设置kubelet的标识--experimental-cri=true来启动。

除了一些[遗失的特性](https://github.com/kubernetes/community/blob/master/contributors/devel/container-runtime-interface.md#docker-cri-integration-known-issues)，新的集成可以一直通过主要的端到端测试。我们计划尽快扩展测试的覆盖率，并且鼓励社区反应关于这个转化的任何问题。

### CRI和Minikube

如果你想要尝试新的集成，但是没有时间在云上启动一个新的测试集群。[minikube](https://github.com/kubernetes/minikube)是一个很棒的工具，你可以迅速在本地搭建集群。在你开始前，请阅读说明并下载安装minikube。

1. 检查可用的Kubernetes版本，选择可用的最新1.5.x版本。我们使用v1.5.0-beta.1作为示例。

```shell
$ minikube get-k8s-versions
```

2. 通过内建的Docker CRI集成启动一个Minikube集群。
```shell $  minikube start --kubernetes-version=v1.5.0-beta.1 --extra-config=kubelet.EnableCRI=true --network-plugin=kubenet --extra-config=kubelet.PodCIDR=10.180.1.0/24 --iso-url=http://storage.googleapis.com/minikube/iso/buildroot/minikube-v0.0.6.iso ``` 
--extra-config=kubelet.EnableCRI=true开启了kubelet的CRI实现。--network-plugin=kubenet和--extra-config=kubelet.PodCIDR=10.180.1.0/24设置Kubenet网络插件，保证分配给节点的PodCIDR。--iso-url设置本地节点启动的minikube iso镜像。

3. 检查minikube日志，查看启动CRI

```shell
$ minikube logs | grep EnableCRI
I1209 01:48:51.150789    3226 localkube.go:116] Setting EnableCRI to true on kubelet.
```

4. 创建pod，检查它的状态。你应该可以看见一个"SandboxReceived"事件，证明Kubelet在使用CRI

```shell
$ kubectl run foo --image=gcr.io/google_containers/pause-amd64:3.0
deployment "foo" created
$ kubectl describe pod foo
...
... From                Type   Reason          Message
... -----------------   -----  --------------- -----------------------------
...{default-scheduler } Normal Scheduled       Successfully assigned foo-141968229-v1op9 to minikube
...{kubelet minikube}   Normal SandboxReceived Pod sandbox received, it will be created.
...
```

注意：kubectl attach/exec/port-forward还不能在minikube的CRI中运行。但这会[在新版本的minikube中得到改善](https://github.com/kubernetes/minikube/issues/896)。 

### 社区

CRI的开发很活跃，并且被Kubernetes SIG-Node社区所维护。我们热切地期盼你的回复。加入社区吧：

* 通过[Github](https://github.com/kubernetes/kubernetes)反馈问题和特性请求
* 加入[Slack](https://kubernetes.slack.com/)上的#sig-node频道
* 参与[SIG-Node](kubernetes-sig-node@googlegroups.com)邮件列表
* 关注我们[Twitter @Kubernetesio](https://twitter.com/kubernetesio)的后续更新

作者：Yu-Ju Hong, Software Engineer, Google



























