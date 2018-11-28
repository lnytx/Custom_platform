"""test_ui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from apscheduler.scheduler import Scheduler  
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls.conf import include
from rest_framework import serializers, viewsets, routers

from cmdb import views as cmdb_views
from cmdb.cron.host_status import update_host
from data_tables import views as table
from git_manage import views as gitmanage
from login import views as login_views
from rest_api import views as api_views
from saltstack import views as saltstack
from service_manage import views as service_manage_views
from zabbix_monitor import views as zabbix_monitor_views


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')
 
 
# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
 
 
# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


#djangorestframework接口
# from django.contrib import admin
urlpatterns = [
    
    #登录，登出
    url(r'^index/$',login_views.index,name='login_index'),
    url(r'^$',login_views.index,name='login_index'),
    url(r'^login/$',login_views.login,name='login_login'),
    url(r'^index/$',login_views.login,name='login_login'),
    url(r'^login_dashboard/$',login_views.login_dashboard,name='login_dashboard'),
    url(r'^logout/$',login_views.logout,name='login_logout'),
    
    #编辑主机
    url(r'^cmdb/$', cmdb_views.cmdb,name='cmdb'),
    url(r'^cmdb/edit_host/$', cmdb_views.edit_host,name='edit_host'),
    #删除一条记录
    url(r'^cmdb/del_host/$', cmdb_views.del_host,name='del_host'),
    #新增一个主机
    url(r'^cmdb/add_host/$', cmdb_views.add_host,name='add_host'),
    #刷新数据
    url(r'^cmdb/update_host/$', cmdb_views.host_update,name='host_info'),
    url(r'^cmdb/host_info/$', cmdb_views.host_info,name='host_info'),
    #添加分组
    url(r'^cmdb/group_list/$', cmdb_views.group_list,name='group_list'),#前台显示gropu_name
    url(r'^cmdb/group_add/$', cmdb_views.group_add,name='group_add'),
    url(r'^cmdb/group_create/$', cmdb_views.group_create,name='group_create'),
    #salt_key管理
    url(r'^minion_key/$', cmdb_views.minion_key,name='minion_key'),
    #accept_minionkey接受key
    url(r'^minion_key/accept_minionkey$', cmdb_views.accept_minionkey,name='accept_minionkey'),
    #拒绝key
    url(r'^minion_key/reject_mminionkey$', cmdb_views.reject_mminionkey,name='reject_mminionkey'),
    #删除key
    url(r'^minion_key/delete_minionkey$', cmdb_views.delete_minionkey,name='delete_minionkey'),
    
    #执行命令
    url(r'^exec_cmd/$', saltstack.exec_cmd,name='exec_cmd'),
    #配置文件修改
    url(r'^exec_cmd/edit_config/$', saltstack.edit_config,name='edit_config'),
    #文件上传
    url(r'^exec_cmd/upload_files/$', saltstack.upload_files,name='upload_files'),
    #yum初始化
    url(r'^exec_cmd/yum_init/$', saltstack.yum_init,name='yum_init'),
    #yum创建
    url(r'^exec_cmd/yum_create/$', saltstack.yum_create,name='yum_create'),
    #分发yum_deploy
    url(r'^exec_cmd/yum_deploy/$', saltstack.yum_deploy,name='yum_deploy'),
    #版本管理
    url(r'^git_manage/$', gitmanage.git_man,name='git_man'),
    #host查看
    url(r'^git_manage/git_project_group_view/$', gitmanage.git_project_group_view,name='git_project_group_view'),
    #业务组初始化
    url(r'^git_manage/git_init/$', gitmanage.git_init,name='git_init'),
    #查看项目的版本
    url(r'^git_manage/view_project_version/$', gitmanage.view_project_version,name='view_project_version'),
    #查看中心库对应项目的版本
    url(r'^git_manage/view_center_version/$', gitmanage.view_center_version,name='view_center_version'),
    #git版本分发到集群中的个机器中
    url(r'^git_manage/git_deploy_version/$', gitmanage.git_deploy_version,name='git_deploy_version'),
    #根据用户名称，查找各自的日志
    url(r'^log_view/$', login_views.view_logs,name='view_logs'),
    url(r'^log_view/details/$', login_views.view_details,name='view_details'),
    url(r'^log_view/search_log/$', login_views.search_log,name='search_log'),
    #zabbix接口监控
    url(r'^zabbix_minion/$', zabbix_monitor_views.zabbix_minion,name='zabbix_minion'),
    #根据组查找主机
    url(r'^zabbix_minion/zabbix_get_host$', zabbix_monitor_views.zabbix_get_host,name='zabbix_get_host'),
    #根据主机找组
    url(r'^zabbix_minion/zabbix_get_group$', zabbix_monitor_views.zabbix_get_group,name='zabbix_get_group'),
    #根据主机找zabbix的监控项，item
    url(r'^zabbix_minion/zabbix_get_items$', zabbix_monitor_views.zabbix_get_items,name='zabbix_get_items'),
    ##获取选中的graph的数据
    url(r'^zabbix_minion/GGG/$', zabbix_monitor_views.GGG,name='GGG'),
    url(r'^zabbix_minion/zabbix_get_graph/$', zabbix_monitor_views.zabbix_get_graph,name='zabbix_get_graph'),
    
    #集群服务管理
    url(r'^service_manage/$', service_manage_views.service_manage,name='service_manage'),
#     url(r'^service_manage/host_service/$', service_manage_views.host_service_detail,name='service_manage'),
    
    #服务管理接口
    url(r'^service_api/$', service_manage_views.service_api,name='service_api'),
    
    
    #测试查看仪表盘
    url(r'^test_minion/$', zabbix_monitor_views.zabbix_minion,name='test_minion'),
    
    
    #ajax异步测试
    url(r'^cmdb/ajax_test/$', cmdb_views.ajax_test,name='ajax_test'),
    #分隔线
    url(r'^admin/', admin.site.urls),
    url(r'^test1/$', saltstack.test1),
    url(r'^test2/$', saltstack.test2),
    url(r'^deploy/$', saltstack.deploy,name='deploy'),
    url(r'^update/$', saltstack.update,name='update'),
    url(r'^routine/$', saltstack.routine,name='routine'),
    url(r'^execute/$', saltstack.execute,name='execute'),
    url(r'^uitest1/$', saltstack.uitest1,name='uitest1'),
    url(r'^uitest2/$', saltstack.uitest2,name='uitest2'),
    #url(r'^cmdb/$', saltstack.cmdb,name='cmdb'),
    url(r'^test1213/$', saltstack.test1213,name='test1213'),
    url(r'^getdata/sss/$', saltstack.liandong),
    url(r'^test3/$', saltstack.test3),
    url(r'^test4/$', saltstack.test4),
    url(r'^mult/$', saltstack.multiselect),
    #测试分页
    url(r'^pag1/$', saltstack.pag1),
    url(r'^pag2/$', saltstack.pag2),
    url(r'^delete/$', cmdb_views.group_add),
    
    
#     url(r'^add$', table.ajax_test_add),
    url(r'^table_basic/$', table.table_basic),
    url(r'^table_responsive/$', table.table_responsive),
    url(r'^table_managed/$', table.table_managed),
    url(r'^table_editable/$', table.table_editable),
    url(r'^table_advanced/$', table.table_advanced),
    url(r'^aaa/$', cmdb_views.aaa),
    url(r'^bbb/$', cmdb_views.bbb,name='bbb'),
    
    
    
    #djangorestframework接口框架
    url(r"^publishes/", api_views.PublishView.as_view()),
    url(r'^test/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    
]
#定时任务脚本
#要执行的方法  

