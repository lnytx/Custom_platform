from datetime import date
import datetime  
import json
from multiprocessing import Pool
import os
import re
import uuid

from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponse
from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.template.context_processors import request

from pymysql_conn import select_table, select_all, update_table, insert_table, \
    delete_table, exec_sql, format_args, exec_sql_args, operation_record, \
    opertion_minions
from salt_api.Mytoolkits import format_result, ssh_connect_command, read_config, \
    replace_dict_value, get_user_info
from salt_api.salt_api_requests import get_salt_api, format_minionIDs
from templates.test.fenye.feye import Pagination


@login_required
@permission_required('login.can_view')
def exec_cmd(request):
    dcen_list=['dcen_list1','dcen_list2','dcen_list3','dcen_list4']
    msg={}
    ips=[]#存储没有定义的host的IP，如果有则不执行命令，直接返回
    host_win=[]#分别存储不同类型的机器
    host_linux=[]
    minion_id=[]
    #根据前台的group_name返回host信息
    if request.is_ajax(): 
        if 'group_name' in request.GET:
            group_name = request.GET.get('group_name')
            select_sql = "select ip from `host` where group_name='%s'" % group_name
            result = exec_sql(select_sql)
            print("result",type(result),result)
            return HttpResponse(json.dumps(result), content_type='application/json')
        if 'host_list' in request.GET:
            #获取前端传过来的group_list，order以及参数数据
            host_list = request.GET.get("host_list").split(',')
            order = request.GET.get("order")
#             args_linux = request.GET.get("args_linux")
#             args_win = request.GET.get("args_win")
#             print("win参数",args_win)
#             print("linux参数",args_linux)
            #根据IP查找对应的minion_id，如果没有则此次命令执行失败，返回并提示有IP未填写minon_id
            sql_minion_id="select ip,minion_id,ostype from `host` where ip in "+format_args(host_list)
            minion_id = exec_sql_args(sql_minion_id,host_list)
            print("minion_id",type(minion_id),minion_id)
            for i in minion_id:
                if(('undefined'==i['minion_id']) or(''==i['minion_id'])):
                    ips.append(i['ip'])
                    print("ips",ips)
                    msg={"code":-1,"msg":'有主机未定义minion_id:'+str(ips)}
                    return HttpResponse(json.dumps(msg), content_type='application/json')#有这种情况马上退出
                
                        #return HttpResponse(json.dumps({"code":-1,'msg':"参数分隔错误，请使用','"}), content_type='application/json')
        if 'order' in request.GET:
            order = request.GET.get("order")
            print("order",type(order),order)
            args_linux = request.GET.get("args_linux")
            args_win = request.GET.get("args_win")
            args_w=[]
            args_lin=[]
#             print("win参数",type(args_win),args_win)
#             print("linux参数",type(args_linux),args_linux)
            for i in minion_id:
                #处理windows机器
                if ('Windows' in i['ostype']):
                    host_win.append(i['minion_id'])
                    print("host_win",host_win)
                    print("len(args_win)",len(args_win))
                    if str(args_win).find(',')==-1:#=-1说明没找到逗号
                        #使用list装参数，方便后面判断有几个参数
                        args_win=args_win#如果有windows机器的话这里的args_win以及args_w才有值，否则是没有值的
                        print("args_win",type(args_win),args_win)
                    else:
                        args_w = args_win.split(',')
                        print("args_w",type(args_w),args_w)
                        if(len(args_w)>2):
                            return HttpResponse(json.dumps({"code":1,"msg":"参数大于2个"}), content_type='application/json')
                            
                #处理其他类型机器
                else:
                    host_linux.append(i['minion_id'])
                    print("host_linux",host_linux)
                    if str(args_linux).find(',')==-1:#=-1说明没找到逗号
                        #使用list装参数，方便后面判断有几个参数
                        args_linux=args_linux
                        print("args_linux",args_linux)
                    else:
                        args_lin = args_linux.split(',')
                        print("args_linux2",type(args_lin),args_lin)
                        if(len(args_lin)>2):
                            return HttpResponse(json.dumps({"code":1,"msg":"参数大于2个"}), content_type='application/json')
            salt_api = get_salt_api()
            result_scuess={}
            result_failed={}
            temp={}
            print("len(args_win)",len(args_win),len(args_w))
            print("len(args_linux)",len(args_linux),len(args_lin))
            #获取所有的minions与前台传来的值进行比较，若前台传值有不符的则不执行
            minions = salt_api.get_all_keys()
            ret={}
            print("minions",minions)
            minion_pre={x['ip']:x['minion_id'] for x in minion_id}
            print("minion_pre",minion_pre)
            if(set(minion_pre.values())-set(minions['minions'])):#集合相减,有值则为真,说明有master端未包含的minion_id,则需要检查，无值则为假
                print("true",set(set(minion_pre.values())-set(minions)))
                #以防万一，这里还是加一手先去接收这些key值。
                for k,v1 in minion_pre.items():
                    for v2 in set(minion_pre.values())-set(minions):
                        if v2==v1:
                            ret[k]=v2
                print("ret",ret)
                #有值说明在salt-master端还没有添加进去，如果是自动添加的话，则去找客户机原因，有这种情况马上退出
                msg={"code":-2,"msg":str(ret)+":直接退出执行，因为salt-master没有接接收到这些minion_id,服务端是自动接收key的，所以请检查客户机服务"}
                print("dict(msg,**ret)",dict(msg,**ret))
                #有这种情况马上退出
                return HttpResponse(json.dumps(dict(msg,**ret)), content_type='application/json')
            else:
                print("false",set(minion_pre)-set(minions))
            #如果前台IP对应的minion_id全部存在于salt-master中则继续执行下面的代码,循环执行minion_id
                min_ids=[x['minion_id'] for x in minion_id]
                print("min_ids",min_ids)
            #没有参数时执行
                if len(args_win)==0 and len(args_linux)==0:
                    print("len(args_win)",len(args_win))
                    print("len(args_linux)",len(args_linux))
                #执行命令，此外也可以直接塞list,set去执行的
                    print("order",order)
                    print("min_ids",min_ids)
                    result = salt_api.salt_command(format_minionIDs(min_ids),order)
                    print("0args_result",result)
                    #处理两个参数的情况
                elif len(args_w)>0 or len(args_lin)>0:
                    if len(args_lin)>0 and len(args_w)<=0:
                        result = salt_api.salt_command_two_args(format_minionIDs(host_linux),order,args_lin[0],args_lin[1])
                    elif len(args_w)>0 and len(args_lin)<=0:
                        result = salt_api.salt_command_two_args(format_minionIDs(host_win),order,args_w[0],args_w[1])
                    elif len(args_w)>0 and len(args_lin)>0:
                        result1 = salt_api.salt_command_two_args(format_minionIDs(host_win),order,args_w[0],args_w[1])
                        print("result1",type(result1),result1)
                        result2 = salt_api.salt_command_two_args(format_minionIDs(host_linux),order,args_lin[0],args_lin[1])
                        print("result2",type(result2),result2)
                        ret = result1+result2
                        print("ret",type(ret),ret)
                        result = format_result(ret)
                        print("两个参数的result",result)
                #处理其他情况个参数
                else: 
                    if len(args_linux)>0 and len(args_win)<=0:
                        result = salt_api.salt_command(format_minionIDs(host_linux),order,args_linux)
                        print("args_linux个参数的result",result)
                    if len(args_win)>0 and len(args_linux)<=0:
                        result = salt_api.salt_command(format_minionIDs(host_win),order,args_win)
                        print("args_win个参数的result",result)
                    elif len(args_win)>0 and len(args_linux)>0:
                        result1 = salt_api.salt_command(format_minionIDs(host_win),order,args_win) 
                        result2 = salt_api.salt_command(format_minionIDs(host_linux),order,args_linux)
                        result = dict(result1,**result2)
                        print("1个参数的result",result)
                    print("执行结果",result)
     #根据error_list找出结果result的key值出现在error_list里的dict,标记为result_failed
     #定义错误列表，根据关键字确定是否执行成功
                error_list=['False','error','No minions matched','No command was sent','incorrect','[]',
                            'no jid was assigned','issue any command','is not recognized',
                            'Usage:','ERROR: Specified cwd','is not available','salt: error:','Minion did not return',
                            'Passed invalid arguments','caused an exception','contains no section headers','Connection refused','Error: Package:','Error'
                            ]
                print("zzz",result)
                result=format_result(result)
                for k1,v1 in result.items():
                    for v2 in error_list:
                        #判断error_list中的串是否在result_list串中出现
                        #grains.items成功的命令中有出现:False，需要将这种情况
                        if str(v1).find(v2)==-1:#等于-1说明没找到
                            pass
                        else:
                            #先将找到了的找出，找到了就说明是有问题的
                            result_failed[k1]=v1
                print("result_failed",result_failed)
                temp1=[]#获取所有的minion_id
                temp2=[]#获取失败的minion_id
                #使用set取result差集，排除掉result_failed，那么剩下的就是result_scuess
                for k2,v2 in result.items():
                    temp1.append(k2)
                for k3,v3 in result_failed.items():
                    temp2.append(k3)
                    result_failed[k3]=v3
                s= set(temp1)-set(temp2)#这里就是剩下的执行成功的minion_id
                for k,v in result.items():#通过比较原始的执行结果的value是否与执行成功的minion_id相等，如果相等则加进result_scuess
                    for i in list(set(temp1)-set(temp2)):
                        if i==k:
                            result_scuess[i]=v
                #给执行失败的结果添加一个标识，以供前台区分
                for k, v in result_failed.items():
                    result_failed[k]='ERROR:'+str(v)
                print("result",result)
                #写入日志
                user_name = request.user
                ret = get_user_info(user_name)
                args= str(args_linux+'或者'+args_win)#记录参数
                #记录成功的命令
                for k,v in result_scuess.items():
                    target_ids = str(uuid.uuid1())
                    operation_record(target_ids,ret['userid'],ret['user_name'],action=k+'执行salt命令:'+order,result='True')
                    opertion_minions(target_ids,k,remark='执行salt命令:'+order+"参数"+args)
                #记录失败的命令
                for k,v in result_failed.items():
                    target_ids = str(uuid.uuid1())
                    operation_record(target_ids,ret['userid'],ret['user_name'],action=k+'执行salt命令:'+order+"参数"+args,result='False')
                    opertion_minions(target_ids,k,remark='执行salt命令:'+order+"参数"+args)
                
                if result:
                    msg={"code":0,"msg":str(order)+"命令执行成功"}
                    result=dict(msg,**dict(result_scuess,**result_failed))
                    return HttpResponse(json.dumps(result), content_type='application/json')
                else:
                    return HttpResponse(json.dumps({"code":-1,"msg":"result为空，执行失败，请看日志"}), content_type='application/json')
    return  render(request,'salt_api/exec_cmd.html',{'dcen_list':dcen_list} )

#修改配置文件
def edit_config(request):
    host_win=[]
    host_linux=[]
    msg_faild={}#失败消息
    msg_success={}
    if request.is_ajax(): 
        edit_config_linux=''
        edit_config_win=''
        edit_config_pre=''
        edit_config_last=''
        if 'ips' in request.GET:  
            ips = request.GET.get("ips").split(',')
            edit_config_win = request.GET.get("edit_config_win")
            print("edit_config_win",edit_config_win)
            edit_config_linux = request.GET.get("edit_config_linux")
            edit_config_pre = request.GET.get("edit_config_pre")
            edit_config_last = request.GET.get("edit_config_last")#前端验证，必定有值
            sql_minion_id="select ip,minion_id,ostype from `host` where ip in "+format_args(ips)
            minion_id = exec_sql_args(sql_minion_id,ips)
            print("minion_id",type(minion_id),minion_id)
        if  len(edit_config_win)>0 and len(edit_config_linux)<=0:
            #记录成功的命令的 一些参数
            user_name = request.user
            ret = get_user_info(user_name)
            edit_config_win= edit_config_win#记录文件位置参数
            edit_before = edit_config_pre
            edit_after = edit_config_last
               #只处理win机器
            for i in minion_id:
                if('windows'==i['ostype']):
                #添加win主机
                   host_win.append(i['minion_id'])
                   #执行修改命令
            salt_api = get_salt_api()
            print("host_win",host_win)
            file_exists = salt_api.salt_command(format_minionIDs(host_win),'file.file_exists',edit_config_win)
            #如果全为真则执行，否则提示有机器没有该文件
            print("file_exists",file_exists)
            for k,v in file_exists.items():
                if 'False' == str(v):
                    msg_faild[k]='ERROR:'+str(v)
                    print("msg_faild",msg_faild)
            if len(msg_faild)>0:
                msg={"code":-1,"msg":'有服务器中该文件不存在,请检查'+str(msg_faild),'status':'error'}
                print("dict(msg,**msg_faild)",dict(msg,**msg_faild))
                return HttpResponse(json.dumps(dict(msg,**msg_faild)), content_type='application/json')
            else:
                for k,v in file_exists.items():
                    msg_success[k]=str(v)
                    print("msg_success",msg_success) 
                msg={"code":-1,"msg":'请看右侧的预览信息，点击提交会修改','status':'success'}  
                if 'preview' in request.GET:#生成预览信息
                    preview=request.GET.get("preview")
                    print("preview",preview)
                    msg_success={}
                    for i in host_win:
                        print("i",i)
                        cmd="salt %s file.replace %s pattern=%s repl=%s  backup='.bak'  dry_run='True'" %(i,edit_config_win,edit_config_pre,edit_config_last)
                        print("cmd",cmd)
                        msg_success[i]=ssh_connect_command(cmd)
                    return HttpResponse(json.dumps(dict(msg_success,**msg)), content_type='application/json')
                #return HttpResponse(json.dumps(dict(msg,**msg_success)), content_type='application/json')
                print(dict(msg,**msg_success))
                #执行替换命令
            if edit_config_pre=='追加':
                print("edit_config_pre",edit_config_pre)
                 #第一个参数为追加时则追加
                msg={"code":-1,"msg":'配置添加到了文件末尾'+str(host_win),'status':'success'}
                
                for i in host_win:
                    print("i",i)
                    cmd="salt %s file.replace %s pattern=%s repl=%s  backup='.bak'  append_if_not_found='True'" %(i,edit_config_win,edit_config_pre,edit_config_last)
                    print("cmd",cmd)
                    msg_success[i]=ssh_connect_command(cmd)
                    
                    #入到日志表
                    target_ids = str(uuid.uuid1())
                    operation_record(target_ids,ret['userid'],ret['user_name'],action=i+'执行命令:'+cmd,result='True')
                    opertion_minions(target_ids,i,edit_before,edit_after,remark='文件位置为:'+edit_config_win)
                return HttpResponse(json.dumps(dict(msg_success,**msg)), content_type='application/json')
                
            else:
                #执行替换
                msg={"code":-1,"msg":'配置已修改完成'+str(host_win),'status':'success'}
                for i in host_win:
                    print("i",i)
                    cmd="salt %s file.replace %s pattern=%s repl=%s  backup='.bak'" %(i,edit_config_win,edit_config_pre,edit_config_last)
                    print("cmd",cmd)
                    msg_success[i]=ssh_connect_command(cmd)
                    target_ids = str(uuid.uuid1())
                    operation_record(target_ids,ret['userid'],ret['user_name'],action=i+'执行命令:'+cmd,result='True')
                    opertion_minions(target_ids,i,edit_before,edit_after,remark='文件位置为:'+edit_config_win)
                return HttpResponse(json.dumps(dict(msg_success,**msg)), content_type='application/json')
                    
                    
                      
                
                           
                       #先查看是否有该行
                       #salt '*' file.contains / etc / crontab'mymaintenance.sh'
                       #salt '*' file.file_exists / etc / passwd 查看文件是否有效
                       #salt.modules.file.get_diff返回主文件上的文件统一比较
               
        if  len(edit_config_linux)>0 and len(edit_config_win)<=0:
               #只处理linux机器
            #记录成功的命令的 一些参数
            user_name = request.user
            ret = get_user_info(user_name)
            edit_config_linux= edit_config_linux#记录文件位置参数
            edit_before = edit_config_pre
            edit_after = edit_config_last
            salt_api = get_salt_api()
            for i in minion_id:
                if('windows'!=i['ostype']):
                #添加win主机
                   host_linux.append(i['minion_id'])
                   #执行修改命令
            print("host_linux",host_linux)
            file_exists = salt_api.salt_command(format_minionIDs(host_linux),'file.file_exists',edit_config_linux)
            #如果全为真则执行，否则提示有机器没有该文件
            print("file_exists",file_exists)
            for k,v in file_exists.items():
                if 'False' == str(v):
                    msg_faild[k]='ERROR:'+str(v)
                    print("msg_faild",msg_faild)
            if len(msg_faild)>0:
                msg={"code":-1,"msg":'有服务器中该文件不存在,请检查'+str(msg_faild),'status':'error'}
                print("dict(msg,**msg_faild)",dict(msg,**msg_faild))
                return HttpResponse(json.dumps(dict(msg,**msg_faild)), content_type='application/json')
            else:
                for k,v in file_exists.items():
                    msg_success[k]=str(v)
                    print("msg_success",msg_success) 
                msg={"code":-1,"msg":'请看右侧的预览信息，点击提交会修改','status':'success'}  
                if 'preview' in request.GET:#生成预览信息
                    preview=request.GET.get("preview")
                    print("preview",preview)
                    msg_success={}
                    for i in host_linux:
                        print("i",i)
                        cmd="salt %s file.replace %s pattern=%s repl=%s  backup='.bak'  dry_run='True'" %(i,edit_config_linux,edit_config_pre,edit_config_last)
                        print("cmd",cmd)
                        msg_success[i]=ssh_connect_command(cmd)
                    return HttpResponse(json.dumps(dict(msg_success,**msg)), content_type='application/json')
                #return HttpResponse(json.dumps(dict(msg,**msg_success)), content_type='application/json')
                print(dict(msg,**msg_success))
                #执行替换命令
            if edit_config_pre=='追加':
                print("edit_config_pre",edit_config_pre)
                 #第一个参数为追加时则追加
                msg={"code":-1,"msg":'配置添加到了文件末尾'+str(host_linux),'status':'success'}
                for i in host_linux:
                    print("i",i)
                    cmd="salt %s file.replace %s pattern=%s repl=%s  backup='.bak'  append_if_not_found='True'" %(i,edit_config_linux,edit_config_pre,edit_config_last)
                    print("cmd",cmd)
                    msg_success[i]=ssh_connect_command(cmd)
                    target_ids = str(uuid.uuid1())
                    operation_record(target_ids,ret['userid'],ret['user_name'],action=i+'执行命令:'+cmd,result='True')
                    opertion_minions(target_ids,i,edit_before,edit_after,remark='文件位置为:'+edit_config_linux)
                return HttpResponse(json.dumps(dict(msg_success,**msg)), content_type='application/json')
                
            else:
                #执行替换
                msg={"code":-1,"msg":'配置已修改完成'+str(host_linux),'status':'success'}
                for i in host_linux:
                    print("i",i)
                    cmd="salt %s file.replace %s pattern=%s repl=%s  backup='.bak'" %(i,edit_config_linux,edit_config_pre,edit_config_last)
                    print("cmd",cmd)
                    msg_success[i]=ssh_connect_command(cmd)
                    target_ids = str(uuid.uuid1())
                    operation_record(target_ids,ret['userid'],ret['user_name'],action=i+'执行命令:'+cmd,result='True')
                    opertion_minions(target_ids,i,edit_before,edit_after,remark='文件位置为:'+edit_config_linux)
                return HttpResponse(json.dumps(dict(msg_success,**msg)), content_type='application/json')
        else:
            #都处理
            user_name = request.user
            ret = get_user_info(user_name)
            edit_config_linux= edit_config_linux#记录文件位置参数
            edit_config_win= edit_config_win#记录文件位置参数
            edit_before = edit_config_pre
            edit_after = edit_config_last
            salt_api = get_salt_api()
            for i in minion_id:
                if('windows'==i['ostype']):
                #添加win主机
                    host_win.append(i['minion_id'])
                else:
                    host_linux.append(i['minion_id'])
            print("host_win",host_win)
            print("host_linux",host_linux)
            file_exists_win = salt_api.salt_command(format_minionIDs(host_win),'file.file_exists',edit_config_win)
            file_exists_linux = salt_api.salt_command(format_minionIDs(host_linux),'file.file_exists',edit_config_linux)
            #合并执行结果
            file_exists=dict(file_exists_win,**file_exists_linux)
            #如果全为真则执行，否则提示有机器没有该文件
            print("file_exists_all",file_exists)
            for k,v in file_exists.items():
                if 'False' == str(v):
                    msg_faild[k]='ERROR:'+str(v)
                    print("msg_faild",msg_faild)
            if len(msg_faild)>0:
                msg={"code":-1,"msg":'有服务器中该文件不存在,请检查'+str(msg_faild),'status':'error'}
                print("dict(msg,**msg_faild)",dict(msg,**msg_faild))
                return HttpResponse(json.dumps(dict(msg,**msg_faild)), content_type='application/json')
            else:
                for k,v in file_exists.items():
                    msg_success[k]=str(v)
                    print("msg_success",msg_success) 
                msg={"code":-1,"msg":'请看右侧的预览信息，点击提交会修改','status':'success'}  
                if 'preview' in request.GET:#生成预览信息
                    preview=request.GET.get("preview")
                    print("preview",preview)
                    msg_success_linux={}
                    msg_success_win={}
                    msg_success={}
                    for i in host_linux:
                        print("i",i)
                        cmd="salt %s file.replace %s pattern=%s repl=%s  backup='.bak' dry_run='True'" %(i,edit_config_linux,edit_config_pre,edit_config_last)
                        print("cmd",cmd)
                        msg_success_linux[i]=ssh_connect_command(cmd)
                    for i in host_win:
                        print("i",i)
                        cmd="salt %s file.replace %s pattern=%s repl=%s  backup='.bak' dry_run='True'" %(i,edit_config_win,edit_config_pre,edit_config_last)
                        print("cmd",cmd)
                        msg_success_win[i]=ssh_connect_command(cmd)
                    msg_success=dict(msg_success_linux,**msg_success_win)
                    return HttpResponse(json.dumps(dict(msg_success,**msg)), content_type='application/json')
                #return HttpResponse(json.dumps(dict(msg,**msg_success)), content_type='application/json')
                print(dict(msg,**msg_success))
                #执行替换命令
            if edit_config_pre=='追加':
                print("edit_config_pre",edit_config_pre)
                 #第一个参数为追加时则追加
                msg={"code":-1,"msg":'配置添加到了文件末尾'+str(host_linux),'status':'success'}
                for i in host_linux:
                    print("i",i)
                    cmd="salt %s file.replace %s pattern=%s repl=%s  backup='.bak'  append_if_not_found='True'" %(i,edit_config_linux,edit_config_pre,edit_config_last)
                    print("cmd",cmd)
                    msg_success_linux[i]=ssh_connect_command(cmd)
                    target_ids = str(uuid.uuid1())
                    operation_record(target_ids,ret['userid'],ret['user_name'],action=i+'执行命令:'+cmd,result='True')
                    opertion_minions(target_ids,i,edit_before,edit_after,remark='文件位置为:'+edit_config_linux)
                for i in host_win:
                    print("i",i)
                    cmd="salt %s file.replace %s pattern=%s repl=%s  backup='.bak'  append_if_not_found='True'" %(i,edit_config_win,edit_config_pre,edit_config_last)
                    print("cmd",cmd)
                    msg_success_win[i]=ssh_connect_command(cmd)
                    target_ids = str(uuid.uuid1())
                    operation_record(target_ids,ret['userid'],ret['user_name'],action=i+'执行命令:'+cmd,result='True')
                    opertion_minions(target_ids,i,edit_before,edit_after,remark='文件位置为:'+edit_config_win)
                msg_success=dict(msg_success_linux,**msg_success_win)
                return HttpResponse(json.dumps(dict(msg_success,**msg)), content_type='application/json')
                
            else:
                #执行替换
                msg_success_linux={}
                msg_success_win={}
                msg_success={}
                msg={"code":-1,"msg":'配置已修改完成'+str(host_linux),'status':'success'}
                for i in host_linux:
                    print("i",i)
                    cmd="salt %s file.replace %s pattern=%s repl=%s  backup='.bak'" %(i,edit_config_linux,edit_config_pre,edit_config_last)
                    print("cmd",cmd)
                    msg_success_win[i]=ssh_connect_command(cmd)
                    target_ids = str(uuid.uuid1())
                    operation_record(target_ids,ret['userid'],ret['user_name'],action=i+'执行命令:'+cmd,result='True')
                    opertion_minions(target_ids,i,edit_before,edit_after,remark='文件位置为:'+edit_config_linux)
                for i in host_win:
                    print("i",i)
                    cmd="salt %s file.replace %s pattern=%s repl=%s  backup='.bak'" %(i,edit_config_win,edit_config_pre,edit_config_last)
                    print("cmd",cmd)
                    msg_success_linux[i]=ssh_connect_command(cmd)
                    target_ids = str(uuid.uuid1())
                    operation_record(target_ids,ret['userid'],ret['user_name'],action=i+'执行命令:'+cmd,result='True')
                    opertion_minions(target_ids,i,edit_before,edit_after,remark='文件位置为:'+edit_config_win)
                msg_success=dict(msg_success_linux,**msg_success_win)
                print("msg_success",type(msg_success),len(msg_success),msg_success)
                if msg_success=='{}':
                    msg={"code":-1,"msg":'未配到，修改未成功','status':'success'}
                    return HttpResponse(json.dumps(msg), content_type='application/json')
                else:
                    return HttpResponse(json.dumps(dict(msg_success,**msg)), content_type='application/json')
        return HttpResponse(json.dumps({"code":1,"msg":"参数异常，请查看日志"}), content_type='application/json')
    return render_to_response('salt_api/exec_cmd.html',{'dcen_list':ips} )

#文件上传函数
def upload_files(request):
    PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    print("PROJECT_DIR",PROJECT_DIR)
    UPLOAD_DIR = os.path.join(PROJECT_DIR, 'upload')
    print("UPLOAD_DIR",UPLOAD_DIR)
    print(str(request))
    user_name = request.user
    ret = get_user_info(user_name)
    target_ids = str(uuid.uuid1())
    if request.method == "POST":
        f = request.FILES.get('file')
#         baseDir = os.path.dirname(os.path.abspath(__name__));
#         jpgdir = os.path.join(baseDir,'static','jpg');
        print("file",f)
        filename = os.path.join(UPLOAD_DIR,f.name);
        fobj = open(filename,'wb');
        for chrunk in f.chunks():
            fobj.write(chrunk);
        fobj.close();
        operation_record(target_ids,ret['userid'],ret['user_name'],action='上传文件命令',result='True')
        opertion_minions(target_ids,'localhost',remark='上传文件地址:'+filename)
        return HttpResponse(json.dumps({"name":1,"msg":str(f)+":文件上传成功"}), content_type='application/json')
    else:
        operation_record(target_ids,ret['userid'],ret['user_name'],action='上传文件命令',result='False')
        opertion_minions(target_ids,'localhost',remark='上传失败')
        return HttpResponse(json.dumps({"name":-1,"msg":str(f)+"文件上传失败，请看日志"}), content_type='application/json')

#yum源初始化中，下载httpd并处理配置文件
def yum_init(request):
    msg_success={}
    if request.is_ajax(): 
        yum_init_port = request.GET.get("yum_init_port")
        yum_init_src = request.GET.get("yum_init_src")
        print("yum_init_port",type(yum_init_port),yum_init_port)
        print("yum_init_src",type(yum_init_src),yum_init_src)
        salt_api = get_salt_api()
        print(salt_api.url)
        compile_rule = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')#匹配IP
        match_list = re.findall(compile_rule, salt_api.url) 
        print("match_list",match_list)
        temp=" ".join(match_list)+":"+yum_init_port#替换原有的Listen 80
        listen = "Listen "+temp
        cmd='yum install -y httpd'
        msg_success[str(cmd)]=ssh_connect_command(cmd)
        cmd='mkdir -p /var/www/html/centos && service httpd restart'
        msg_success[str(cmd)]=ssh_connect_command(cmd)
        cmd="sed -i 's/Listen 80/%s/' /etc/httpd/conf/httpd.conf && service httpd restart" %(listen)
        msg_success[str(cmd)]=ssh_connect_command(cmd)
        #安装yum-utils下载rpm及其依赖包
        cmd='yum install -y yum-utils'
        msg_success[str(cmd)]=ssh_connect_command(cmd)
        #修改Listen 80为本地IP+port
        print("msg_success",msg_success)
        msg={"code":1,"msg":msg_success,'status':'success'}
        print("json.dumps(msg)",json.dumps(msg))
        #记录到日志里面
        user_name = request.user
        ret = get_user_info(user_name)
        target_ids = str(uuid.uuid1())
        #提取所有的命令，写入数据库日志表中
        cmd = [x for x in msg_success]
        remark = ','.join(cmd)#a,c,b
        operation_record(target_ids,ret['userid'],ret['user_name'],action='本地yum初始化',result='True')
        opertion_minions(target_ids,'salt_master','None','None',remark)
        return HttpResponse(json.dumps(dict(msg_success,**msg)), content_type='application/json')

#yum源创建
def yum_create(request):
    msg_success={}
    if request.is_ajax(): 
        create_yum_name = request.GET.get("create_yum_name")
        salt_api = get_salt_api()
        print("222",salt_api.url)
        compile_rule = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')#匹配IP
        match_list = re.findall(compile_rule, salt_api.url) 
        print("match_list",match_list)
        print("1111111111111111111")
        temp=" ".join(match_list)+":"#替换原有的Listen 80
        if str(create_yum_name).find(","):#如果找到,说明有多个则需要做处理
            create_yum_name=create_yum_name.split(',')
            create_yum_name=' '.join(create_yum_name)
        else:
            create_yum_name=create_yum_name
            print("create_yum_name",create_yum_name)
        #获取配置文件中的httpd路径
        data = read_config('yum_http')
        print("data['url']",data['url'])
        cmd='yum clean all'
        msg_success[str(cmd)]=ssh_connect_command(cmd)
        cmd='yumdownloader --destdir /var/www/html/centos/ %s' %(create_yum_name)#下载对应的rpm包
        print("cmd",cmd)
        msg_success[str(cmd)]=ssh_connect_command(cmd)
        cmd='createrepo -v /var/www/html/centos/ && service httpd restart'#生成repodata目录，自动创建索引信息
        msg_success[str(cmd)]=ssh_connect_command(cmd)
        cmd='createrepo --update /var/www/html/centos/'#每次有新包则需要更新这个文件
        msg_success[str(cmd)]=ssh_connect_command(cmd)
        repo_name='/var/www/html/centos/local_init.repo'
        url=data['url']+'centos'
        print("url",url)
        cmd="rm -f %s && echo '[base]'>>%s && echo 'name=local repo' >>%s && echo 'baseurl=%s' >>%s && echo 'enabled=1'>>%s && echo 'gpgcheck=0' >>%s" \
        %(repo_name,repo_name,repo_name,url,repo_name,repo_name,repo_name)
        msg_success[str(cmd)]=ssh_connect_command(cmd)+'执行结果为空'
        #复制repo文件到file_roots目录下面
        #找到master的file_roots目录
        cmd="grep -A10 'file_roots:' /etc/salt/master|grep -v '#'|grep ' -'|awk -F'-' '{print $2}'"
        msg_success[str(cmd)]=file_roots=ssh_connect_command(cmd)[1:-5]
        print("file_roots",file_roots)
        cmd='mv /var/www/html/centos/local_init.repo %s/local_init.repo' % (file_roots)
        msg_success[str(cmd)]=ssh_connect_command(cmd)
        msg={"code":1,'status':'success'}
        print("json.dumps(msg)",json.dumps(dict(msg_success,**msg)))
        #写日志到数据库
        user_name = request.user
        ret = get_user_info(user_name)
        target_ids = str(uuid.uuid1())
        #提取所有的命令，写入数据库日志表中
        cmd = [x for x in msg_success]
        remark = ','.join(cmd)#a,c,b
        operation_record(target_ids,ret['userid'],ret['user_name'],action='创建yum源:'+create_yum_name,result='True')
        opertion_minions(target_ids,'salt_master','None','None',remark)
        return HttpResponse(json.dumps(dict(msg_success,**msg)), content_type='application/json')
#yum包分发到各个salt_minion机器上
def yum_deploy(request):
    msg_success={}
    msg_faild={}
    result_failed={}
    result_scuess={}
    if request.is_ajax(): 
        ips = request.GET.get("ips")
        ips=list(ips.split(','))
        print("ips",type(ips),ips)
        yum_salt_rpm = request.GET.get("yum_salt_rpm")
        sql_minion_id="select ip,minion_id,ostype from `host` where ip in "+format_args(ips)
        minion_ids = exec_sql_args(sql_minion_id,ips)
        minion_id = [x['minion_id'] for x in minion_ids]
        print("minion_idsssssssssssssss",minion_id)
        if str(yum_salt_rpm).find(",")>=0:#如果未找到,说明有只有一个包名
            print("str(yum_salt_rpm).find(",")",str(yum_salt_rpm).find(","))
            yum_salt_rpm=yum_salt_rpm.split(',')
            yum_salt_rpm=' '.join(yum_salt_rpm)
        else:
            yum_salt_rpm=yum_salt_rpm
        print("yum_salt_rpm",type(yum_salt_rpm),yum_salt_rpm)
        #首先将初始化yum源中的  
        salt_api = get_salt_api()
        #备份minion下的repo文件
        result_cmd = salt_api.salt_command(format_minionIDs(minion_id),'cmd.run','mkdir -p /etc/yum.repos.d/yum_bak && mv -f /etc/yum.repos.d/*.repo.aa /etc/yum.repos.d/yum_bak')
        #清理yum缓存 
        salt_api.salt_command(format_minionIDs(minion_id),'cmd.run','yum clean all')
        #result=salt_api.
        #复制文件到salit_minion目录下
        result=salt_api.salt_command_two_args(format_minionIDs(minion_id),'cp.get_file','salt://local_init.repo', '/etc/yum.repos.d/local_init.repo')
        error_list=['False','error','No minions matched','No command was sent',
                            'no jid was assigned','issue any command','is not recognized',
                            'Usage:','ERROR: Specified cwd','is not available','salt: error:','Minion did not return',
                            'Passed invalid arguments','caused an exception','contains no section headers','Connection refused','Error: Package:','Error'
                            ]
        print("zzz",result)
        result=format_result(result)
        for k1,v1 in result.items():
            for v2 in error_list:
                #判断error_list中的串是否在result_list串中出现
                #grains.items成功的命令中有出现:False，需要将这种情况
                if str(v1).find(v2)==-1:#等于-1说明没找到
                    pass
                else:
                    #先将找到了的找出，找到了就说明是有问题的
                    result_failed[k1]=v1
        print("result_failed1",result_failed)
        temp1=[]#获取所有的minion_id
        temp2=[]#获取失败的minion_id
        #使用set取result差集，排除掉result_failed，那么剩下的就是result_scuess
        for k2,v2 in result.items():
            temp1.append(k2)
        for k3,v3 in result_failed.items():
            temp2.append(k3)
            result_failed[k3]=v3
        s= set(temp1)-set(temp2)#这里就是剩下的执行成功的minion_id
        for k,v in result.items():#通过比较原始的执行结果的value是否与执行成功的minion_id相等，如果相等则加进result_scuess
            for i in list(set(temp1)-set(temp2)):
                if i==k:
                    result_scuess[i]=v
        #给执行失败的结果添加一个标识，以供前台区分
        for k, v in result_failed.items():
            result_failed[k]='ERROR:'+str(v)
        print("result",result)
        print("result_failed2",result_failed)
        result_cp=dict(result_scuess,**result_failed)
        print("result_cp",result_cp)
        #这里处理安装包
        result_yum = salt_api.salt_command(format_minionIDs(minion_id),'cmd.run','yum install -y '+yum_salt_rpm)
        print("result_yum_1",result_yum)
        for k1,v1 in result_yum.items():
            for v2 in error_list:
                #判断error_list中的串是否在result_list串中出现
                #grains.items成功的命令中有出现:False，需要将这种情况
                if str(v1).find(v2)==-1:#等于-1说明没找到
                    pass
                else:
                    #先将找到了的找出，找到了就说明是有问题的
                    result_failed[k1]=v1
        print("result_failed",result_failed)
        temp1=[]#获取所有的minion_id
        temp2=[]#获取失败的minion_id
        #使用set取result差集，排除掉result_failed，那么剩下的就是result_scuess
        for k2,v2 in result_yum.items():
            temp1.append(k2)
        for k3,v3 in result_failed.items():
            temp2.append(k3)
            result_failed[k3]=v3
        s= set(temp1)-set(temp2)#这里就是剩下的执行成功的minion_id
        for k,v in result_yum.items():#通过比较原始的执行结果的value是否与执行成功的minion_id相等，如果相等则加进result_scuess
            for i in list(set(temp1)-set(temp2)):
                if i==k:
                    result_scuess[i]=v
        #给执行失败的结果添加一个标识，以供前台区分
        for k, v in result_failed.items():
            result_failed[k]='ERROR:'+str(v)
            
        #写入日志
        user_name = request.user
        ret = get_user_info(user_name)
        args= yum_salt_rpm#记录参数
        #记录成功的命令
        for k,v in result_scuess.items():
            target_ids = str(uuid.uuid1())
            operation_record(target_ids,ret['userid'],ret['user_name'],action=k+'集群安装:yum install -y '+args,result='True')
            opertion_minions(target_ids,k,remark='执行salt命令:yum install -y '+args)
        #记录失败的命令
        for k,v in result_failed.items():
            target_ids = str(uuid.uuid1())
            operation_record(target_ids,ret['userid'],ret['user_name'],action=k+'集群安装:yum install -y '+args,result='False')
            opertion_minions(target_ids,k,remark='执行salt命令:yum install -y '+args)
        print("result_failed——2",result_failed)
        result_yum=dict(result_scuess,**result_failed)
        print("result_yums",result_yum)
        #合并cp.getfile怀yum install的结果,这里不能合并，因为两个key是一样的，所以不 合并，只看最后的yum的结果
        result=replace_dict_value(result_yum,'\n','<br>')
        if result!={}:
            print("123123123")
            msg={"code":1,'status':'success'}
            result=dict(msg,**result)
            print("result_a",result)
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"code":-1,"msg":"执行结果为空，执行失败，请看日志",'status':'error'}), content_type='application/json')
# Create your views here.
def test1(request):
    
    dcen_list=['dcen_list1','dcen_list2','dcen_list3','dcen_list4']
    data_centers=['广东','上海','北京','天津']
    print(type(data_centers),data_centers)
    sls_list=['sls1','sls2','sls3','sls4']
    sls_mod_dict=['sls_mod_dict1','sls_mod_dict2','sls_mod_dict3','sls_mod_dict4']

    
    
    
def test2(request):
    
    dcen_list=['dcen_list1','dcen_list2','dcen_list3','dcen_list4']
    data_centers=['广东','上海','北京','天津']
    print(type(data_centers),data_centers)
    sls_list=['sls1','sls2','sls3','sls4']
    sls_mod_dict=['sls_mod_dict1','sls_mod_dict2','sls_mod_dict3','sls_mod_dict4']
    return render_to_response('salt_api/test2.html',
                            { 'data_centers': data_centers,
                            'sls_list': sls_list,
                            'sls_mod_dict': sls_mod_dict
                                }
                            )
#ajax菜单二级联动


#处理时间json,
#TypeError: datetime.datetime(2017, 8, 31, 10, 8, 19) is not JSON serializable
class DateEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj, datetime.datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S')  
        elif isinstance(obj, date):  
            return obj.strftime("%Y-%m-%d")  
        else:  
            return json.JSONEncoder.default(self, obj)

def liandong(request):
    #http://blog.csdn.net/guduchina/article/details/11681513w
    if request.is_ajax():
        print("if request.is_ajax()")
        if 'samllselect' in request.GET:
            print("samllselect")
            samllselect=request.GET.get('samllselect')
            print("前台选中的",type(samllselect),samllselect)
            result = select_all('host')#返回给前台ajax的值
            print("result",type(result),result[0])
            return HttpResponse(json.dumps(result,cls=DateEncoder), content_type='application/json')
    return render_to_response('test2.html')


def test3(request):
    
    dcen_list=['dcen_list1','dcen_list2','dcen_list3','dcen_list4']
    data_centers=['广东','上海','北京','天津']
    print(type(data_centers),data_centers)
    sls_list=['sls1','sls2','sls3','sls4']
    sls_mod_dict=['sls_mod_dict1','sls_mod_dict2','sls_mod_dict3','sls_mod_dict4']
    return render_to_response('salt_api/test3.html',
                            { 'data_centers': data_centers,
                            'sls_list': sls_list,
                            'sls_mod_dict': sls_mod_dict
                                }
                            )
def test4(request):
    
    dcen_list=['dcen_list1','dcen_list2','dcen_list3','dcen_list4']
    data_centers=['广东','上海','北京','天津']
    print(type(data_centers),data_centers)
    sls_list=['sls1','sls2','sls3','sls4']
    sls_mod_dict=['sls_mod_dict1','sls_mod_dict2','sls_mod_dict3','sls_mod_dict4']
    a='IDC，返回值'
    '''
                使用 locals() 时要注意是它将包括所有的局部变量，它们可能比你想让模板访问的要多。甚至有你没有想象到的变量也会发送到模板。在本例中，locals() 还包含了 request 。对此如何取舍取决你的应用程序
                在本例中， locals() 并没有带来多大的改进，只是一个小技巧，但是如果有多个模板变量要界定而你又想偷懒，这种技术可以减少一些键盘输入。.
    '''
    return render_to_response('salt_api/123.html',locals())

def multiselect(request):
    
    dcen_list=['dcen_list1','dcen_list2','dcen_list3','dcen_list4']
    data_centers=['广东','上海','北京','天津']
    print(type(data_centers),data_centers)
    sls_list=['sls1','sls2','sls3','sls4']
    sls_mod_dict=['sls_mod_dict1','sls_mod_dict2','sls_mod_dict3','sls_mod_dict4']
    a='IDC，返回值'
    '''
                使用 locals() 时要注意是它将包括所有的局部变量，它们可能比你想让模板访问的要多。甚至有你没有想象到的变量也会发送到模板。在本例中，locals() 还包含了 request 。对此如何取舍取决你的应用程序
                在本例中， locals() 并没有带来多大的改进，只是一个小技巧，但是如果有多个模板变量要界定而你又想偷懒，这种技术可以减少一些键盘输入。
    '''
    return render_to_response('test/Multiselect.html',locals())


#下面是针对test模板中的测试页面的
def deploy(request):
    
    dcen_list=['dcen_list1','dcen_list2','dcen_list3','dcen_list4']
    data_centers=['广东','上海','北京','天津']
    print(type(data_centers),data_centers)
    sls_list=['sls1','sls2','sls3','sls4']
    sls_mod_dict=['sls_mod_dict1','sls_mod_dict2','sls_mod_dict3','sls_mod_dict4']
    a='IDC，返回值'
    '''
                使用 locals() 时要注意是它将包括所有的局部变量，它们可能比你想让模板访问的要多。甚至有你没有想象到的变量也会发送到模板。在本例中，locals() 还包含了 request 。对此如何取舍取决你的应用程序
                在本例中， locals() 并没有带来多大的改进，只是一个小技巧，但是如果有多个模板变量要界定而你又想偷懒，这种技术可以减少一些键盘输入。
    '''
    return render_to_response('test/salt_deploy.html',locals())
def update(request):
    
    dcen_list=['dcen_list1','dcen_list2','dcen_list3','dcen_list4']
    data_centers=['广东','上海','北京','天津']
    print(type(data_centers),data_centers)
    sls_list=['sls1','sls2','sls3','sls4']
    sls_mod_dict=['sls_mod_dict1','sls_mod_dict2','sls_mod_dict3','sls_mod_dict4']
    a='IDC，返回值'
    '''
                使用 locals() 时要注意是它将包括所有的局部变量，它们可能比你想让模板访问的要多。甚至有你没有想象到的变量也会发送到模板。在本例中，locals() 还包含了 request 。对此如何取舍取决你的应用程序
                在本例中， locals() 并没有带来多大的改进，只是一个小技巧，但是如果有多个模板变量要界定而你又想偷懒，这种技术可以减少一些键盘输入。
    '''
    return render_to_response('test/salt_update.html',locals())
def routine(request):
    
    dcen_list=['dcen_list1','dcen_list2','dcen_list3','dcen_list4']
    data_centers=['广东','上海','北京','天津']
    print(type(data_centers),data_centers)
    sls_list=['sls1','sls2','sls3','sls4']
    sls_mod_dict=['sls_mod_dict1','sls_mod_dict2','sls_mod_dict3','sls_mod_dict4']
    a='IDC，返回值'
    '''
                使用 locals() 时要注意是它将包括所有的局部变量，它们可能比你想让模板访问的要多。甚至有你没有想象到的变量也会发送到模板。在本例中，locals() 还包含了 request 。对此如何取舍取决你的应用程序
                在本例中， locals() 并没有带来多大的改进，只是一个小技巧，但是如果有多个模板变量要界定而你又想偷懒，这种技术可以减少一些键盘输入。
    '''
    return render_to_response('test/salt_routne.html',locals())
def execute(request):
    
    dcen_list=['dcen_list1','dcen_list2','dcen_list3','dcen_list4']
    data_centers=['广东','上海','北京','天津']
    print(type(data_centers),data_centers)
    sls_list=['sls1','sls2','sls3','sls4']
    sls_mod_dict=['sls_mod_dict1','sls_mod_dict2','sls_mod_dict3','sls_mod_dict4']
    a='IDC，返回值'
    '''
                使用 locals() 时要注意是它将包括所有的局部变量，它们可能比你想让模板访问的要多。甚至有你没有想象到的变量也会发送到模板。在本例中，locals() 还包含了 request 。对此如何取舍取决你的应用程序
                在本例中， locals() 并没有带来多大的改进，只是一个小技巧，但是如果有多个模板变量要界定而你又想偷懒，这种技术可以减少一些键盘输入。。.
    '''
    return render_to_response('test/salt_execute.html',locals())


def uitest1(request):
    
    dcen_list=['dcen_list1','dcen_list2','dcen_list3','dcen_list4']
    data_centers=['广东','上海','北京','天津']
    print(type(data_centers),data_centers)
    sls_list=['sls1','sls2','sls3','sls4']
    sls_mod_dict=['sls_mod_dict1','sls_mod_dict2','sls_mod_dict3','sls_mod_dict4']
    a='IDC，返回值'
    '''
                使用 locals() 时要注意是它将包括所有的局部变量，它们可能比你想让模板访问的要多。甚至有你没有想象到的变量也会发送到模板。在本例中，locals() 还包含了 request 。对此如何取舍取决你的应用程序
                在本例中， locals() 并没有带来多大的改进，只是一个小技巧，但是如果有多个模板变量要界定而你又想偷懒，这种技术可以减少一些键盘输入。。.
    '''
    return render_to_response('test/uitest1.html',locals())


#命令执行方式
def uitest2(request):
    
    dcen_list=['dcen_list1','dcen_list2','dcen_list3','dcen_list4']
    data_centers=['广东','上海','北京','天津']
    print(type(data_centers),data_centers)
    sls_list=['sls1','sls2','sls3','sls4']
    sls_mod_dict=['sls_mod_dict1','sls_mod_dict2','sls_mod_dict3','sls_mod_dict4']
    a='IDC，返回值'
    '''
                使用 locals() 时要注意是它将包括所有的局部变量，它们可能比你想让模板访问的要多。甚至有你没有想象到的变量也会发送到模板。在本例中，locals() 还包含了 request 。对此如何取舍取决你的应用程序
                在本例中， locals() 并没有带来多大的改进，只是一个小技巧，但是如果有多个模板变量要界定而你又想偷懒，这种技术可以减少一些键盘输入。。.
    '''
    return render_to_response('test/uitest2.html',locals())




def test1213(request):
    
    dcen_list=['dcen_list1','dcen_list2','dcen_list3','dcen_list4']
    data_centers=['广东','上海','北京','天津']
    print(type(data_centers),data_centers)
    sls_list=['sls1','sls2','sls3','sls4']
    sls_mod_dict=['sls_mod_dict1','sls_mod_dict2','sls_mod_dict3','sls_mod_dict4']
    a='IDC，返回值'
    '''
                使用 locals() 时要注意是它将包括所有的局部变量，它们可能比你想让模板访问的要多。甚至有你没有想象到的变量也会发送到模板。在本例中，locals() 还包含了 request 。对此如何取舍取决你的应用程序
                在本例中， locals() 并没有带来多大的改进，只是一个小技巧，但是如果有多个模板变量要界定而你又想偷懒，这种技术可以减少一些键盘输入。。.
    '''
    return render_to_response('test/1213.html',locals())

def pag1(request):
    '''
    Django模块
    '''
    ONE_PAGE_OF_DATA = 5  
    posts=[]
    del posts[:]
    try:  
        curPage = int(request.GET.get('curPage', '1'))  
        allPage = int(request.GET.get('allPage','1'))  
        pageType = str(request.GET.get('pageType', ''))  
    except ValueError:  
        curPage = 1  
        allPage = 1  
        pageType = ''  
  
    #判断点击了【下一页】还是【上一页】  
    if pageType == 'pageDown':  
        curPage += 1  
    elif pageType == 'pageUp':  
        curPage -= 1  
  
    startPos = (curPage - 1) * ONE_PAGE_OF_DATA  
    endPos = startPos + ONE_PAGE_OF_DATA  
    print("startPos,endPos",startPos,endPos)
    posts = exec_sql_args("select * from `host` limit %s,%s",(startPos,endPos))
    print("posts",posts)
    print("posts",len(posts))
  
    if curPage == 1 and allPage == 1: #标记1  
        allPostCounts = exec_sql("select count(*) count from `host`")
        print("allPostCounts",type(allPostCounts[0]['count']),allPostCounts[0]['count'])
        allPage = int(allPostCounts[0]['count'] / ONE_PAGE_OF_DATA) 
        print("allPage",allPage)
        remainPost = allPostCounts[0]['count'] % ONE_PAGE_OF_DATA  
        if remainPost > 0:  
            allPage += 1  
    page_num_range=[x for x in range(1,10)]
    return render_to_response("test/pagination.html",{'list_ip':posts, 'allPage':allPage, 'curPage':curPage,"page_num_range":page_num_range})  
#     list_ip = exec_sql("select * from `host`")
#     print("list_ip",list_ip)
#     return render_to_response('test/pagination.html',locals())

 
 
 
 
def pag2(request):
    #每页多少条记录
    ONE_PAGE_OF_DATA=3
    current_page = request.GET.get('p')
    allPostCounts = exec_sql("select count(*) count from `host`")
    print("allPostCounts",type(allPostCounts[0]['count']),allPostCounts[0]['count'])
    total_num = int(allPostCounts[0]['count'])
    total_page_count = int(allPostCounts[0]['count'] / ONE_PAGE_OF_DATA) 
    print("allPage",total_page_count)
    #有多少页
    remainPost = allPostCounts[0]['count'] % ONE_PAGE_OF_DATA  
    #总共的数量
    if remainPost > 0:  
        total_page_count += 1 
    print("allPage",total_page_count)
    '''调用工具类进行分页
    from templates.test.fenye.feye import Pagination
    '''
    page_obj = Pagination(current_page,total_num,ONE_PAGE_OF_DATA,total_page_count,page_url="pag2")
    print("page_obj.start_page_item()",page_obj.start_page_item())
    print("page_obj.end_page_item()",page_obj.end_page_item())
    #mysql这样来分页
    list_ip = exec_sql_args("select * from `host` limit %s,%s",(page_obj.start_page_item(),ONE_PAGE_OF_DATA))
    print("list_ip",len(list_ip),list_ip)
    #data_list = USER_LIST[page_obj.start_page_item():page_obj.end_page_item()]
    return render(request,"test/fenye/pagination.html",{'list_ip':list_ip,'page_obj':page_obj})