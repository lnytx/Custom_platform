#!/usr/bin/env python
import urllib.request,urllib
import time
from urllib import parse
try:
    import json
except ImportError:
    import simplejson as json
class SaltAPI(object):
    __token_id = ''
    def __init__(self,url,username,password):
        self.__url = url.rstrip('/')
        self.__user = username
        self.__password = password
    def token_id(self):
        ''' user login and get token id '''
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        encode = urllib.parse.urlencode(params).encode(encoding='utf-8')
        print("encode",encode)
        #obj = urllib.parse.unquote(encode)
        obj=encode
        print("obj_token_id",type(obj),obj)
        content = self.postRequest(obj,prefix='/login')
        print("content",content)
        try:
            self.__token_id = content['return'][0]['token']
        except KeyError:
            raise KeyError
        
    def postRequest(self,obj,prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token':self.__token_id}
        req = urllib.request.Request(url, obj,headers)
        print("type req",type(req),req)
        opener = urllib.request.urlopen(req)
        #opener.read()只许出现一次，否则第二次是打印的为空
#         print("opener",opener.read().decode('UTF-8', 'ignore'))
        content = json.loads(opener.read().decode('utf-8', 'ignore'))
        return content
    
#     def postRequest(self,obj,prefix='/'):
#         url = self.__url + prefix
#         headers = {'X-Auth-Token'   : self.__token_id}
#         req = urllib2.Request(url, obj, headers)
#         opener = urllib2.urlopen(req)
#         content = json.loads(opener.read())
#         return content

    def list_all_key(self):
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        obj = urllib.parse.urlencode(params)
        self.token_id()
        print(type(obj))
        content = self.postRequest(bytes(obj,encoding='utf-8'))
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        return minions,minions_pre
    
    def delete_key(self,node_name):
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': node_name}
        obj = urllib.parse.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret
    def accept_key(self,node_name):
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': node_name}
        obj = urllib.parse.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret
    def remote_noarg_execution(self,tgt,fun):
        ''' Execute commands without parameters '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun}
        obj = urllib.parse.urlencode(params)
        print("obj",obj,type(obj))
        obj=bytes(obj,encoding='utf-8')
        self.token_id()
        content = self.postRequest(obj)
        print("content",content)
        #ret = content['return'][0]['monitor']['cpu_model']
        ret = content['return'][0]
        return ret
    def remote_execution(self,tgt,fun,arg):
        ''' Command execution with parameters '''        
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
        obj = urllib.parse.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0][tgt]
        return ret
    def target_remote_execution(self,tgt,fun,arg):
        ''' Use targeting for remote execution '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'nodegroup'}
        obj = urllib.parse.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid
    def deploy(self,tgt,arg):
        ''' Module deployment '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        obj = urllib.parse.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        return content
    def async_deploy(self,tgt,arg):
        ''' Asynchronously send a command to connected minions '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        obj = urllib.parse.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid
    def target_deploy(self,tgt,arg):
        ''' Based on the node group forms deployment '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'nodegroup'}
        obj = urllib.parse.urlencode(params)
        self.token_id()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid
def main():
    sapi = SaltAPI(url='http://192.168.216.128:9999',username='saltapi',password='saltapi')
    #print (sapi.list_all_key())
#    sapi.token_id()
    #sapi.delete_key('test-01')
    #print (sapi.accept_key('localhost'))
    #sapi.deploy('test-01','nginx')
    print (sapi.remote_noarg_execution('*','grains.items'))
    #print (sapi.list_all_key())
if __name__ == '__main__':
    main()
