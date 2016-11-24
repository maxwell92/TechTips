November
=========
20161124

    [ ] 利用placeholder修改nodeport的为批量插入
    [ ] 跟yong.li-1，hong.guo，ming.yan讨论容器云上线方法，发现了三个问题待讨论：
        [ ] 组织和用户的对应。是用户在组织上，还是组织在用户上？是否多对多
        [ ] 取消namespace创建时的limitrange，确定pod的resource是limits还是request及对应的值
        [ ] nodeport如何管理
    [ ] 给rui.chen升级yce。具体来说：
        [x] 升级镜像
        [ ] 安装TunnelBlick后登VPN更新mysql。
    [x] 修改了文档中一处错误，给deployment的pod template里添加metadata的labels字段 
