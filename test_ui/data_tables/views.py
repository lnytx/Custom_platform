import json

from django.http.response import HttpResponse
from django.shortcuts import render, render_to_response
from pymysql_conn import delete_table, select_table, \
    select_all, insert_table, update_table


# Create your views here.。。
def index(request):
    return render_to_response('index.html')


def bbb(request):
    return render_to_response('table_editable.html')



#可编辑表
#从table_editable2.html获取需要edit的数据，并传到了后台，下面就可以执行插入数据库的动作了
def table_editable(request):
    ip_list=select_all('host')
    print("ip_list",ip_list)
    if 'jsonStr' in request.GET:
        col_edit=request.GET.get('jsonStr')
        print("col_edit",col_edit)
        data_list = col_edit.split(',')
        print("data_list",data_list)
        ip = data_list[0],
        data={
                'ip':ip,
                'hostname':data_list[1],
                'ostype':data_list[2],
                'application':data_list[3],
                'username':data_list[4],
                'ports':data_list[5],
                'pwd':data_list[6],
                }
        #ip,hostname,ostype,application,pwd,username,port
        if len(select_table('host', ip)) != 0:
            update_table('host',data)
        else:
            insert_table('host',data)

    elif 'Delete_jsonStr' in request.GET:
        col_edit=request.GET.get('Delete_jsonStr')
        print("Delete_jsonStr",col_edit)
        ip = col_edit.split(',')
        delete_table('host',ip)
    #返回到前台
    return render_to_response('table_editable.html',{'ip_list':ip_list})

#高级表
def table_advanced(request):
    return render_to_response('table_advanced.html')

#可管理表

def table_managed(request):
    return render_to_response('table_managed.html')

#可响应表
def table_responsive(request):
    return render_to_response('table_responsive.html')

#基本表
def table_basic(request):
    return render_to_response('table_basic.html')