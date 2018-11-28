import json

from django.contrib.auth.decorators import login_required, permission_required
from django.http.response import HttpResponse
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from pymysql_conn import select_all, exec_sql, select_table, exec_sql_args


# Create your views here.
@login_required
@permission_required('login.can_view')
def service_manage(request):
    ip_list=''
    ip=''
    if 'ip' in request.GET:
        ip=request.GET.get('ip')
        print("ip是",type(ip),ip)
        ip_list=exec_sql_args('select * from `service_manage` where ip=%s',ip)
    else:#显示全部
       ip_list=exec_sql('select * from `service_manage`') 
    return render(request, 'service_manage/service_manage.html',{'ip_list':ip_list})

def service_api(request):#rest_framework接口
    '''
            前台调用http://127.0.0.1:8000/service_api/?action=stop&service_name=httpd
    '''
    action=''
    service_name=''
    if 'action' in request.GET:
        action=request.GET.get('action')
    if 'service_name' in request.GET:
        service_name=request.GET.get('service_name')
    msg={'action':action+':'+service_name,'msg':'成功'}
    retsj = json.dumps(msg)
    return HttpResponse(retsj)


    
