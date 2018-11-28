# -*- coding: utf-8 -*-
import configparser
import json
import os
import sys
import time
import urllib.parse
import urllib.request

import requests


 #从配置文件获取api接口信息url,username,password
def get_api():
    #D:\Program Files\Python_Workspace\test_ui\salt_api\salt_api.conf
    #confile ='D:\\Program Files\\Python_Workspace\\test_ui\\salt_api\\salt_api.conf'
    #confile ='E:\\soft\python3.4\\workspace\\test_ui\\salt_api\\salt_api.conf'
    #confile ='E:\\soft\python3.4\\workspace\\test_ui\\salt_api\\salt_api.conf' 
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
            for i in config.sections():  
                for (key, value) in config.items(i):  
                    data[key] = value
            return data      
    except Exception as e:  
        print ("Open file error." ,str(e)) 



class SaltAPI(object):
    #默认为空 tokenid
    __token_id = ''
    data = {}
    def __init__(self,url,username,password):
        self.__url = url.rstrip('/')
        self.__user = username
        self.__password = password
    def token_id(self):
        ''' user login and get token id
        curl -k https://ip地址:8080/login
        -H "Accept: application/x-yaml" -d username='用户名' -d password='密码' -d eauth='pam'
        '''
        #获取token_id的请求数据
        params = {'eauth': 'pam', 'username': self.__user,'password': self.__password}
        #将请求的类型转成例如
        #password=salt&eauth=pam&username=salt
        encode = urllib.parse.urlencode(params)
        #转成二进制
        obj = encode.encode()
        #将二进制数据交给postRequest函数处理
        content = self.postRequest(obj,prefix='/login')
        try:
            self.__token_id = content['return'][0]['token']
        except KeyError:
                raise KeyError
    def postRequest(self,obj,prefix="/"):
        #将url和后面的地址进行拼接
        url = self.__url + prefix
        # headers = {'X-Auth-Token': self.__token_id,'Accept':'application/json'}
        headers = {'X-Auth-Token': self.__token_id}
        #提交请求
        req = urllib.request.Request(url,obj,headers)
        response = urllib.request.urlopen(req)
        #获取结果
        request = response.read()
        #转成字典
        content = json.loads(str(request,encoding='utf-8'))
        return content
    def all_key(self):
        '''
        获取所有的minion_key
        '''
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        self.token_id()
        content = self.postRequest(obj)
        # print(content)
        # 取出认证已经通过的
        minions = content['return'][0]['data']['return']['minions']
        #print('已认证',minions)
        # 取出未通过认证的
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        # print('未认证',minions_pre)
        return minions,minions_pre

    #接受认证方法
    def accept_key(self,node_name):
        '''
        如果你想认证某个主机 那么调用此方法
        '''
        params = {'client': 'wheel', 'fun': 'key.accept', 'match':node_name}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret
    #删除认证方法
    def delete_key(self,node_name):
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': node_name}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret
    def remote_execution_noargs(self,tgt,fun):
        ''' tgt是主机 fun是方法（执行命令,命令无参数的）
            写上模块名 返回 可以用来调用基本的资产
            例如 curl -k https://ip地址:8080/ \
        >      -H "Accept: application/x-yaml" \
        >      -H "X-Auth-Token:b50e90485615309de0d83132cece2906f6193e43" \
        >      -d client='local' \
        >      -d tgt='*' \
        >      -d fun='test.ping'  要执行的模块
        return:
        - iZ28r91y66hZ: true
          node2.minion: true
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        self.token_id()
        content = self.postRequest(obj)
        print("remote_execution_module",content)
        ret = content['return'][0]
        return ret
    def remote_execution_func(self,tgt,fun,arg):
        '''
        #   curl -k https://ip地址:8080 \
        -H "Accept: application/x-yaml"
        -H "X-Auth-Token:b50e90485615309de0d83132cece2906f6193e43"
        -d client='local'
        -d tgt='*'            tgt是minion名称 默认匹配所有  如果加上 那么匹配固定主机名  这个函数可以用来获取硬件信息
        -d fun='grains.item'  使用grains.item模块
        -d arg='id'           查到主机的minionid
        return:
        - iZ28r91y66hZ:
            id: iZ28r91y66hZ
          node2.minion:
            id: node2.minion
        带参数
         curl -k http://115.29.51.8:8080/ -H "Accept: application/x-yaml"
          -H "X-Auth-Token: e5c2aa981109330ab9dacf238fb0ea0507d204cb"
          -d client='local' -d tgt='*'  -d fun='saltutil.sync_all'
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret
        #基于分组来执行
    def target_remote_execution(self,tgt,fun,arg):
        ''' 根据分组来执行 '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'nodegroup'}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        self.token_id()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid

    def server(self,tgt,arg):
        '''
        执行sls文件
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        self.token_id()
        content = self.postRequest(obj)
        return content
    def server_async(self,tgt,arg):
        '''异步sls '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        self.token_id()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid
    def server_group(self,tgt,arg):
        ''' 分组进行sls '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'nodegroup'}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        self.token_id()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid
    
    
    def asyncMasterToMinion(self, tgt, fun, arg):
        '''
            异步执行，当target为部分minion时，Master操作Minion；
        :param target: 目标服务器ID组成的字符串；
        :param fun: 使用的salt模块，如state.sls, cmd.run
        :param arg: 传入的命令或sls文件
        :return: jid字符串
        salt执行命令有时候会有超时的问题，就是命令下发下去了，部分主机没有返回信息，
        这时候就很难判断命令或任务是否执行成功。因此，salt提供异步执行的功能，发出命令后立即返回一个jid。
        然后我们就可以根据这个jid来查询任务是否执行成功。
        salt-run jobs.lookup_jid 20150915151813222323
        '''
        if tgt == '*':
            params = {'client': 'local_async', 'tgt': tgt, 'fun': fun, 'arg': arg}
        else:
            params = {'client': 'local_async', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'list'}
        '''
        以前，一直用compound参数，
        现在，想要并行执行salt命令，那list就派上用场了。
        同时传多个主机列表，用逗号分隔，然后，用list参数传，就好。
        # curl -k https://10.2.74.41:8000/      
        -H "Accept: application/x-yaml"      
        -H "X-Auth-Token: 7efbcb3dac9d99c5504b5543f96c06f9bd30e1bb"      
        -d client='local'      
        -d tgt="cn29-1.4.174.127","c91-1.5.174.57" -d expr_form='list' -d fun='test.ping'
        '''
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        #print("obj",obj)
        content = self.postRequest(obj)
        #print("asyncMasterToMinioncontent",content)
        jid = content['return'][0]['jid']
        return jid

    def masterToMinionContent(self, tgt, fun, arg):
        '''
            Master控制Minion，返回的结果是内容，不是jid；
            目标参数tgt是一个如下格式的字符串：'*' 或 'zhaogb-201, zhaogb-202, zhaogb-203, ...'
        '''
        if tgt == '*':
            params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
        else:
            params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'list'}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        content = self.postRequest(obj)
        print("masterToMinionContent",content)
        result = content['return'][0]
        return result

    def allMinionKeys(self):
        '''
        返回所有Minion keys；
        分别为 已接受、待接受、已拒绝；
        :return: [u'local', u'minions_rejected', u'minions_denied', u'minions_pre', u'minions']
        '''
        '''
        external_auth:
            pam:
                saltapi:
                  - .*
                  - '@wheel'
        需要修改master的配置对saltapi用户wheel模块进行授权,wheel未授权会报错
        urllib2.HTTPError: HTTP Error 401: Unauthorized
        '''
        params = {'client':'wheel', 'fun':'key.list_all'}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        #print("obj",obj)
        content = self.postRequest(obj)
        #print("allMinionKeyscontent",type(content),content)
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        minions_rej = content['return'][0]['data']['return']['minions_rejected']
        return minions, minions_pre, minions_rej

    def actionKyes(self, keystrings, action):
        '''
        对Minion keys 进行指定处理；
        :param keystrings: 将要处理的minion id字符串；
        :param action: 将要进行的处理，如接受、拒绝、删除；accept/reject/delect
        :return:
        {"return": [{"tag": "salt/wheel/20160322171740805129", "data": {"jid": "20160322171740805129", "return": {}, "success": true, "_stamp": "2016-03-22T09:17:40.899757", "tag": "salt/wheel/20160322171740805129", "user": "zhaogb", "fun": "wheel.key.delete"}}]}
        '''
        func = 'key.' + action
        params = {'client': 'wheel', 'fun': func, 'match': keystrings}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        #print("actionKyes",obj)
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def acceptKeys(self, keystrings):
        '''
        接受Minion发过来的key；
        :return:
        '''
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': keystrings}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def deleteKeys(self, keystrings):
        '''
        删除Minion keys；
        :param node_name:
        :return:
        '''
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': keystrings}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret
    
#     def SaltJob(self,jid=''):
#         if jid:
#             prefix = '/jobs/'+jid
#         else:
#             prefix = '/jobs'
#         res = self.postRequest(None,prefix)
#         # print res
#         return res
    def file_copy(self,tgt,fun,arg1,arg2,expr_form):
        '''
        文件上传、备份到minion、项目管理
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg1, 'expr_form': expr_form}
        # 拼接url参数
        params2 = {'arg':arg2}
        arg_add = urllib.parse.urlencode(params2)
        obj = urllib.parse.urlencode(params)
        print("arg_add",arg_add)
        obj = obj + '&' + arg_add
        print("obj",obj)
        encode = urllib.parse.urlencode(obj)
        obj = encode.encode()
        content = self.postRequest(obj)
        ret = content
        return ret
    
def findJob(minionids_set, jid):
    '''

    :return:
    '''
    target_list_to_str = ','.join(list(minionids_set))
    #log.debug('target_list: %s' % str(target_list_to_str))
    #如果作业已经完成，则无法找到该作业，因此该函数返回一个空字典，在CLI中如下所示：
    #my-minion:
    #----------
    fun = 'saltutil.find_job'
    diff_send_receive = []
    loop = True

    sapi = SaltAPI(
                url='http://192.168.174.128:9999/',
                username='saltapi',
                password='saltapi')

    while loop:
        counter = 0
        # log.debug('The loop variable')
        #log.debug('into loop start [common.views.findJob]')
        time.sleep(10)
        #返回所有的MinionID的执行结果
        find_job_result = sapi.masterToMinionContent(target_list_to_str, fun, jid)
        #log.debug('find_job_result: %s' % str(find_job_result))
        #得到执行的MinionID
        find_job_result_set = set(find_job_result.keys())
        #将另一个列表添加到本列表中,difference是取差集，a.difference(b),取a中有的，但在b中没有的
        #minionids_set是传入的集合，取与已执行的MinionID之后就是没能执行的MinionID了
        diff_send_receive.extend(list(minionids_set.difference(find_job_result_set)))
        find_job_result_value = find_job_result.values()
        for eachDict in find_job_result_value:
            if eachDict:
                print('The find job result is Dict, It is values list is Not null.')
                break
            else:
                counter += 1
        if counter == len(find_job_result_set):
            loop = False

    diff_send_receive_set = set(diff_send_receive)

    print("diff_send_receive_set",diff_send_receive_set)

    return diff_send_receive_set

def get_salt_api1():
    data = get_api()
    salt_api=SaltAPI(data['url'],data['username'],data['password'])
    return salt_api
if __name__=='__main__':
    data = get_api()
    saltapi = get_api()
#     sapi = SaltAPI(
#                 url='http://172.17.39.93:9999/',
#                 username='saltapi',
#                 password='saltapi')
    sapi=SaltAPI(data['url'],data['username'],data['password'])
    #sapi = SaltAPI();
#     print(sapi.remote_execution_noargs('windows10_app1','grains.items'))
#     print(sapi.asyncMasterToMinion('*', 'sys.list_modules', ''))
    print("salt_command",sapi.file_copy('172.17.39.208_windows10_app','cp.get_file','salt://soft/temp/1.txt','/tmp/1.txt','list'))
    #print(sapi.remote_execution_func('windows10_app','cmd.run', 'ssss'))
# #如果作业已经完成，则无法找到该作业，因此该函数返回一个空字典
#     print(sapi.masterToMinionContent('*','saltutil.find_job',20171009001703327645))
    #findJob(set(a), 20171008232629117734)
    #print(sapi.masterToMinionContent('*', 'grains.items', '20170921025003986650')
    #print(sapi.jobs_all('20171008211455284301'))
    a=['172.17.39.208_windows10_app', 'aaa_windows10_app','192.168.174.133_web1']
    print("sls",sapi.allMinionKeys())