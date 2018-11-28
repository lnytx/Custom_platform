# test_ui


CMDB，先创建主机，然后自动去刷新，通过salt接口去获取主机详细信息（此处之前用得的ansible接口，后来发现在windows上无法很好的支持，）
通过wsgi定时任务查找主机上的salt_key变化并更新到数据
Salt因为是在笔记本来，导致列表变大，稍后传一张正常的图上来

我的邮箱:ln111999@163.com

yum install -y salt-master
yum install -y salt-api
yum install -y expect(git@host的交互，各个子节点都要装，本地yum源中有，可以直接安装)

pip configparser \
pip paramiko \
pip install -y pygit2 \
pip install GitPython是python库 
#pip install schedule  #定时模块 未用到
#pip install django-crontab定时运行函数 未用到 
pip install apscheduler==2.1.2 定时运行函数 
在url中定义运行定时任务
#定时任务脚本
from apscheduler.scheduler import Scheduler  
#要执行的方法  
from cmdb.cron.host_status import update_host
from cmdb.cron.host_status2 import update_host

salt-api配置
1、api.conf \
rest_cherrypy: \
  port: 9999\<br>  
  host: 172.17.39.93\
  disable_ssl: True\
2、eauth.conf\
external_auth:\
  pam:\
    saltapi:\
      - .*\
      - '@wheel'
      - '@runner'


configparser(读取配置文件)

python3.6\
bootstrap2.7(3)

CherryPy(salt-api的web服务器)
安装pip(python setup.py install)\<br>  \
安装cherrypy(pip install cherrypy)

sweetalert（1.1.3版本，提交后的弹出确认框)
http://www.bootcdn.cn/sweetalert/


bootstrap-3.3.7-dist\
bootstrap-fileinput\
上传文件插件(路径为http://127.0.0.1:8000/mult/)

bootstrap-multiselect(多项目选择插件)(需要，并且手动修了修改css，bootstrap-multiselect.css，具体请查看笔记)
开发/下拉多选框bootstrap-multiselect教程

git模块
将git命令动态写入到git_order.sls文件中的cmd.run中上传到/srv/salt中去执行
从版本管理开始就不考虑windows机器了（以后需要就再加上）
这部分功能是结合的是上家公司实际的业务实现自动化代码提交回滚

yum源那里可以自己挂载或者复制ISO里的package包到/var/www/html/centos/目录下面，该目录固定（安装httpd时产生）\
使用yum安装git时需要手动下载epel-release-7-9.noarch.rpm到/var/www/html/centos/


[先放数据库sql](https://github.com/lnytx/test_ui/blob/master/db/my_devpos.sql) \
用户登录名可以在数据库user表中查看，密码都是test123456可以自行在数据库修改 \
机器管理：手动添加机器，项目里有个update_host的定时任务，随项目启动，定时1分钟去探测机器是否在线，
![ABC](https://github.com/lnytx/test_ui/blob/master/temp/%E4%B8%BB%E6%9C%BA%E7%AE%A1%E7%90%86.png) 



![ABC](https://github.com/lnytx/test_ui/blob/master/project_images/cmdb1.png)

git项目管理，初始化git项目，之后就可以直接实现业务自动化代码提交回滚（上家公司的管理方式）
![git1](https://github.com/lnytx/test_ui/blob/master/project_images/git1.png)



![git2](https://github.com/lnytx/test_ui/blob/master/project_images/git2.png)

![git3](https://github.com/lnytx/test_ui/blob/master/project_images/git3.png)

命令执行模块：因为使用的是saltstack所以执行的参数与salt命令参数一样，只是加了个webui，便于管理
![salt-cmd1](https://github.com/lnytx/test_ui/blob/master/project_images/salt_cmd1.png)

![salt-cmd1](https://github.com/lnytx/test_ui/blob/master/temp/%E5%91%BD%E4%BB%A4%E6%89%A7%E8%A1%8C.png)


![ABC](https://github.com/lnytx/test_ui/blob/master/project_images/salt_file_modify.png)

20181128添加服务管理：
![aaa](https://github.com/lnytx/test_ui/blob/master/project_images/%E6%9C%8D%E5%8A%A1.png)


salt_minion管理模块：接受，删除或拒绝salt-minionid，里面的minionid是salt-key -L的结果
![ABC](https://github.com/lnytx/test_ui/blob/master/project_images/salt_minion_key.png)

minion_id管理
![abc](https://github.com/lnytx/test_ui/blob/master/temp/minion_id%E7%AE%A1%E7%90%86.png)

![ABC](https://github.com/lnytx/test_ui/blob/master/project_images/yum.png)

![ABC](https://github.com/lnytx/test_ui/blob/master/project_images/yum_deploy.png)

操作日志：简单记录一下，用户对本系统的各个模块的内容修改的记录，比如修改了哪个主机的什么参数
![ABC](https://github.com/lnytx/test_ui/blob/master/temp/%E6%93%8D%E4%BD%9C%E6%97%A5%E5%BF%97.png)

添加权限管理
不同的角色显示不同的按钮图标
![ABC](https://github.com/lnytx/test_ui/blob/master/project_images/view_perm.png)
![ABC](https://github.com/lnytx/test_ui/blob/master/project_images/edit_perm.png)

监控界面，使用了Highcharts-6.0.4，一次显示所有的zabbix监控的item(使用了zabbix的监控api)所以只显示了线状图
如果可以分细一些，还可以饼状图，柱状图等。
![ABC](https://github.com/lnytx/test_ui/blob/master/project_images/01.png)
![ABC](https://github.com/lnytx/test_ui/blob/master/project_images/02.png)
![ABC](https://github.com/lnytx/test_ui/blob/master/project_images/03.png)
![ABC](https://github.com/lnytx/test_ui/blob/master/project_images/04.png)
