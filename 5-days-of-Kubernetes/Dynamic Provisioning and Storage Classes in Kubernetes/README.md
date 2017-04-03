Dynamic Provisioning and Storage Classes in Kubernetes
======================

作者注：这是[5天深入理解Kubernetes新特性系列](http://blog.kubernetes.io/2017/03/five-days-of-kubernetes-1.6.html)的第一篇。

**存储**(*Storage*)是运行有状态容器的关键要素，*Kubernetes*提供了强大的原语来管理存储。**动态卷配置**(*Dynamic provisioning*)是*Kubernetes*的独有功能，它可以根据需要动态的创建存储卷。在动态配置之前，集群管理员必须手动调用云/存储服务提供商的接口来配置新的存储卷，然后创建*PersistentVolume*对象以在*Kubernetes*中表示和使用他们。通过动态配置，可以实现两个步骤的自动化，无须集群管理员预先配置存储资源，而是使用*StorageClass*对象制定的供应商来动态配置存储资源，具体请参考[用户指南](https://kubernetes.io/docs/user-guide/persistent-volumes/index#storageclasses)）。*StorageClass*本质上是为底层存储提供者描绘了蓝图，以及各种参数，例如磁盘类型（例如固态和标准磁盘）。

*StorageClasses*使用特定的存储平台或者云提供商为*Kubernetes*提供物理介质。多个存储配置以*in-tree*的形式（[用户手册](https://kubernetes.io/docs/user-guide/persistent-volumes/index#provisioner)），但现在也支持*out-of-tree*配置器（请参阅[*kubernetes-incubator*](https://github.com/kubernetes-incubator/external-storage)）。

在*Kubernetes 1.6*正式版中，动态配置被提升至稳定版（*Kubernetes 1.4*是*Beta*
）。这是完成*Kubernetes*存储自动化愿景的一大重要进步，它允许集群管理员控制资源的配置，也能够让用户更好地专注应用开发。这些所有的有点，在使用*Kubernetes 1.6*之前，这些面向用户的变化都是非常重要的。

### 怎么使用*Storage Classes*
---------------------------------

*StorageClass*是*Dynamic Provisioning*（动态配置）的基础，允许集群管理员位底层存储平台做定义抽象。用户只需在*PersistentVolumeClaim(PVC)*通过名字引用*StorageClass*即可。

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mypvc
  namespace: testns
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
  storageClassName: gold
```

为了促进*Dynamic Provisioning*的使用，此功能允许集群管理指定默认的*StorageClass*。当*Dynamic Provisioning*存在时，用户可以创建一个*PVC*而不需要制定一个*StorageClassName*，进一步减少了用户用于关注底层存储提供者所需的精力。当使用默认的*StorageClasses*时，创建*PersistentVolumeClaims(PV)*，这一点尤为重要：

* 在*Kubernetes 1.6*中，已经跟*PVCs*绑定的*PVs*依然保持绑定：

    * 除非用户手动添加他们，否则，他们将不具有与他们相关联的*StorageClass*。

    * 如果*PV*变为“可用”，如果删除的*PVC*和对应的*PV*被回收，则它要接受如下约束：

* 如果*PVC*中未指定*StorageClassName*，则默认的*StorageClass*将用于动态配置(*Dynamic Provisioning*)。
    
    * 如果存在并且“可用”，没有*StorageClass*标签的*PV*将不被考虑用于绑定到*PVC*。

* 如果在*PVC*中将*StorageClassName*设置为空字符串("")，则不会使用存储类。（即：此*PVC*禁止使用动态配置）

    * 如果存在并且“可用”，*PVs*（没有指定*StorageClassName*），将被考虑用于绑定到*PVC*。


* 如果*StorageClassName*设置为特定值，则将使用与之匹配的存储类。

    * 如果存在并且“可用”，匹配到*StorageClassName*的*PV*将被考虑用于绑定到*PVC*。

    * 如果不存在对应的存储类，*PVC*将失败。


为了减轻集群中默认*StorageClasses*的负担，从*Kubernetes 1.6*开始，*Kubernetes*为多个云提供商安装（通过*add-on*管理器）默认的*StorageClasses*。要使用这些默认的*StorageClasses*，用户不需要按名称引用他们，也就是说，不需要在*PVC*中指定*StorageClassName*，便可直接使用。
