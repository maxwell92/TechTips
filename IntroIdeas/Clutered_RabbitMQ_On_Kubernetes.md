Clustered RabbitMQ on Kubernetes
===============================

在Kubernetes上搭建RabbitMQ有很多方法。今天将为大家分享我们在Fuel CCP项目上集群化RabbitMQ时踩过的那些坑。这些坑大部分都很常见，如果你想提出你的解决方案，你应该可以从本文中获得灵感。

### 命名你的兔子
在Kubernetes上运行RabbitMQ带来一系列有趣的问题。首要的问题就是我们该如何给兔子命名，好让它们能相互发现？下面是一些可以参考的命名例子：

* rabbit@hostname
* rabbit@hostname.domainname
* rabbit@172.17.0.4

在你试图启动任何兔子之前，你应该确保容器间可以使用命名相互连通。例如，可以ping通@后面的内容。

Erlang发布版（常被RabbitMQ使用）可以运行在两种命名模式里：短名称或长名称。最好是当它包含"."时采用长名称，否则是短名称。对于上面的命名示例，第一个是短名称，而第二个和第三个都是长名称。

看看我们在Kubernetes上是怎么命名nodes的：

* 使用PetSet（现在也叫做StatlefulSets）让我们可以使用稳定的DNS命名。与常见的如果不健康就会被丢弃的“不可分解”副本相反，PetSet是一组有状态的pods，拥有强标记。
* 使用IP地址和一些自动化对端发现（例如autocluster plugin），它可以以一种可发现的方法自动集群化RabbitMQ。

这些选项都需要运行在长名称模式下。但是运行前要注意：在Kubernetes Pod里配置的DNS/hostname与RabbitMQ 3.6.6之前的版本是不兼容的。

### Erlang cookie
集群化成功的第二要素是RabbitMQ节点需要拥有共享的secret cookie。默认情况下，RabbitMQ从一个文件里读取这个cookie（如果没有这个文件则会生成）。为了保证在所有节点上这个Cookie的一致，我们采用的办法是：

* 在打Docker 镜像的时候就创建cookie文件。但不推荐这么做，因为拿到cookie就意味着获得了进入RabbitMQ内部的所有权限。
* 在entrypoint脚本里创建文件。将secret作为环境变量，如果我们还需要entrypoint脚本，这是一个次好的办法。
* 通过环境变量向Rabbit MQ传入更多的选项。比如：RABBITMQ_CTL_ERL_ARGS="-setcookie <our-cookie>"，RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS="-setcookie <our-cookie>"  

### 集群须知
关于RabbitMQ集群我们还需要知道的一点是：当一个节点加入集群时，不管怎样它的数据都会丢失。通常这无所谓，当

### 原文链接
[Clustered RabbitMQ on Kubernetes](https://www.mirantis.com/blog/clustered-rabbitmq-kubernetes/?utm_content=buffer1fa9c&utm_medium=social&utm_source=twitter.com&utm_campaign=buffer)
[Alexey Lebedev]()
