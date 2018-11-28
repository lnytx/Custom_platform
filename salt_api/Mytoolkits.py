# -*- coding:utf-8 -*-
'''
功能salt执行的结果，一些
'''
from _datetime import date
import configparser
import datetime
import json
import os
import re
import time

from django.contrib.auth.models import User
import paramiko
import pexpect

from pymysql_conn import connect
from salt_api.loggingclass import log_record


# from django.contrib.auth.models import User
#python的expect模块
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
logfile=os.path.join(PROJECT_DIR, 'log_dir\paramiko_ssh.log')
log=log_record(logfile)#写入日志
def format_result(ret):
    '''
    输入列表list[{'172.17.39.208_windows10_app': ['d:/1012/aaa/temp/1.txt', 'd:/1012/aaa/temp/2.txt', 'd:/1012/aaa/temp/3.txt']}, {'windows10_app': False, '172.17.39.96_web1_centos7_2': False}]
    这种类型的执行结果，将其转化成dict
    {'windows10_app': False, '172.17.39.208_windows10_app': ['d:/1012/aaa/temp/1.txt', 'd:/1012/aaa/temp/2.txt', 'd:/1012/aaa/temp/3.txt'], '172.17.39.96_web1_centos7_2': False}
    '''
    result={}
    if isinstance(ret,list):
        for item in ret:
            for i,k in item.items():
                result[i]=k
        return result
    elif isinstance(ret,dict):
        return ret

def get_listdict_values(ret,key,value):
    '''
    将[{'minion_id': '172.17.39.208_windows10_app', 'dest_path': '/soft/OMS'}, {'minion_id': '172.17.39.96_web1_centos7_2', 'dest_path': '/soft/OMS'}]
    结果为{'172.17.39.208_windows10_app':'/soft/OMS','172.17.39.96_web1_centos7_2':''/soft/OMS''}
    这种由数据库查出来的有相同key值的dict列表中的values提取出来,
    输入的是get_listdict_values(ret,'minion_id','dest_path')minion_id为后来的key,dest_path为后来的value
    最后的结果为{'192.168.174.133_web1': '/soft/EC_MY', 'this is a': '/soft/EC_MY', 'windows10_app': '/soft/EC_MY', '172.17.39.96_web1_centos7_2': '/soft/EC_MY', '172.17.39.208_windows10_app': '/soft/EC_MY'}
    '''
    result={}
    if isinstance(ret,list):
        for item in ret:
            print("items",type(item),item)
            print("items[key]",item[key])
            for k,v in item.items():
                result[item[key]]=item[value]
        return result
    else:
        return ret
            
  
#读取配置文件
def read_config(sections):
    PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    print("PROJECT_DIR",PROJECT_DIR)
    print("os.path.dirname(__file__)",os.path.dirname(__file__))
    confile = os.path.join(PROJECT_DIR, 'config_dir\salt_api.conf')
    print("confile",confile)
    data = {}  
    config = configparser.ConfigParser()
    try:  
        with open(confile,'r') as confile:  
            config.readfp(confile)  
        #config.read(filename)  
            for k,v in config.items(sections):#读取配置文件中的指定section
                print(k,v)
                data[k] = v
            print("data",data)
            return data      
        
    except Exception as e:  
        print ("Open file error." ,log.error(str(e)))
#使用paramiko在salt主机上执行一些命令
def ssh_connect_command(command):
    confile = os.path.join(PROJECT_DIR, 'config_dir\salt_api.conf')
    sections='salt_master_host'#从这里读取配置文件信息
    data=read_config(sections)
    print("data",type(data),data)
    no_con_server=[]
    try:
        ssh = paramiko.SSHClient()
        paramiko.util.log_to_file(logfile)
        #允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("ip+端口",data['ip'],data['port'])
        ssh.connect(data['ip'], int(data['port']),data['username'], data['password'],timeout=1)
        try:
            stdin,stdout,stderr = ssh.exec_command(command)
            channel = stdout.channel
            status = channel.recv_exit_status()
            print("status",status)
            if status==0:
                print("已经连接到该主机%s:%s，%s命令执行成功" %(data['ip'],data['port'],command))
                #打印执行的命令
                ret=stdout.read().decode('utf-8')
                print ("ret",type(ret),len(ret),ret)
                return ret.replace("\n", "<br/>")
            else:
                print("执行命令%s报错,请查看日志"% (status,logfile))
                log.error(str(stderr.read()))
                print (stderr.read().decode('utf-8'))
                ret=stderr.read().decode('utf-8')
                print("retretretret",ret)
                return ret.replace("\n", "<br/>")
        except Exception as e:
            print ("执行命令%s时报错，请看日志" % command,logfile,'\n',stderr.read().decode('utf-8'),log.error(str(e)))
            sessions=data['ip']+":"+data['port']
            #执行命令异常的IP写入到数据库，这里是写入到一个配置文件中
    except Exception as e:
        print ("连接%s:%s时报错，请查看日志%s" % (data['ip'],data['port'],logfile),log.error(str(e)),'\n')

# def format_dict(ret):
#     if isinstance(ret,dict):
#         for k,v in ret.items():
#             fmat_v=str(v).replace("\n", "<br>")
#             ret[k]=fmat_v
#         return ret
#     else:
#         return None


def replace_clone_file(center_path,dest_path):
    '''
        动态修改git_clone_except脚本，比如项目路径，master用户名与密码等，分别对应的路径及git命令（可以通过前端传入）
        user,pwd,host均为中间库机器所在的IP，用户，密码
        center_path为中间库对应的项目路径 
        dest_path为客户机也就是项目集群每个单机中的项目实际路径
        修改文件中的有指定关键字的行
        可以先将文件读入列表中，利用列表的下标插入文本，之后再重新写入文件。但是弊端是，如果文件量太大列表的性能可能不是很高。
    '''
    PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    confile = os.path.join(PROJECT_DIR, 'salt_api\shell\git\git_clone_except.sh')
    
    ip=read_config('salt_master_host')['ip']
    port=read_config('salt_master_host')['port']
    username=read_config('salt_master_host')['username']
    password=read_config('salt_master_host')['password']
    new_line=[]
    try:
        with open(confile,"r",encoding="utf-8") as f:
            lines = f.readlines() 
            for line in lines:
                new_line.append(line)
        print("x",[x for x in new_line])
        #写的方式打开文件
        new_line[1]='user=%s\n'%(username)
        new_line[2]='pwd=%s\n'%(password)
        new_line[3]='host=%s\n'%(ip)
        print("git_project_center",center_path)
        new_line[4]='center_path=%s\n'%(center_path)
        new_line=''.join(new_line)
        with open(confile,"w",encoding="utf-8") as f_w:
            f_w.write(new_line)
        return True
    except Exception as e:
        log.error('replace_clone_file动态写入配置文件出错'+str(e))


def replace_git_view_file(dest,num):
    '''
        动态生成sls，执行git log -num,num值从前台取得,dest为目录，num为数值
    '''
    PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    confile = os.path.join(PROJECT_DIR, 'salt_api\sls\git\git_view_version.sls')
    new_line=[]
    try:
        with open(confile,"r",encoding="utf-8") as f:
            lines = f.readlines() 
            for line in lines:
                new_line.append(line)
        print("x",[x for x in new_line])
        new_line[2]='  - cwd: %s\n'%(dest)
        new_line[3]='  - name: git log --stat -%s --abbrev-commit --graph --decorate\n'%(str(num))
        new_line=''.join(new_line)
        with open(confile,"w",encoding="utf-8") as f_w:
            f_w.write(new_line)
        return True
    except Exception as e:
        log.error('replace_view_clone_file动态写入配置文件出错'+str(e))
    return None


def replace_git_order_file(dest,cmd):
    '''
    dest为集群中项目所对应的路径,如：/soft/EC_MY
    cmd,如git pull
    '''
    PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    confile = os.path.join(PROJECT_DIR, 'salt_api\shell\git\git_order.sh')
    
    ip=read_config('salt_master_host')['ip']
    port=read_config('salt_master_host')['port']
    username=read_config('salt_master_host')['username']
    password=read_config('salt_master_host')['password']
    new_line=[]
    try:
        with open(confile,"r",encoding="utf-8") as f:
            lines = f.readlines() 
            for line in lines:
                new_line.append(line)
        print("x",[x for x in new_line])
        #写的方式打开文件
        new_line[1]='user=%s\n'%(username)
        new_line[2]='pwd=%s\n'%(password)
        new_line[3]='dest_path=%s\n'%(dest)
        print("list(cmd)",type(cmd),cmd[3:])
        new_line[4]="option='git --no-pager %s'\n"%(cmd[3:])
        print("new_line[4]",new_line[4])
        new_line=''.join(new_line)
        with open(confile,"w",encoding="utf-8") as f_w:
            f_w.write(new_line)
        return True
    except Exception as e:
        log.error('replace_clone_file动态写入配置文件出错'+str(e))
    
def get_file_name(file_path):
    '''
    取一个路径中的文件名称与后缀名
    extension为后缀名
    '''
    file={}
    (filepath,tempfilename) = os.path.split(file_path);
    (shotname,extension) = os.path.splitext(tempfilename);
    file['filename']=shotname
    file['extension']=extension
    return file
#上传文件
def upload_file(file_absolute_path):
    """向salt_master服务器上传单个文件 
    """  
    
    ip=read_config('salt_master_host')['ip']
    port=read_config('salt_master_host')['port']
    username=read_config('salt_master_host')['username']
    password=read_config('salt_master_host')['password']
    #服务器上的目标文件
    file_name=os.path.basename(file_absolute_path)
    print("file_name",file_name)
    
    remote_file_path=read_config('salt_api_info')['file_roots']+file_name
    #上传前先删除之前的同名的文件
    cmd='cd %s && rm -f %s'%(read_config('salt_api_info')['file_roots'],file_name)
    ssh_connect_command(cmd)
    print("remote_file_path",remote_file_path)
    try:
        paramiko.util.log_to_file(logfile)  
        trans = paramiko.Transport((ip, int(port)))  
        trans.connect(username=username, password=password)  
        sftp = paramiko.SFTPClient.from_transport(trans)  
        sftp.put(file_absolute_path, remote_file_path)
    except Exception as e:
        print (log.error('upload_file'+str(e)))
    finally:
        trans.close()  

def replace_dict_value(ret,key,replace_key):
    '''
        将一个dict中的value替换成指定字符串换成另外的一个
    '''
    if isinstance(ret,dict):
        for k,v in ret.items():
            fmat_v=str(v).replace(key, replace_key)
            ret[k]=fmat_v
        return ret
    else:
        return None
    
def multiple_replace(text, adict):  
     rx = re.compile('|'.join(map(re.escape, adict)))  
     def one_xlat(match):  
           return adict[match.group(0)]  
     return rx.sub(one_xlat, text) 
 
def find_err(error_list,dict_result):
    '''
    根据提供的err_list关键字，来区分执行结果是否成功
    error_list=['False','error','No minions matched']
    
    dict_result=[{'172.17.39.208_windows10_app': {'retcode': 0, 'stderr': '', 'pid': 13452, 'stdout': ''}, '192.168.174.133_web1': {'retcode': 0, 'stderr': '', 'pid': 50078, 'stdout': "Loaded plugins: fastestmirror, langpacks\nLoading mirror speeds from cached hostfile\nPackage expect-5.45-12.el7.x86_64 already installed and latest version\nNothing to do\nspawn git clone root@192.168.216.128:/soft/projects/EC_MY\r\nCloning into 'EC_MY'...\r\nroot@192.168.216.128's password: \r\nwarning: You appear to have cloned an empty repository."}}]
    dict_result={'172.17.39.208_windows10_app': {'retcode': 0, 'stderr': '', 'pid': 13452, 'stdout': ''}, '192.168.174.133_web1': {'retcode': 0, 'stderr': '', 'pid': 50078, 'stdout': "Loaded plugins: fastestmirror, langpacks\nLoading mirror speeds from cached hostfile\nPackage expect-5.45-12.el7.x86_64 already installed and latest version\nNothing to do\nspawn git clone root@192.168.216.128:/soft/projects/EC_MY\r\nCloning into 'EC_MY'...\r\nroot@192.168.216.128's password: \r\nwarning: You appear to have cloned an empty repository."}}
    '''
    result_failed={}
    result_scuess={}
    result=format_result(dict_result)
    for k1,v1 in result.items():
        for v2 in error_list:
            #判断error_list中的串是否在result_list串中出现
            #grains.items成功的命令中有出现:False，需要将这种情况
            if str(v1).find(v2)==-1:#等于-1说明没找到
                pass
            else:
                #先将找到了的找出，找到了就说明是有问题的
                print("找到错误",v1,v2)
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
        print(k,type(v),v)
        result_failed[k]='ERROR:'+str(replace_dict_value(v,'\r\n','<br>'))
    for k, v in result_scuess.items():
        print(k,type(v),v)
        result_failed[k]=replace_dict_value(v,'\r\n','<br>')
    result_all=dict(result_scuess,**result_failed)
    print("result_all",type(result_all),result_all)
    return result_all

def get_salt_stdout(ret):
    '''
    获取salt执行脚本或是sls结果后的stdout结果部分,
    如果stdout为空则获取Comment字段，通常stdout为空表示是结果执行出错了。
    '''
    dict_fail={}
    dict_success={}
    for k,v in ret.items():
        for i,j in v.items():
            print("i","j",i,j)
            if str(i).find('stdout')>=0:
                dict_success[k]=j
'''
根据request获取用户名，用户ID，登录时间等信息
'''
def get_user_info(user_name): 
    data={}
    ret = User.objects.filter(username=user_name)
    for item in ret:
        data['userid']=item.id
        data['last_login']=json.dumps(item.last_login, cls=DateEncoder)
        data['user_name']=item.username
    return data
#处理时间json,
#TypeError: datetime.datetime(2017, 8, 31, 10, 8, 19) is not JSON serializable
'''
print json.dumps(dataMap, cls=DateEncoder)  
'''
class DateEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj, datetime.datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S')  
        elif isinstance(obj, date):  
            return obj.strftime("%Y-%m-%d")  
        else:  
            return json.JSONEncoder.default(self, obj)
    

        
if __name__ == '__main__':
    #print(rsync_file('172.17.39.208_windows10_app','salt://temp/1.txt','D:/1012/1.txt'))
    a={'192.168.174.133_web1': 'Loaded plugins: fastestmirror, langpacks\nLoading mirror speeds from cached hostfile\nNo package sshd available.\nResolving Dependencies\n--> Running transaction check\n---> Package httpd.x86_64 0:2.4.6-67.el7.centos.6 will be installed\n--> Processing Dependency: httpd-tools = 2.4.6-67.el7.centos.6 for package: httpd-2.4.6-67.el7.centos.6.x86_64\n--> Processing Dependency: /etc/mime.types for package: httpd-2.4.6-67.el7.centos.6.x86_64\n--> Processing Dependency: libaprutil-1.so.0()(64bit) for package: httpd-2.4.6-67.el7.centos.6.x86_64\n--> Processing Dependency: libapr-1.so.0()(64bit) for package: httpd-2.4.6-67.el7.centos.6.x86_64\n--> Processing Dependency: /etc/mime.types for package: httpd-2.4.6-67.el7.centos.6.x86_64\n--> Finished Dependency Resolution\nError: Package: httpd-2.4.6-67.el7.centos.6.x86_64 (base)\n           Requires: libaprutil-1.so.0()(64bit)\nError: Package: httpd-2.4.6-67.el7.centos.6.x86_64 (base)\n           Requires: httpd-tools = 2.4.6-67.el7.centos.6\nError: Package: httpd-2.4.6-67.el7.centos.6.x86_64 (base)\n           Requires: libapr-1.so.0()(64bit)\nError: Package: httpd-2.4.6-67.el7.centos.6.x86_64 (base)\n           Requires: /etc/mime.types\n You could try using --skip-broken to work around the problem\n You could try running: rpm -Va --nofiles --nodigest'}
    b={'192.168.174.133_web1': '/etc/yum.repos.d/local_init.repo'}
    #data = read_config('git')
    c={'192.168.174.133_web1': ['The function "state.sls" is running as PID 11977 and was started at 2017, Dec 17 19:22:20.321620 with jid 20171217192220321620'], '172.17.39.208_windows10_app': ["No matching salt environment for environment 'windows10_app' found", "No matching sls found for '172.17.39.208_windows10_app' in env 'windows10_app'"]}
    #print(replace_file_line('/soft/EC_MY','git log -p'))
    print("def replace_clone_file(center_path,dest_path):",replace_clone_file('/soft/projects/EC_MY','/www/EC_MY'))
    dic={'192.168.174.133_web1': {'retcode': 0, 'stderr': '', 'pid': 50078, 'stdout': "Loaded plugins: fastestmirror, langpacks\nLoading mirror speeds from cached hostfile\nPackage expect-5.45-12.el7.x86_64 already installed and latest version\nNothing to do\nspawn git clone root@192.168.216.128:/soft/projects/EC_MY\r\nCloning into 'EC_MY'...\r\nroot@192.168.216.128's password: \r\nwarning: You appear to have cloned an empty repository."}}
    dica={'172.17.39.208_windows10_app': {'stderr': '', 'pid': 11000, 'retcode': 0, 'stdout': ''}, '192.168.174.133_web1': {'stderr': '', 'pid': 65206, 'retcode': 0, 'stdout': "Loaded plugins: fastestmirror, langpacks\nLoading mirror speeds from cached hostfile\nPackage expect-5.45-12.el7.x86_64 already installed and latest version\nNothing to do\nspawn git clone root@192.168.216.128:/soft/projects/EC_MY\r\nfatal: destination path 'EC_MY' already exists and is not an empty directory."}}
    error_list=['No such file',"'stdout': ''",'is not recognized','could not']
    find_err(error_list,dica)
    ss = {'192.168.174.133_web1': {'pid': '116938', 'stderr': '', 'retcode': '0', 'stdout': "spawn git --no-pager log\r<br>commit 57348bb8fccb5bcc6d7364d4a32d2527b20835b3\r<br>Author: unknown <ning.lin@LGZB0050.Trendy-global.com>\r<br>Date:   Tue Dec 26 12:19:18 2017 +0800\r<br>\r<br>    aa\r<br>\r<br>commit 6a23c5ecaf4e423b5914a6b0dbd6606e5672f553\r<br>Author: unknown <ning.lin@LGZB0050.Trendy-global.com>\r<br>Date:   Tue Dec 26 11:56:36 2017 +0800\r<br>\r<br>    aa\r<br>\r<br>commit 7dc4906c938a0ec1c3a0b0e39df3107ac84cae88\r<br>Merge: 4a1c4e8 0ec5fef\r<br>Author: unknown <ning.lin@LGZB0050.Trendy-global.com>\r<br>Date:   Tue Dec 26 10:38:36 2017 +0800\r<br>\r<br>    Merge branch 'master' of 192.168.216.128:/soft/projects/EC_MY\r<br>\r<br>commit 4a1c4e8c306ef38bc7124744b5e4e3778ff6eea2\r<br>Author: unknown <ning.lin@LGZB0050.Trendy-global.com>\r<br>Date:   Tue Dec 26 10:36:16 2017 +0800\r<br>\r<br>    aaa\r<br>\r<br>commit 0ec5fef772831c5fb94ddeed15ffeca10266d25a\r<br>Merge: b0ddb7e 0a4bf09\r<br>Author: Your Name <you@example.com>\r<br>Date:   Mon Dec 25 18:34:58 2017 -0800\r<br>\r<br>    Merge branch 'master' of 192.168.216.128:/soft/projects/EC_MY\r<br>\r<br>commit 0a4bf09643576832faed4c250f171e2227020e51\r<br>Author: unknown <ning.lin@LGZB0050.Trendy-global.com>\r<br>Date:   Tue Dec 26 10:34:29 2017 +0800\r<br>\r<br>    delete 7.txt\r<br>\r<br>commit b0ddb7e2dadf1287e5eae0f26dd6f61c4a08f3aa\r<br>Merge: f0b8844 02a17dc\r<br>Author: Your Name <you@example.com>\r<br>Date:   Mon Dec 25 18:33:23 2017 -0800\r<br>\r<br>    Merge branch 'master' of 192.168.216.128:/soft/projects/EC_MY\r<br>\r<br>commit 02a17dc46c2b7f7ea9a9c3869d71b83a12d74933\r<br>Author: unknown <ning.lin@LGZB0050.Trendy-global.com>\r<br>Date:   Mon Dec 25 14:26:32 2017 +0800\r<br>\r<br>    7.txt\r<br>\r<br>commit 09f98598c23b71571d9caecb126b3fb9766d0918\r<br>Author: unknown <ning.lin@LGZB0050.Trendy-global.com>\r<br>Date:   Mon Dec 25 14:26:09 2017 +0800\r<br>\r<br>    6.txt\r<br>\r<br>commit e8124aec1fed7117d9a833a353cc5f157a832b66\r<br>Author: unknown <ning.lin@LGZB0050.Trendy-global.com>\r<br>Date:   Mon Dec 25 14:25:52 2017 +0800\r<br>\r<br>    5\r<br>\r<br>commit 559dfb044fe325358d4fa648db86a014863e52b5\r<br>Author: unknown <ning.lin@LGZB0050.Trendy-global.com>\r<br>Date:   Mon Dec 25 14:25:31 2017 +0800\r<br>\r<br>    4.txt\r<br>\r<br>commit f0b8844fcfbabd1b720bc81d9a6bf3575fda36d7\r<br>Author: Your Name <you@example.com>\r<br>Date:   Thu Dec 21 01:00:30 2017 -0800\r<br>\r<br>    del 1.txt\r<br>\r<br>commit ede67f4956a4cc6dc476ca45db22afbbfdb0f218\r<br>Author: Your Name <you@example.com>\r<br>Date:   Thu Dec 21 00:59:06 2017 -0800\r<br>\r<br>    add 1.txt\r<br>\r<br>commit cfb3b5b9d25558de2e9dde71e8358c66c3888d15\r<br>Author: unknown <ning.lin@LGZB0050.Trendy-global.com>\r<br>Date:   Thu Dec 21 11:36:24 2017 +0800\r<br>\r<br>    addall"}, '172.17.39.208_windows10_app': "ERROR:{'pid': '2280', 'stderr': '', 'retcode': '0', 'stdout': ''}"}
    print("ss",type(ss),ss)
    for k,v in ss.items():
        for i,j in v.items():
            print(i,j)
#     print("text",ssh_connect_command('free -m'))
#     print("ssss",dict(format_dict(b),**a))