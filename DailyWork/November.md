November
=========
20161124

    [x] 利用placeholder修改nodeport的为批量插入， 但是会导致MySQL注入的风险
    [ ] 跟yong.li-1，hong.guo，ming.yan讨论容器云上线方法，发现了三个问题待讨论：
        [ ] 组织和用户的对应。是用户在组织上，还是组织在用户上？是否多对多
        [ ] 取消namespace创建时的limitrange，确定pod的resource是limits还是request及对应的值
        [ ] nodeport如何管理
    [x] 给rui.chen升级yce。具体来说：
        [x] 升级镜像
        [x] 安装TunnelBlick后登VPN更新mysql。yong.li-1的TunnelBlick不好使，重新下载了新版的。湖南的mysql里datacenter的host和port有重复，为了添加唯一约束，故将其Host和port均置为0。另外发现SQL脚本里没有给datacenter的name字段增加唯一约束，所以需要检查其他的机器是否已经添加了约束。
    [x] 修改了文档中一处错误，给deployment的pod template里添加metadata的labels字段 
    [x] 尝试了GDB调试golang程序
    [x] 检查其他机器是否添加了datacenter表的name的唯一约束。均有，除了B28没权限检查。
    [ ] 给gitlab里保存的sql添加相应的sql语句

20161125
    [x] 利用placeholder修改nodeport的为批量插入和批量软删（update），需要用到mysql的insert on duplicate key update的batch
    [x] 研究每次前端更新后都需要刷新缓存的原因，但是问题没有能够复现。不确定是否解决。了解到了HTTP关于缓存控制的响应头和相关的状态码。
    [x] 学习了ElasticSearch的基本知识。它可以被看作是数据库。

20161128
    [x] 将github上最新的代码（批量插入/删除）迁回gitlab，并测试成功
    [ ] 整理MySQL注入的内容
    [ ] 重写批量插入/删除的代码，解决MySQL注入的隐患
