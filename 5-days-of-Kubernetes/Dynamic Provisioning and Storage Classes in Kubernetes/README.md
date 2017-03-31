Dynamic Provisioning and Storage Classes in Kubernetes
======================

作者注：这是[5天深入理解Kubernetes新特性系列](http://blog.kubernetes.io/2017/03/five-days-of-kubernetes-1.6.html)的第一篇。

**存储**(*Storage*)是运行有状态容器的关键要素，*Kubernetes*提供了强大的原语来管理存储。**动态卷配置**(*Dynamic provisioning*)是*Kubernetes*的独有功能，它可以根据需要动态的创建存储卷。在动态配置之前，集群管理员必须手动调用云/存储服务提供商的接口来配置新的存储卷，然后创建*PersistentVolume*对象以在*Kubernetes*中表示和使用他们。通过动态配置，可以实现两个步骤的自动化，无须集群管理员预先配置存储资源，而是使用*StorageClass*对象制定的供应商来动态配置存储资源，具体请参考[用户指南](https://kubernetes.io/docs/user-guide/persistent-volumes/index#storageclasses)）。*StorageClass*本质上是为底层存储提供者描绘了蓝图，以及各种参数，例如磁盘类型（例如固态和标准磁盘）。

*StorageClasses*使用特定的存储平台或者云提供商为*Kubernetes*提供物理介质。多个存储配置以*in-tree*的形式



