December
========
20161201

    [x] 修改确定新的navList，包含个人中心的修改、nodeport管理、顺序调整，准备更新SQL脚本，更新创建用户const
    [x] 创建数据中心时自动占用32080端口,更新里也是。
    [x] 完成个人中心修改密码的调试
    [x] 完成nodeport管理功能的文档编写及调试
    [ ] 校验及错误详情的文档编写及调试

20161202

    [x] 校验及错误详情的文档编写及调试 

20161203

    [x] 公众号RESTful API Design文章整理
    [x] 校验及错误详情程序编写

20161205

    [x] 解决睿哥的问题1和4：1是不能挂载日志卷，2是datayp配额问题
    [x] 解决勇哥的问题：更新模板时生成的volumes json格式为map形式，正确的应该是数组形式。问题的原因是在导入模板的时候，缺了一行：$scope.param.deployment.spec.template.spec.volumes = [{}]; 这样在一个if语句的else里。这个if语句的含义就是如果导入的模板里有存储卷，则执行if里面的内容，否则如果没有导入模板，就执行else里的内容。缺少了的这行代码为初始化，如果没有它，就导致了保存的volumes的json变成了map。导致了最后的错误。这句话应该出现在所有涉及导入模板的地方，包括三处：appManage/deployment/controller.js，template/addTemplate/controller.js，walkthrougth/controller.js里
    [x] 应用发布的格式校验，但是请求响应时间变慢了很多（太多if语句）
    
20161206

    [x] 新的应用发布的格式校验，完成了objmeta的校验
    [x] 在b28为jinchao.ma创建只能看应用管理和集群拓扑的navList
    [x] 更新navList 172.21.1.27
    [ ] 其他校验的设计

20161207

    [x] 应用发布校验完毕
    [ ] 服务更新后台

20161208

    [x] 为k8s 1.5准备文章，研究新特性

20161209

    [x] 为更新组织配额时，如果该组织没有配额（比如原来手动创建的组织），会去创建相应的配额，否则是更新配额。
    [x] 提供更新服务的后台，目前仅支持修改端口（增加、删除、修改）
    [x] 搭建Gitlab ci，在m6 test上测试yce代码推送到打镜像成功.不知道什么test上gitlab runner访问的仓库地址是127.0.0.1，而服务在223上，所以启动了docker nginx 做了代理转发
