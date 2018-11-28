from _datetime import date
import datetime
import json
import os
import uuid

from django.contrib.auth.decorators import login_required, permission_required
from django.http.response import HttpResponse
from django.shortcuts import render_to_response, render
from django.template.context_processors import request

from pymysql_conn import select_table, insert_table, select_all, exec_sql, \
    format_args, exec_sql_args, operation_record, opertion_minions
from salt_api.Mytoolkits import format_result, ssh_connect_command, read_config, \
    replace_clone_file, upload_file, find_err, get_listdict_values, \
    get_file_name, replace_git_view_file, replace_dict_value, \
    replace_git_order_file, get_user_info
from salt_api.salt_api_requests import get_salt_api, format_minionIDs


# Create your views here.
@login_required
@permission_required('login.can_view')
def git_man(request):
    #处理版本管理
    
    print("git_man管理")
    return render(request,'git_manage/git_manage.html',{"code":1})

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
def git_project_group_view(request):
    result={}
    project_name = select_all('project_manage')
    p_name_sql = 'select ip,project_name from project_manage group by project_name'
    p_num_sql = 'select count(distinct project_name) count from project_manage'
    p_name = exec_sql(p_name_sql)
    p_num = exec_sql(p_num_sql)
    print("p_name",type(p_name),p_name)
    print("p_num",type(p_num),p_num)
    #return render(request,'git_manage/git_manage.html',{"p_name":p_name,"p_num":p_num})
    return HttpResponse(json.dumps(project_name,cls=DateEncoder), content_type='application/json')

@login_required
def git_init(request):
    #处理版本管理
    #D:\Program Files\Python_Workspace\test_ui
    PROJECT_DIR = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
    scuess={}
    failed={}
    msg_master_host={}#接收所有在master机器上执行的命令及结果
    if request.is_ajax(): 
        if 'ips' in request.GET:  
            msg_success={}
            ips = request.GET.get("ips").split(',')
            print("ips",type(ips),ips)
            git_project_name = request.GET.get("git_project_name")
            host_group_name = request.GET.get("group_name")
            git_project_dest = request.GET.get("git_project_dest")
            git_project_center = request.GET.get("git_project_center")
            print("view_git_project_center",git_project_center)
            print("git_project_dest",git_project_dest)
            #获取minion_id
            git_minion_id=exec_sql_args("select minion_id from `host` where ip in" +format_args(ips),ips )
            print("git_minion_id",git_minion_id)
            git_minion_ids = [x['minion_id'] for x in git_minion_id]
            for minion_id in git_minion_ids:
                if minion_id=='undefined':
                    msg={'code':1,'msg':minion_id+'未定义的salt_key,请检查','status':'warning'}
                    return HttpResponse(json.dumps(msg), content_type='application/json')
            print("git_minion_id",type(git_minion_id),git_minion_id)
            for i in ips:
                print("i",i)
                data={
                    'ip':i,
                    'project_name':git_project_name,
                    'center_path':git_project_center,
                    'dest_path':git_project_dest,
                    }
                print("data",data)
                temp=select_table('project_manage', data['ip'])
                print("select_table('project_manage', data['ip'])",select_table('project_manage', data['ip']))
                old_ips = [x['ip'] for x in temp]#数据库中存在的IP列表
                old_project_name = [x['project_name'] for x in temp]#数据库中存在的项目名称列表
                if git_project_name  in old_project_name and i in old_ips:#两个都相同的话说明数据已存在，退出
                    #这里还要做判断，处理一个IP对应多个项目的情况
                    msg={'code':1,'msg':data['ip']+':'+data['project_name']+'已存在,不能重复添加','status':'warning'}
                    return HttpResponse(json.dumps(msg), content_type='application/json')
                else:
                    code = insert_table('project_manage',data)
                #自动级联更新host_details表
                    scuess[i]=data['project_name']
                    msg={'code':code,'msg':data['ip']+'项目已添加成功,请在开发机上使用git remote add xxname连接此中心库，并使用git push xxname master推送文件到中心库'}
            #宿主机相当于是中间代码库，会使用git --bare init（只能push/pull无法add与commit）
            #会根据前面提供的路径一一建立,在master机上建立目录
            cmd='mkdir -p %s'%(git_project_center)
            msg_success[str(cmd)]=str(ssh_connect_command(cmd))+'目录创建成功<br>'
            cmd='cd %s && git --bare init'%(git_project_center)#创建一个对应的空的中间库
            msg_success[str(cmd)]=ssh_connect_command(cmd)
            #下面是处理minion_id服务器中的对应目录的初始化
            #首先判断目录是否存在，如不存在则使用git clone git@192.168.153.135:/soft/git/来创建初始化git,这样客户机就与master机建立了联系
            #就可以使用git push,git pull进行代码处理了
            #下面是使用salt '*' cmd.script执行expect脚本执行
            msg_success['replace_config_file']=str(replace_clone_file(git_project_center,git_project_dest))+':动态生成shell文件成功<br>'#动态生成对应参数的git_clone_except脚本
            #上传该脚本
            local_file_path = os.path.join(PROJECT_DIR, 'salt_api\shell\git\git_clone_except.sh')
            file_name=os.path.basename(local_file_path)
            print("local_file_path",local_file_path)
            upload_file(local_file_path)
            #文件上传完之后使用sed命令sed -i "s/\r//" filename  或者 sed -i "s/^M//" filename直接替换结尾符为unix格式
            cmd = "cd %s && sed -i 's/\r//' %s"%(read_config('salt_api_info')['file_roots'],file_name)
            msg_success["sed"]=ssh_connect_command(cmd)+':doc转成unix格式<br>'
            msg_master_host[read_config('salt_master_host')['ip']]=msg_success
            for k,v in msg_master_host.items():
                print("type",k,type(v))
            print("msg_master_host",type(msg_master_host),msg_master_host)
            salt_api = get_salt_api()
            minion_ids=[x['minion_id'] for x in git_minion_id]
            dic_result=salt_api.salt_command(format_minionIDs(minion_ids),'cmd.script','salt://%s'%(file_name))
            #对结果对错进行判断
            error_list=['No such file','False',"'stdout': ''",'is not recognized','could not']
            result_salt=find_err(error_list,dic_result)
            print("dic_result",dic_result)
            #分出结果的正确与否
            result_failed=[]
            for k,v in result_salt.items():
                print("vvvv",k,str(v)[0:5])
                if (str(v)[0:5]=='ERROR' or str(v)=='None'):
                    #失败的
                    result_failed.append(k)
            #获取成功的,总的minion_id减去失败的minion_id
            all_minion_ids = result_salt.keys()
            result_scuess=list(set(all_minion_ids)-set(result_failed))
            print("result_scuess",result_scuess)
            print("result_failed",result_failed)
            #插入日志表中，
            user_name = request.user
            ret = get_user_info(user_name)
            if len(result_scuess)>0:
                target_ids = str(uuid.uuid1())
                operation_record(target_ids,ret['userid'],ret['user_name'],action='项目git初始化成功',result='True')
                for minion_id in result_scuess:
                    opertion_minions(target_ids,minion_id,remark='cmd.script salt://git_clone_except.sh 执行成功')
            if len(result_failed)>0:
                target_ids = str(uuid.uuid1())
                operation_record(target_ids,ret['userid'],ret['user_name'],action='项目git初始化失败',result='False')
                for minion_id in result_failed:
                    opertion_minions(target_ids,minion_id,remark='cmd.script salt://git_clone_except.sh 执行失败')
            result=dict(msg_master_host,**result_salt)
            #执行克隆操作
            #msg_success['salt_git_clone']=salt_api.salt_command(format_minionIDs(minion_ids),'cmd.run',cmd)
            return HttpResponse(json.dumps(dict(result,**msg)), content_type='application/json')
#查看项目版本,比较不同的版本
def view_project_version(request):   
    if request.is_ajax(): 
        if 'view_project' in request.GET:  
            p_name_sql = 'select distinct project_name from project_manage group by project_name'
            project_name = exec_sql(p_name_sql) 
            print("project_name",type(project_name),project_name)
            return HttpResponse(json.dumps(project_name), content_type='application/json')
        if 'project_name' in request.GET:
            PROJECT_DIR = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
            local_file_path = os.path.join(PROJECT_DIR, 'salt_api\sls\git\git_view_version.sls')
            print("local_file_path",local_file_path)
            project_name = request.GET.get("project_name").split(',')
            log_num = request.GET.get("log_num")
            print("log_num",log_num)
            sql_minion = "select minion_id,dest_path from host a,project_manage b where a.ip=b.ip and b.project_name in "+format_args(project_name)
            minion_path = exec_sql_args(sql_minion,project_name) 
            salt_api = get_salt_api()
            print("minion_path",minion_path)
            minions = get_listdict_values(minion_path,'minion_id','dest_path')
            
            for minion_id in minions.keys():
                if minion_id=='undefined':
                    msg={'code':1,'msg':minion_id+'未定义的salt_key,请检查','status':'warning'}
                    return HttpResponse(json.dumps(msg), content_type='application/json')
            
            print("minionsminionsminionsminions",minions)
            s = set()
            for k,v in minions.items():
                s = v
            print("type()s",type(s),s)
            #动态生成view_git_version.sls
            replace_git_view_file(s,log_num)
            #上传sls文件
            upload_file(local_file_path)
            file_name=os.path.basename(local_file_path)
            #salt执行
            dic_result=salt_api.salt_command(format_minionIDs(list(minions.keys())),'state.sls',get_file_name(file_name)['filename'])
            print("dic_resultdic_result",len(dic_result),dic_result)
            if len(dic_result)==0:
                print("dic_resultdic_result1",dic_result)
                msg={'code':-2,'msg':'结果为空','status':'error'}
                return HttpResponse(json.dumps(msg), content_type='application/json')
            
            dict_success={}
            dict_fail={}
            #只取changes的值，但是如果有报错的的话changes为空，所以这里没有这样做了，全部输出到前端
#             for k,v in dic_result.items():
#                 for i,j in v.items():
#                     for s,m in j.items():
#                         print("三层",type(s),type(m),s,m)
#                         if s=='changes':
#                             print(s,m)
#                             dict_success[k]=m
#                         if s=='changes' and m=='{}':
#                             print("三层{}",type(s),type(m),s,m)
#                             dict_fail[k]=m
            print("dict_success",dict_success,dict_fail)
            print("dic_result",dic_result.keys())
            error_list=['Data failed','not available',"'stdout': ''",'False','{}','Data failed to compile','failed:']
            result_salt=find_err(error_list,dic_result)
            print("result_salt",result_salt)
            
            
            #分出结果的正确与否
            result_failed=[]
            for k,v in result_salt.items():
                print("vvvv",k,str(v)[0:5])
                if (str(v)[0:5]=='ERROR' or str(v)=='None'):
                    #失败的
                    result_failed.append(k)
            #获取成功的,总的minion_id减去失败的minion_id
            all_minion_ids = result_salt.keys()
            result_scuess=list(set(all_minion_ids)-set(result_failed))
            print("result_scuess",result_scuess)
            print("result_failed",result_failed)
            
            
            msg={'code':1,'msg':'执行成功'}
            result = replace_dict_value(replace_dict_value(result_salt,'\\n','<br>'),'\\','')
            print("result",result)
            
            #插入日志表中，
            user_name = request.user
            ret = get_user_info(user_name)
            if len(result_scuess)>0:
                target_ids = str(uuid.uuid1())
                operation_record(target_ids,ret['userid'],ret['user_name'],action='项目版本查看成功',result='True')
                for minion_id in result_scuess:
                    opertion_minions(target_ids,minion_id,remark=local_file_path+' git log --stat -'+log_num+' --abbrev-commit --graph --decorate 执行成功')
            if len(result_failed)>0:
                target_ids = str(uuid.uuid1())
                operation_record(target_ids,ret['userid'],ret['user_name'],action='项目版本查看失败',result='False')
                for minion_id in result_failed:
                    opertion_minions(target_ids,minion_id,remark=local_file_path+' git log --stat -'+log_num+' --abbrev-commit --graph --decorate 执行失败')
            
            
            
            return HttpResponse(json.dumps(dict(result,**msg)), content_type='application/json')
            #get_salt_api.salt_command(format_minionIDs(minions),'cmd.run','')
            #view_project_result = salt_api.salt_command(format_minionIDs([x['minion_id']]))
#查看中心库版本
def view_center_version(request): 
    if request.is_ajax(): 
        msg_success={}
        result={}
        if 'project_name' in request.GET:
            project_name = request.GET.get("project_name").split(',')
            sql_path = "select distinct center_path from project_manage where project_name = "+format_args(project_name)
            center_path = format_result(exec_sql_args(sql_path,project_name))
            print("center_path",center_path)
            cmd='cd %s && git log --stat -5 --abbrev-commit --graph --decorate ' %(center_path['center_path'])#下载对应的rpm包
            print("cmd",cmd)
            msg_success[str(cmd)]=ssh_connect_command(cmd)
            print("msg_success",msg_success)
            temp = msg_success.get(cmd)
            if temp==None:
                msg_success[cmd]='ERROR:'+'中心库不存在此项目目录或者未没有任何提交'
#             err_list = ['None']
#             result = find_err(err_list,msg_success)
#             print("result",result)
        return HttpResponse(json.dumps(msg_success), content_type='application/json')
def git_deploy_version(request):
    msg_success = {}
    if 'project_name' in request.GET:
        project_name = request.GET.get("project_name").split(',')
        print("project_name",project_name)
#         version_num = request.GET.get("version_num")
        git_pull_project = request.GET.get("git_pull_project")
        ss=str(git_pull_project)
        print("ssss",ss)
        print("project_name",('.').join(project_name))
        pre_view = request.GET.get("pre_view")
#         if version_num=='':
#             print("为空")
        if git_pull_project=='':
            git_pull_project='git pull'
        print("git_pull_project",git_pull_project)
        sql_minion = "select minion_id,dest_path from host a,project_manage b where a.ip=b.ip and b.project_name in "+format_args(project_name)
        minion_path = exec_sql_args(sql_minion,project_name) 
        salt_api = get_salt_api()
        print("minion_path",minion_path)
        minions = get_listdict_values(minion_path,'minion_id','dest_path')
        print("minionsminionsminions",minions)
        #动态生成git_order.sh
        s = set()
        for k,v in minions.items():
            s = v
        replace_git_order_file(s,git_pull_project)
        #上传要执行的sh文件
        PROJECT_DIR = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
        local_file_path = os.path.join(PROJECT_DIR, 'salt_api\shell\git\git_order.sh')
        upload_file(local_file_path)
        file_name=os.path.basename(local_file_path)
        print("file_name",file_name)
        #文件上传完之后使用sed命令sed -i "s/\r//" filename  或者 sed -i "s/^M//" filename直接替换结尾符为unix格式
        cmd = "cd %s && sed -i 's/\r//' %s" %(read_config('salt_api_info')['file_roots'],file_name)
        msg_success["sed"]=ssh_connect_command(cmd)+':doc转成unix格式<br>'
        
        #salt执行
        dic_result=salt_api.salt_command(format_minionIDs(list(minions.keys())),'cmd.script','salt://%s'%(file_name))
        print("dic_result",dic_result)
        
        if dic_result=='':
            print("NONENONE")
        
        error_list=['not available','',"'stdout': ''",'False','{}','Data failed to compile','failed:','not','fatal']
        result_salt=find_err(error_list,dic_result)
        print("result_salt",result_salt)
        msg={'code':1,'msg':'执行成功'}
        result = replace_dict_value(replace_dict_value(result_salt,'\r',''),'\\','')
        
        #分出结果的正确与否
        result_failed=[]
        for k,v in result_salt.items():
            print("vvvv",k,str(v)[0:5])
            if (str(v)[0:5]=='ERROR' or str(v)=='None'):
                #失败的
                result_failed.append(k)
        #获取成功的,总的minion_id减去失败的minion_id
        all_minion_ids = minions.keys()
        result_scuess=list(set(all_minion_ids)-set(result_failed))
        
        #插入日志表中，
        user_name = request.user
        ret = get_user_info(user_name)
        if len(result_scuess)>0:
            target_ids = str(uuid.uuid1())
            operation_record(target_ids,ret['userid'],ret['user_name'],action='命令:'+ss+'执行成功',result='True')
            for minion_id in result_scuess:
                opertion_minions(target_ids,minion_id,remark='项目'+('.').join(project_name)+'命令'+ss+' 执行成功')
        if len(result_failed)>0:
            target_ids = str(uuid.uuid1())
            operation_record(target_ids,ret['userid'],ret['user_name'],action='命令:'+ss+'执行失败',result='False')
            for minion_id in result_failed:
                opertion_minions(target_ids,minion_id,remark='项目'+('.').join(project_name)+'命令'+ss+' 执行失败')
        
        return HttpResponse(json.dumps(dict(result,**msg)), content_type='application/json')
