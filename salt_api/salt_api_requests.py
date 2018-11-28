# -*- coding: utf-8 -*-
#
from collections import OrderedDict
import configparser
import json
from multiprocessing import Pool
import os
import re
import time
import urllib.request

import requests



#一些工具方法
 #从配置文件获取api接口信息url,username,password
def get_api():
    #D:\Program Files\Python_Workspace\test_ui\salt_api\salt_api.conf
    config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    confile = os.path.join(config_dir, 'config_dir\salt_api.conf')
    #confile ='E:\\soft\python3.4\\workspace\\test_ui\\salt_api\\salt_api.conf'
    #confile ='E:\\soft\python3.4\\workspace\\test_ui\\salt_api\\salt_api.conf' 
#     data = read_config('salt_api_info')  
#     print("data",data)
#     return data
    data = {}
    config = configparser.ConfigParser()
    try:  
        with open(confile,'r',encoding='utf-8') as confile:  
            config.readfp(confile)  
        #config.read(filename)  
            for (key, value) in config.items('salt_api_info'):  
                data[key] = value
            return data      
    except Exception as e:  
        print ("Open file error." ,str(e)) 
        
#多线程执行方法


#获取api接口对象
def get_salt_api():
    data = get_api()
    salt_api=SaltAPI(data['url'],data['username'],data['password'])
    return salt_api

#将list的minion_id转成('a,b,c,d')这种格式
def format_minionIDs(minion_ids):
    if isinstance(minion_ids, set) or isinstance(minion_ids, tuple):
        minion_ids=list(minion_ids)
    for_minino_ids=""
    for i in minion_ids:
        #处理最后的特殊的一个
        if(i==minion_ids[-1]):
            for_minino_ids +=i+""
            break
        for_minino_ids +=i+","
    print("for_minino_ids",type(for_minino_ids),for_minino_ids)
    return for_minino_ids
class SaltAPI:
    """
    定义salt api接口的类
    初始化获得token
    """
    def __init__(self, url,username,password):
        self.url = url
        self.username = username
        self.password = password
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Content-type": "application/json"
            # "Content-type": "application/x-yaml"
        }
        self.params = {'client': 'local', 'fun': '', 'tgt': ''}
        # self.params = {'client': 'local', 'fun': '', 'tgt': '', 'arg': ''}
        self.login_url = url + "login"
        self.login_params = {'username': self.username, 'password': self.password, 'eauth': 'pam'}
        self.token = self.get_data(self.login_url, self.login_params)['token']
        print("token",self.token)
        self.headers['X-Auth-Token'] = self.token
        
    #这里是定制请求头
    def get_data(self, url, params):
        send_data = json.dumps(params)
        request = requests.post(url, data=send_data, headers=self.headers, verify=False)
        print("request",request)
        response=json.loads(request.text)
        result = dict(response)
        print("result",result)
        return result['return'][0]
        #response = request.json()
        
    
    #这里是为处理传递的多参数问题
    def send_request(self,params):
        url = self.url + '/'
        tokenid = self.token
        headers = {'X-Auth-Token': tokenid}
        data = urllib.parse.urlencode(params)
        #将arg参数后面带数字的全部替换成arg
        data, num = re.subn("arg\d", 'arg', data)
        data = data.encode('utf-8')
        req = urllib.request.Request(url, data, headers)
        opener = urllib.request.urlopen(req)
        resData = opener.read()
        resData = json.loads(resData.decode())
        return resData
    
    def salt_command_two_args(self,serverlist,fun,spath, dpath):
        params = OrderedDict([('client', 'local'), ('fun', fun), ('arg1', spath), ('arg2', dpath), ('tgt', serverlist),('expr_form', 'list')])
        result = self.send_request(params)
        return result['return']
    
    def salt_command_many_args(self,serverlist,fun,**args):
        '''这样调用salt_command_many_args(format_minionIDs(a),'file.file_exists',arg1='d:/1012/temp/1.txt'))
        '''
        from Mytoolkits import format_result
        data=[]
        print("args",args)
        if len(args)==0:
            print("len(args)",len(args))
            print("无")
            params = OrderedDict([('client', 'local'), ('fun', fun),('tgt', serverlist),('expr_form', 'list')])
        else:
            print("len(args)",len(args))
            i=0
            for k,v in args.items():
                i+=1
                print(k,v)
                a={'k'+str(i):v}
                par=(k,v)
                data.append(par)
            print("par",par)
            params = OrderedDict([('client', 'local'), ('fun', fun),('tgt', serverlist),('expr_form', 'list')]+data)
            print("params",params)
        result = self.send_request(params)
        return result['return']
    
    
    def salt_alive(self,tgt):
        '''
        salt主机存活检测
        '''

        params = {'client': 'local', 'tgt': tgt, 'fun': 'test.ping','expr_form':'list'}
        result = self.get_data(self.url, params)
        return result

    def salt_command(self, tgt, method, arg=None):
        """远程执行命令，相当于salt 'client1' cmd.run 'free -m'
            加上'expr_form':'list'参数可以使用('a,b,c')这种形式来批量执行
        """
        if arg:
            params = {'client': 'local', 'fun': method, 'tgt': tgt, 'arg': arg,'expr_form':'list'}
        else:
            params = {'client': 'local', 'fun': method, 'tgt': tgt,'expr_form':'list'}
        result = self.get_data(self.url, params)
        return result
    
    def salt_async_command(self, tgt, method, arg=None):  # 异步执行salt命令，根据jid查看执行结果
        '''远程异步执行命令'''
        if arg:
            params = {'client': 'local_async', 'fun': method, 'tgt': tgt, 'arg': arg}
        else:
            params = {'client': 'local_async', 'fun': method, 'tgt': tgt}
        jid = self.get_data(self.url, params)['jid']
        print("jid",jid)
        return jid
    
#执行runner模块
    def look_jid(self, jid):  # 根据异步执行命令返回的jid查看事件结果
        params = {'client': 'runner', 'fun': 'jobs.lookup_jid', 'jid': jid}
        result = self.get_data(self.url, params)
        return result
    
    def minion_status(self):
        params = {'client': 'runner', 'fun': 'manage.status'}
        result = self.get_data(self.url,params)
        return result
    
    def local_run(self,method, arg=None):
        if arg:
            params = {'client': 'runner', 'fun': method, 'arg': arg,'expr_form':'list'}
        else:
            params = {'client': 'runner', 'fun': method,'expr_form':'list'}
        result = self.get_data(self.url, params)
        print("result",result)
        return result
    
    def salt_running_jobs(self):
        '''
                             获取运行中的任务
        '''
        params = {'client':'runner', 'fun':'jobs.active'}
        result = self.get_data(self.url,params)
        return result['return'][0]
    
    def salt_runner(self,jid):
        '''
                        通过jid获取执行结果
        '''
        params = {'client':'runner', 'fun':'jobs.lookup_jid', 'jid': jid}
        result = self.get_data(self.url,params)
        return result['return'][0]
#执行wheel模块
    def get_all_keys(self):
        '''
            获取已认证的主机
        '''
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        result = self.get_data(self.url,params)
        print(result)
        return result['data']['return']#['minions']
    #{'minions': ['172.17.39.208_windows10_app', '192.168.174.133_web1'], 'minions_rejected': [], 'minions_pre': ['docker_images_minion1', 'docker_images_minion2', 'docker_images_minion3', 'docker_images_minion4'],
    # 'local': ['master.pem', 'master.pub'], 'minions_denied': []}
    def delete_key(self,node_name):
        '''
                拒绝salt主机
        '''
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': node_name}
        result = self.get_data(self.url,params)
        ret = result['data']['success']
        return ret
    
    def reject_key(self,node_name):
        '''
                拒绝salt主机
        '''
        params = {'client': 'wheel', 'fun': 'key.reject', 'match': node_name}
        result = self.get_data(self.url,params)
        ret = result['data']['success']
        return ret
    def accept_key(self,node_name):
        '''
                接受salt主机
        '''

        params = {'client': 'wheel', 'fun': 'key.accept', 'match': node_name}
        result = self.get_data(self.url,params)
        ret = result['data']['success']
        #{'tag': 'salt/wheel/20171106193734318141', 'data': {'tag': 'salt/wheel/20171106193734318141', 'user': 'saltapi', '_stamp': '2017-11-07T03:37:34.332185', 'success': True, 'jid': '20171106193734318141', 'return': {'minions': ['172.17.39.208_windows10_app']}, 'fun': 'wheel.key.accept'}}
        return ret
#file模块
    def salt_file_replace(self, tgt,file, arg1,arg2):
        """远程执行命令，相当于salt 'client1' cmd.run 'free -m'
            加上'expr_form':'list'参数可以使用('a,b,c')这种形式来批量执行
        """
        #params = {'client': 'local', 'fun': 'file.replace', 'tgt': tgt,'arg1':(file,arg1,arg2),'expr_form':'list'}
        params=[('client', 'local'), ('fun', 'file.replace'),('tgt', tgt),("arg", [file,arg1,arg2]),('expr_form', 'list')]
#         params ={
#         "client": "local",
#         "tgt": tgt,
#         "fun": "file.replace",
#         "arg": [file,arg1,arg2],
#     }
        params = {'client': 'local', 'fun': 'file.replace', 'tgt': tgt, 'arg': file,'expr_form':'list'}
        params = OrderedDict([('client', 'local'), ('fun', 'file.replace'), ('arg1', file), ('arg2', arg1),('arg3', arg2),('tgt', tgt),('expr_form', 'list')])
        print("params",params)
        result = self.get_data(self.url, params)
        return result    
    #执行sls
    def server(self,tgt,sls_name):
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': sls_name,'expr_form':'list'}
        result = self.get_data(self.url, params)
        print("result",result)
        return result
    #执行sls
    def server_async(self,tgt,sls_name):
        '''异步sls返回jid'''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': sls_name,'expr_form':'list'}
        result = self.get_data(self.url, params)
        print("result",result)
        return result

def fun_pool(fun,n):
    '''
    多进程执行方法
    多进程
        threads=[]
    for i in range(20):
        t=threading.Thread(target=fun)
        threads.append(t)
    for i in range(0,20):
        threads[i].start()
    '''
    #进程池
    pool=Pool(n)#创建n个进程数量的进程池
    res_l=[]
    for i in range(n):
        res=pool.apply(fun,args=(i,)) #同步运行,阻塞、直到本次任务执行完毕拿到res
        res_l.append(res)
    print(res_l)
    return res_l
    
def fun_pool_async(fun,n):
    '''
    异步执行：非阻塞
    '''
    #进程池
    pool=Pool(n)#创建n个进程数量的进程池
    res_l=[]
    for i in range(n):
        res=pool.apply_async(fun,args=("*",'test.ping')) #异步执行：非阻塞
        res_l.append(res)
    #异步apply_async用法：如果使用异步提交的任务，主进程需要使用jion，等待进程池内任务都处理完，然后可以用get收集结果，否则，主进程结束，进程池可能还没来得及执行，也就跟着一起结束了
    pool.close()
    pool.join()
    for res in res_l:
        print(res.get()) #使用get来获取apply_aync的结果,如果是apply,则没有get方法,因为apply是同步执行,立刻获取结果,也根本无需get
    return res_l
    
    
def main():
    salt = get_salt_api()
    print("salt",type(salt),salt)
#     salt = get_salt_api()
#     salt_client = '*'
#     salt_test = 'test.ping'
#     salt_t = 'salt-key -L'
#     salt_method = 'cmd.run'
#     salt_params = 'free -m'
#     a=['172.17.39.208_windows10_app', 'aaa_windows10_app','192.168.174.133_web1']
#     
#     c=('172.17.39.208_windows10_app,windows10_app,172.17.39.96_web1_centos7_2')
#     d=['192.168.160.128_oracledb','192.168.160.128_oracledb_Exit','windows10_app_Exit','windows10_app']
#     b=format_minionIDs(a)
#     print("b",type(b),b)
#     print("c",type(c),c)
    # print salt.salt_command(salt_client, salt_method, salt_params)
    # 下面只是为了打印结果好看点
#     result1 = salt.salt_command(salt_client, salt_test)
#     for i in result1.keys():
#         print (i, ': ', result1[i])
#     result2 = salt.salt_command(salt_client, salt_method, salt_params)
#     for i in result2.keys():
#         print (i)
#         print (result2[i])
#     result3=salt.look_jid(salt.salt_async_command(salt_client,salt_method,salt_params))
#     for i in result3.keys():
#         print (i)
#         print (result3[i])
#     print("salt-key -L",salt.salt_async_command(salt_client,salt_t))
    
#     print("minion_status",salt.minion_status())
#     print("get_all_key",salt.get_all_keys())
    #print("salt_command",salt.rsync_file(('172.17.39.96_web1_centos7_2,172.17.39.208_windows10_app'),'cp.get_dir','salt://temp/','D:/1012/'))
    #print("salt_alive",salt.salt_alive("172.17.39.208_windows10_app"))
    #print(salt.salt_command_two_args(format_minionIDs(a),'cp.get_file','salt://local_init.repo', '/etc/yum.repos.d/local_init.repo'))
#     print("salt_command",salt.salt_command(format_minionIDs(a),'file.file_exists','d:/1012/temp/1.txt'))
#     print("salt_command_two_args",salt.salt_command_two_args(format_minionIDs(a),'git.add','/soft', '/soft'))
#     print("salt_command",salt.salt_command_many_args(format_minionIDs(a),'file.replace',arg1='d:/1012/temp/1.txt','sdf','AAAAA',backup='.bak',append_if_not_found='True'))
    #print("salt_file_replace方法",salt.salt_file_replace(format_minionIDs(a),'d:/1012/temp/1.txt','sdf','ss'))
    #salt '*' file.replace d:/1012/temp/1.txt pattern='sdf' repl='AAAAA'  backup='.bak' append_if_not_found='True'
    #print("salt_command_many_args方法",salt.salt_command_many_args(format_minionIDs(a),'test.ping'))
    #print("salt_command_many_args",salt.salt_command(format_minionIDs(a),'cmd.run','yum install -y nmon'))
    #min_ids=['192.168.174.133_web1']
#     print("获取keu",salt.get_all_keys() )
    #print("sls",salt.server_async(format_minionIDs(a),'ccc'))
    #print("aaa",salt.look_jid(20171217232508420845))
#     s=['cmd.run', 'yum remove -y nmon']
    #print("str(s)",str(s))
#     print("accept_key",salt.accept_key("172.17.39.208_wows10_app"))
if __name__ == '__main__':
    main()
#     a=['ip', '172.17.39.208', '172.17.39.96']
#     b={'ip', '172.17.39.208', '172.17.39.96'}
# #     print("type(a)",type(a))
#     print("sss",format_minionIDs(a))
#     dic = {'client': 'local', 'tgt': 'tgt', 'fun': 'fun', 'arg':'arg1','arg':'arg2',"aaa":['salt://soft/temp/1.txt','d:/1012/1.txt']}
#     print("dict",dic)
#     send_data = json.dumps(dic)
#     print("")
#     r= requests.post("http://httpbin.org/get", params=dic)
#     print(r.url)
    #client=local&fun=cp.get_dir&arg=salt%3A%2F%2Ftemp%2F&arg=D%3A%2F1012%2F&tgt=172.17.39.208_windows10_app'
    #http://httpbin.org/get?tgt=tgt&aaa=salt%3A%2F%2Fsoft%2Ftemp%2F1.txt&aaa=d%3A%2F1012%2F1.txt&arg=arg2&fun=fun&client=local