



import json
import uuid

from django.contrib.auth.context_processors import PermWrapper
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render, render_to_response

from pymysql_conn import select_all, select_table, update_table, insert_table, \
    delete_table, exec_add_group, exec_sql, exec_sql_args, format_args, \
    operation_record, opertion_minions
from salt_api.Mytoolkits import get_user_info
from salt_api.get_host_info import get_salt_host_details
from salt_api.salt_api_requests import get_salt_api


# Create your views here.
#服务器管理及编辑
@login_required
@permission_required('login.can_view')
def cmdb(request):
    if hasattr(request, 'user'):
        user = request.user
        print("用户",user, '-----------------------')
    else:
        from django.contrib.auth.models import AnonymousUser
        user = AnonymousUser()
        print("用户",user, '############################')
    #ip_list=select_all('host')
    username = request.session.get('session_txt')
    request.session.get('userid',None)       
    print("sssss",request.session.get('userid',None)) 
    print("username1",username)
    username=request.session
    
    print("username2",username)
    for key, value in username.items():  
        print ("key %s value %s" %(key,value))
    print("cmdbusername",username)
    group_list = select_all('host_group')
    host_sql = "select ip,minion_id,hostname,ostype,application,username,port,group_name, \
                (case when status=1 then 'Up' when status=0 then 'Down' else 'Other' end) status \
                from `host`"
    ip_list=exec_sql(host_sql)
    print("ip_list",ip_list)
    #返回到前台return render_to_response无法返回权限{{ perms }}变量但是render可以
    #return render_to_response('cmdb/host_info.html',{'ip_list':ip_list},{'group_list':group_list})
    #return render(request, 'cmdb/host_info.html', {'ip_list':ip_list,'group_list':group_list})返回两个字典要这样写，下面写的后面的group_list前台无法接收
    return render(request, 'cmdb/host_info.html', {'ip_list':ip_list},{'group_list':group_list})


#minion_key管理
def minion_key(request):
    ip_list=select_all('host')
    group_list = select_all('host_group')
    #case when语句
    minions=exec_sql("select a.ip,a.minion_id,a.group_name,(case  when a.minion_key_stat=1 then 'Accepted'  when a.minion_key_stat=2 then 'Unaccepted'  when a.minion_key_stat=3 then 'Denied' when a.minion_key_stat=4 then 'Rejected' else 'other' end) status,a.hostname \
                    from `host` a,host_group b where a.group_name=b.group_name and a.minion_key_stat!=0" )
    #minion_ids=exec_sql("select (CASE WHEN minion_key_stat='1' THEN 'a' END) aaa from `host`")
    print("minion_ids",minions)
    salt_api = get_salt_api()
    minion_ids = salt_api.get_all_keys()
    #返回到前台
    return render(request,'cmdb/salt_minion_key.html',{'minion_ids':minions})
#接收key
def accept_minionkey(request):
    if 'ip' in request.GET:
        ip=request.GET.get('ip').split(',')
        minion_key=request.GET.get('minion_key').split(',')
        salt_api = get_salt_api()
        salt_api.accept_key(minion_key)
        #更新数据库
        if salt_api.accept_key(minion_key):
            accept_key_sql = 'update `host` set minion_key_stat=1 where ip=%s and minion_id=%s'
            exec_sql_args(accept_key_sql, (ip,minion_key))
            msg={"code":1,'msg':"accept成功"}
            user_name = request.user
            ret = get_user_info(user_name)
            target_ids = str(uuid.uuid1())
            minion_id = minion_key
            operation_record(target_ids,ret['userid'],ret['user_name'],action='接收salt_key',result='True')
            opertion_minions(target_ids,minion_id,remark='接收salt_key'+minion_id)
        else:
            msg={"code":-1,'msg':"accept失败"}
        return HttpResponse(json.dumps(msg), content_type='application/json')
#拒绝key
def reject_mminionkey(request):
    if 'ip' in request.GET:
        ip=request.GET.get('ip').split(',')
        minion_key=request.GET.get('minion_key').split(',')
        salt_api = get_salt_api()
        salt_api.reject_key(minion_key)
        #更新数据库
        if salt_api.reject_key(minion_key):
            accept_key_sql = 'update `host` set minion_key_stat=4 where ip=%s and minion_id=%s'
            exec_sql_args(accept_key_sql, (ip,minion_key))
            msg={"code":1,'msg':"Rejected成功"}
            user_name = request.user
            ret = get_user_info(user_name)
            target_ids = str(uuid.uuid1())
            minion_id = minion_key
            operation_record(target_ids,ret['userid'],ret['user_name'],action='拒绝salt_key',result='True')
            opertion_minions(target_ids,minion_id,remark='拒绝salt_key'+minion_id)
        else:
            msg={"code":1,'msg':"Rejected失败"}
        return HttpResponse(json.dumps(msg), content_type='application/json')
#删除key
def delete_minionkey(request):
    if 'ip' in request.GET:
        ip=request.GET.get('ip').split(',')
        minion_key=request.GET.get('minion_key').split(',')
        salt_api = get_salt_api()
        salt_api.accept_key(minion_key)
        #更新数据库
        if salt_api.delete_key(minion_key):
            accept_key_sql = 'update `host` set minion_key_stat=0 where ip=%s and minion_id=%s'
            exec_sql_args(accept_key_sql, (ip,minion_key))
            msg={"code":1,'msg':"delete成功"}
            user_name = request.user
            ret = get_user_info(user_name)
            target_ids = str(uuid.uuid1())
            minion_id = ''.join(minion_key)
            print("minion_id的类型",type(minion_id),minion_id)
            operation_record(target_ids,ret['userid'],ret['user_name'],action='删除salt_key',result='True')
            opertion_minions(target_ids,minion_id,remark='删除salt_key'+minion_id)
        else:
            msg={"code":-1,'msg':"delete失败"}
        return HttpResponse(json.dumps(msg), content_type='application/json')
    

def aaa(request):
    ip_list=select_all('host')
    group_list = select_all('host_group')
    
    #返回到前台
    return render_to_response('cmdb/aaa.html',{'ip_list':ip_list},{'group_list':group_list})

def bbb(request):
    ip_list=select_all('host')
    group_list = select_all('host_group')
    
    #返回到前台
    return render_to_response('cmdb/bbb.html',{'ip_list':ip_list},{'group_list':group_list})

#    #add_str ip,hostname,username,application,prot,undefined,Linux,pwd
def add_host(request):
#     if hasattr(request, 'user'):
#         user = request.user
#         print("user",user)
    msg=''
    if 'add_str' in request.GET:
        col_add=request.GET.get('add_str')
        print("add_str",col_add)
        data_list = col_add.split(',')
        for i in range(len(data_list)):
            if data_list[i]=='':
                data_list[i]='undefined'
#         if(data_list[1]==''):
#             data_list[1]='undefined'
#         elif(data_list[3]==''):
#             data_list[3]='undefined'
#         elif(data_list[5]==''):
#             data_list[5]='undefined'
        data={
                'ip':data_list[0],
                'hostname':data_list[1],
                'username':data_list[2],
                'application':data_list[3],
                'ports':data_list[4],
                'group_name':data_list[5],
                'ostype':data_list[6],
                'pwd':data_list[7],
                'minion_id':data_list[8]
                }
        
        service_manage_data={
                                'ip':data_list[0],
                                'ports':data_list[4],
                                'group_name':data_list[5]
            }
        print("data",data)
        #ip,hostname,ostype,application,pwd,username,port,group_name
        if '' in data:
            print("空值")
            msg={'code':-1,'msg':'有必填值未填写，请检查'}
        a=len(exec_sql_args('select * from `host` where minion_id=%s',data['minion_id']))
        b=exec_sql_args('select * from `host` where minion_id=%s',data['minion_id'])
        if len(select_table('host', data['ip'])) != 0 and \
        len(exec_sql_args('select * from `host` where minion_id=%s',data['minion_id'])) != 0:
            msg={'code':-1,'msg':'该IP或minion_id已经存在'}
            return HttpResponse(json.dumps(msg), content_type='application/json')
        else:
            code = insert_table('host',data)
            #添加一部分数据到service_manage表，这个表与host有外键关联
            if service_manage_data:
                insert_table('service_manage',service_manage_data)
            #添加到日志表
            user_name = request.user
            ret = get_user_info(user_name)
            target_ids = str(uuid.uuid1())
            #插入日志表中，没有对应的minion_id所以目标表不用操作
            if data['ip']=='undefined':
                minion_id = data['minion_id']
            elif data['minion_id']=='undefined':
                minion_id =data['ip']
            else:
                minion_id = data['minion_id']
            operation_record(target_ids,ret['userid'],ret['user_name'],action='添加主机',result='True')
            opertion_minions(target_ids,minion_id,remark='添加主机'+minion_id)
            
            msg={'code':code,'msg':data['ip']+'已添加成功'}
    print("msg",msg)
    return HttpResponse(json.dumps(msg), content_type='application/json')
    #返回到前台

def edit_host(request):
    ip_list=select_all('host')
    print("ip_list",ip_list)
    #下面三个参数是操作记录表参数
    msg=''
    #处理host的edit
    if 'edit_str' in request.GET:
        col_edit=request.GET.get('edit_str')
        edit_result = json.loads(request.GET.get('edit_result'))#这里记录的修改前后的值
        print("edit_result",type(edit_result),edit_result)
        print("col_edit",type(col_edit),col_edit)
        data_list = col_edit.split(',')
        print("data_list",data_list)
        for i in range(len(data_list)):
            if data_list[i]=='':
                data_list[i]='undefined'
            
        data={
                'ip':data_list[0],
                'hostname':data_list[1],
                'username':data_list[2],
                'application':data_list[3],
                'ports':data_list[4],
                'group_name':data_list[5],
                'ostype':data_list[6],
                'pwd':data_list[7],
                'minion_id':data_list[8],
                'old_ip':data_list[9],
                'old_minion_id':data_list[10],
                }
        print("data[ip]",data['ip'])
        #ip,hostname,ostype,application,pwd,username,port,group_name
        if len(select_table('host', data['old_ip'])) != 0:#数据库没有原IP就更新
            ret = update_table('host',data)
            if ret[0]==-1:#等于-1说明有异常了
                print("执行有异常",type(ret),ret)
                print("ret[0]",ret[0])
                msg={"code":ret[0],'msg':ret[1]}
            else:
                msg={"code":ret[0],'msg':"修改成功"}
                #写日志
                user_name = request.user
                ret = get_user_info(user_name)
                target_ids = str(uuid.uuid1())
                operation_record(target_ids,ret['userid'],ret['user_name'],action='修改主机',result='True')
                if data['ip']=='undefined':
                    minion_id = data['minion_id']
                elif data['minion_id']=='undefined':
                    minion_id =data['ip']
                else:
                    minion_id = data['minion_id']
                for edit_before,edit_after in edit_result.items():
                    opertion_minions(target_ids,minion_id,edit_before,edit_after,remark='修改主机')
        else:
            ret = insert_table('host',data)
            msg={"code":ret,'msg':"修改成功"}
            #写日志
            
        print("msgmsgmsgmsg",msg)
    #返回到前台
    #return render_to_response('cmdb/host_info.html',locals())
    return HttpResponse(json.dumps(msg), content_type='application/json')

@login_required
@permission_required('login.can_delete')
def del_host(request):
    ip_list=select_all('host')
    print("ip_list",ip_list)
    if 'del_str' in request.GET:
        ip=request.GET.get('del_str')
        code = delete_table('host',ip)
        msg={'code':code}
        user_name = request.user
        ret = get_user_info(user_name)
        print("ret",ret)
        target_ids = str(uuid.uuid1())
        minion_id = ip
        operation_record(target_ids,ret['userid'],ret['user_name'],action='删除主机',result='True')
        opertion_minions(target_ids,minion_id,remark='删除主机')
        
    return HttpResponse(json.dumps(msg), content_type='application/json')

#查看主机的详细信息
@login_required
@permission_required('login.can_delete')
def host_info(request):
    if 'minion_id' in request.GET:
        minion_id=request.GET.get('minion_id')
        ip=request.GET.get('ip')
        print("IP",ip)
        print("minion_id",minion_id)
        disk_total_sql="select sum(total)/1024/1024 total from disk_usage where ip='%s' and minion_id='%s'" % (ip,minion_id)
        host_info = select_table('salt_host_details',ip)
        disk = exec_sql(disk_total_sql)
        print("host_info",host_info,disk)
        if len(host_info) and len(disk):#如果不为空的话
            json_str = dict(host_info[0], **disk[0])
            print(json_str)
        else:
            msg={"code":2,'msg':'没有对应的详细信息，请确保主机有效'}
            return HttpResponse(json.dumps(msg), content_type='application/json')
    return HttpResponse(json.dumps(json_str), content_type='application/json')


#根据IP刷新主机详细信息,
def host_update(request):
    #ip_list=select_all('salt_host_details')
    #print("ip_list",ip_list)
            #result[1]是磁盘信息，result[0]是主机信息,get_salt_host_details只返回了两个tuple
    disk_info=[]
    #disk是批量操作，所以insert与update所需要的参数不一样，因为是批量插入，update后面的where多了两个参数，所以参数list需要额外加上IP与minion_id
    data_disk=[]
    msg=0
    if 'minion_id' in request.GET:
        minion_id=request.GET.get('minion_id')
        ip=request.GET.get('ip')
        print("IP",ip)
        print("minion_id",minion_id)
        result = get_salt_host_details(minion_id)
        print("result",result)
        if minion_id not in result[2]:
            msg={'code':-2,'msg':'这个'+minion_id+'未定义'}
            return HttpResponse(json.dumps(msg), content_type='application/json')
#         print("result",result[2][minion_id])
        elif result[2][minion_id]:#等于False时表示salt未能连上salt-minion
            print("未能连接上去")
            for k,v in result[0].items():
                if v=='':
                    result[0][k]='undefined'
            #判断roles是否有获取到，
            if 'roles' in result[1]:
                pass
            else:
                result[0]['roles']='undefined'
            #redhad下面没有这些参数
            if 'osversion' in result[1]:
                pass
            else:
                result[0]['osversion']='undefined'
            if 'windowsdomain' in result[1]:
                pass
            else:
                result[0]['windowsdomain']='undefined'
            if 'osmanufacturer' in result[1]:
                pass
            else:
                result[0]['osmanufacturer']='undefined'
            if 'timezone' in result[1]:
                pass
            else:
                result[0]['timezone']='undefined'
            data_info = {
                    'ip':ip,
                    'minion_id':result[0]['minion_id'],
                    'kernel':result[0]['kernel'],
                    'osversion':result[0]['osversion'],
                    'cpu_model':result[0]['cpu_model'],
                    'num_cpus':result[0]['num_cpus'],
                    'manufacturer':result[0]['manufacturer'],
                    'osfullname':result[0]['osfullname'],
                    'mem_total':result[0]['mem_total'],
                    'windowsdomain':result[0]['windowsdomain'],
                    'fqdn':result[0]['fqdn'],
                    'os':result[0]['os'],
                    'cpuarch':result[0]['cpuarch'],
                    'roles':result[0]['roles'],
                    'osrelease':result[0]['osrelease'],
                    'kernelrelease':result[0]['kernelrelease'],
                    'saltversion':result[0]['saltversion'],
                    'osmanufacturer':result[0]['osmanufacturer'],
                    'saltpath':result[0]['saltpath'],
                    'timezone':result[0]['timezone'],
                    'os_family':result[0]['os_family'],
                    'shell':result[0]['shell'],
                    'username':result[0]['username'],
                    'domain':result[0]['domain']          
                    }
            print("diskdddddd",type(result[1]),result[1])
            temp={'ip':ip,'minion_id':minion_id}
            print("temp",result[1])
            for k,v in result[1].items():
                print(type(v),"key:%s,value:%s" % (k,v))
                #两个dict合并
                data_disk.append(dict(temp, **v))
            print("data_disk",data_disk)
            if len(select_table('salt_host_details', ip)) != 0:
                #不管怎样都需要更新
                code = update_table('salt_host_details',data_info)
                msg={'code':1,'msg':'更新成功'}
            else:
                code = insert_table('salt_host_details',data_info)
                msg={'code':0,'msg':'首次更新成功'}
            #更新disk_usage表
            if len(select_table('disk_usage', ip)) != 0:
                #不管怎样都需要更新
                code = update_table('disk_usage',data_disk)
                msg={'code':1,'msg':'更新成功'}
            else:
                code = insert_table('disk_usage',data_disk)
                msg={'code':0,'msg':'首次添加成功'}
            user_name = request.user
            ret = get_user_info(user_name)
            target_ids = str(uuid.uuid1())
            #插入日志表中，没有对应的minion_id所以目标表不用操作
            minion_id =minion_id
            operation_record(target_ids,ret['userid'],ret['user_name'],action='更新主机详情',result='True')
            opertion_minions(target_ids,minion_id,remark='更新主机详情')
        else:#未连接到salt-minion时
            msg={'code':-1,'msg':'未能连接到指定的minion'+minion_id}
        user_name = request.user
        ret = get_user_info(user_name)
        target_ids = str(uuid.uuid1())
        #插入日志表中，没有对应的minion_id所以目标表不用操作
        minion_id =minion_id
        result='None'
        remark='更新主机详情'
        if msg['code']==1:
            result='True'
            operation_record(target_ids,ret['userid'],ret['user_name'],action='更新主机详情',result='True')
            opertion_minions(target_ids,minion_id,remark)
        if msg['code']==-1:
            operation_record(target_ids,ret['userid'],ret['user_name'],action='更新主机详情',result='False')
            opertion_minions(target_ids,minion_id,remark='更新操作失败'+str(msg['msg']))
        return HttpResponse(json.dumps(msg), content_type='application/json')

#专门处理添加到group_name与group_id到host表里
def group_add(request):
    msg=''
    if 'ip_list' in request.GET:
        ip_list = request.GET.get('ip_list')
        group_name = request.GET.get('group_name')
        group_id = request.GET.get('group_id')
        data_list = tuple(ip_list.split(','))
        data={
                'ip':data_list,
                'group_name':group_name,
                'group_id':group_id
                }
        if(len(ip_list)==0):
            print("未选择IP")
            msg={'code':-1,'msg':'未选择IP'}
        else:
            #添加group，顺便获取code值
            code = exec_add_group(data)
            msg={'code':code,'msg':'已添加到组:'+data['group_name']}
            user_name = request.user
            ret = get_user_info(user_name)
            target_ids = str(uuid.uuid1())
            #插入日志表中，
            operation_record(target_ids,ret['userid'],ret['user_name'],action='将主机IP添加主机组',result='True')
            for minion_id in data['ip']:
                print("minion_id",minion_id)
                opertion_minions(target_ids,minion_id,remark='将主机添加'+minion_id+","+data['group_name']+'中')
            print("data",type(data),data)
    return HttpResponse(json.dumps(msg), content_type='application/json')

#前面添加组那里动态显示数据库里的group_name
def group_list(request):
    group_list = select_all('host_group')
    return HttpResponse(json.dumps(group_list), content_type='application/json')


def group_create(request):
    if 'cretat_group_str' in request.GET:
        col_create=request.GET.get('cretat_group_str')
        print("cretat_group_str",type(col_create),col_create)
        data_list = col_create.split(',')
        print("ooo",len(str(data_list[0])))
        if(len(str(data_list[1]))==0):
            data_list[1]='undefined'
        data={
                'group_name':data_list[0],
                'remark':data_list[1]
                }
        if(len(str(data_list[0]))==0):
            msg={'code':-1,'msg':'未填写组名'}
            return HttpResponse(json.dumps(msg), content_type='application/json')
        elif len(select_table('host_group', data['group_name'])) != 0:
            msg={'code':-1,'msg':'该组已经存在'}
            return HttpResponse(json.dumps(msg), content_type='application/json')
        else:
            #添加group，顺便获取code值
            code = insert_table('host_group',data)
            msg={'code':code,'msg':data['group_name']+':已添加成功'}
            user_name = request.user
            ret = get_user_info(user_name)
            target_ids = str(uuid.uuid1())
            minion_id=data['group_name']
            #插入日志表中，
            operation_record(target_ids,ret['userid'],ret['user_name'],action='创建主机组',result='True')
            opertion_minions(target_ids,minion_id,remark=msg['msg'])
            return HttpResponse(json.dumps(msg), content_type='application/json')
        
def ajax_test(request):
    msg={'code':1,'msg':'已添加成功'}
    return HttpResponse(json.dumps(msg), content_type='application/json')
