# Custom_platform


业余时间，根据公司日常操作，写个有web_ui的操作界面（底层调用saltstack接口）
界面模板是一个boostrap2.7的模板经过修改而来（有些丑）

我的邮箱:ln111999@163.com

yum install -y salt-master \
yum install -y salt-api \
yum install -y expect(git@host的交互，各个子节点都要装，本地yum源中有，可以直接安装) \

pip install django \
pip install configparser \
pip install paramiko \
pip install apscheduler==2.1.2 \
pip install pymysql 

主要功能有: \
git版本集群发布管理 \
salt命令批量执行 \
一键yum源 \
简单cmdb管理 \
saltminion_key管理 \
系统日志记录 \
zabbix api接入 \
服务管理 \
系统权限管理使用的django自身权限管理

[先放数据库sql](https://github.com/lnytx/Custom_platform/blob/master/db/my_devpos.sql) \
用户登录名可以在数据库user表中查看，密码都是test123456可以自行在数据库修改 \
机器管理：手动添加机器，项目里有个update_host的定时任务，随项目启动，定时1分钟去探测机器是否在线，
![ABC](https://github.com/lnytx/Custom_platform/blob/master/temp/%E4%B8%BB%E6%9C%BA%E7%AE%A1%E7%90%86.png) 



![ABC](https://github.com/lnytx/Custom_platform/blob/master/project_images/cmdb1.png)

git项目管理，初始化git项目，之后就可以直接实现业务自动化代码提交回滚（上家公司的管理方式）
![git1](https://github.com/lnytx/Custom_platform/blob/master/project_images/git1.png)



![git2](https://github.com/lnytx/Custom_platform/blob/master/project_images/git2.png)

![git3](https://github.com/lnytx/Custom_platform/blob/master/project_images/git3.png)

命令执行模块：因为使用的是saltstack所以执行的参数与salt命令参数一样，只是加了个webui，便于管理
![salt-cmd1](https://github.com/lnytx/Custom_platform/blob/master/project_images/salt_cmd1.png)

![salt-cmd1](https://github.com/lnytx/Custom_platform/blob/master/temp/%E5%91%BD%E4%BB%A4%E6%89%A7%E8%A1%8C.png)


![ABC](https://github.com/lnytx/Custom_platform/blob/master/project_images/salt_file_modify.png)

20181128添加服务管理：
![aaa](https://github.com/lnytx/Custom_platform/blob/master/project_images/%E6%9C%8D%E5%8A%A1.png)


salt_minion管理模块：接受，删除或拒绝salt-minionid，里面的minionid是salt-key -L的结果
![ABC](https://github.com/lnytx/Custom_platform/blob/master/project_images/salt_minion_key.png)

minion_id管理
![abc](https://github.com/lnytx/Custom_platform/blob/master/temp/minion_id%E7%AE%A1%E7%90%86.png)

![ABC](https://github.com/lnytx/Custom_platform/blob/master/project_images/yum.png)

![ABC](https://github.com/lnytx/Custom_platform/blob/master/project_images/yum_deploy.png)

操作日志：简单记录一下，用户对本系统的各个模块的内容修改的记录，比如修改了哪个主机的什么参数
![ABC](https://github.com/lnytx/Custom_platform/blob/master/temp/%E6%93%8D%E4%BD%9C%E6%97%A5%E5%BF%97.png)

添加权限管理
不同的角色显示不同的按钮图标
![ABC](https://github.com/lnytx/Custom_platform/blob/master/project_images/view_perm.png)
![ABC](https://github.com/lnytx/Custom_platform/blob/master/project_images/edit_perm.png)

监控界面，使用了Highcharts-6.0.4，一次显示所有的zabbix监控的item(使用了zabbix的监控api)所以只显示了线状图
如果可以分细一些，还可以饼状图，柱状图等。
![ABC](https://github.com/lnytx/Custom_platform/blob/master/project_images/01.png)
![ABC](https://github.com/lnytx/Custom_platform/blob/master/project_images/02.png)
![ABC](https://github.com/lnytx/Custom_platform/blob/master/project_images/03.png)
![ABC](https://github.com/lnytx/Custom_platform/blob/master/project_images/04.png)
