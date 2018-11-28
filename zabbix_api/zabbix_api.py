'''
Created on 2018年1月26日

@author: ning.lin
'''

#coding=utf-8
import configparser
import json
import os
import time

import requests


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
            for (key, value) in config.items('zabbix_api_info'):  
                data[key] = value
            return data      
    except Exception as e:  
        print ("Open file error." ,str(e)) 
        
#多线程执行方法


#获取api接口对象
def get_zabbix_api():
    data = get_api()
    zabbix_api=ZabbixApi(data['url'],data['username'],data['password'])
    return zabbix_api



class ZabbixApi():
    def __init__(self, url,username,password):
        self.url = url
        self.username = username
        self.password = password
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Content-type": "application/json"
            # "Content-type": "application/x-yaml"
        }
        self.data = {
                        "jsonrpc": "2.0",
                        "method": "user.login",
                        "params": {
                            "user": username,
                            "password": password
                        },
                        "id": 1,
                    }
        # self.params = {'client': 'local', 'fun': '', 'tgt': '', 'arg': ''}
        self.api_url = "{}/api_jsonrpc.php".format(self.url)
        self.token = self.get_data(self.data)['result']
        #print("token_id",self.token)
        
    #这里是定制请求头
    def get_data(self, params):
        url = self.api_url
        send_data = json.dumps(params)
        request = requests.post(url, data=send_data, headers=self.headers)
        #response = request.json()
        response=json.loads(request.text)
        result = dict(response)
        #print("result",type(result),result)
        return result
        #return result['result']
    #获取主机组
    def getgroupId(self,auth,groupName):
        data = {
        "jsonrpc": "2.0",
        "method": "hostgroup.get",
        "params": {
            "output": "extend",
            #"output":["groupid","name"],
            "filter": {
                "name":groupName
            }
        },
        "auth": auth,
        "id": 1
        }
        return self.get_data(data)
    #获取主机
    '''
    hostip可以为主机IP
    '''
    def get_host_from_ip(self,hostip):
        data = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
                    "output": ["hostid", "host","status"],
#         "selectInterfaces": [
#                     "interfaceid", "ip" ],
        "filter": {
            "ip": hostip,
            "status":0,
        },
            #"output":["hostid","name","status","host"],
            #"filter": {"host": [hostip]},
        },
        "auth": self.token,
        "id": 0
        }
        return self.get_data(data)
    #获取主机
    '''
    hostname可以为主机名
    '''
    def get_host_from_name(self,hostname):
        data = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
                    "output": ["hostid", "host","status"],
#         "selectInterfaces": [
#                     "interfaceid", "ip" ],
        "filter": {
            "host": hostname,
        },
            #"output":["hostid","name","status","host"],
            #"filter": {"host": [hostip]},
        },
        "auth": self.token,
        "id": 0
        }
        return self.get_data(data)
    
    #获取模板ID
    def template_get(self,hostip):
        data =  {
                    "jsonrpc": "2.0",
                    "method": "template.get",
                    "params": {
                        "output": "extend",
                        "host":hostip,
                        },
                    "auth":  self.token,
                    "id": 1,
                    }
        return self.get_data(data)
    #获取主机下面的所有items
    def get_item(self,hostids):
        data = {
                "jsonrpc": "2.0",
                "method": "item.get",
                "params": {
#                     "output": "extend",
                    "hostids": hostids,
                    #value_type用来确定history.get方法的history参数
                    "output":["itemids","key_","value_type","units","lastvalue","units","lastclock","description"],
                    "sortfield": "name"
                },
                "auth":  self.token,
                "id": 1
            }
        return self.get_data(data)
    
    def get_history(self,items_id,time_from,time_till,history_type=3):
        '''
        history参数，决定在history, history_uint,哪个表中去查    integer    History object types to return. 

            Possible values: 
            0 - numeric float; 
            1 - character; 
            2 - log; 
            3 - numeric unsigned; 
            4 - text. 
            
            Default: 3.
        '''
        data =  {
                    "jsonrpc": "2.0",
                    "method": "history.get",
                    "params": {
                        "output": "extend",
                        "history": history_type,
                        "itemids": items_id,
                        "sortfield": "clock",
                        "sortorder": "DESC",
                        "time_from": time_from,
                        "time_till": time_till,
#                         "limit":10,
                    },
                    "auth":  self.token,
                    "id": 1
                }
        return self.get_data(data)
    def aaa(self,history_type,items_id):
        data =  {
                    "jsonrpc": "2.0",
                    "method": "history.get",
                    "params": {
                        "output": "extend",
                        "history": history_type,
                        "itemids": items_id,
                        "sortfield": "clock",
                        "sortorder": "DESC",
#                         "time_from": time_from,
#                         "time_till": time_till,
                        "limit":10,
                    },
                    "auth":  self.token,
                    "id": 1
                }
        return self.get_data(data)

if __name__ == '__main__':
#     ZABBIX_URL = 'http://192.168.216.128:8080/zabbix/'
#     ZABBIX_USERNAME = "Admin"
#     ZABBIX_PASSWORD = "zabbix"
#     zabbix_api=ZabbixApi(ZABBIX_URL,ZABBIX_USERNAME,ZABBIX_PASSWORD)
    zb_api = get_zabbix_api()
    print("zabbix_api",type(zb_api.token),zb_api.token)
    {'key_': 'system.cpu.switches', 'history_type': '3', 'itemid': '28271'}
    #    3.0_agent_windows
    #master_129
    #print("aaa",zabbix_api.getgroupId(zabbix_api.token, ['3.0_agent_windows','master_129']))
    result=zb_api.get_host_from_ip(['192.168.216.128','192.168.23.130'])
#     print("resultb",len(result),result)
# #     result=zabbix_api.template_get(['192.168.216.128','192.168.23.130'])
    result=zb_api.get_item(10254)
    print("resulta",len(result),result)
    for item in result['result']:
        print("itema",item,len(item))
#     result = zb_api.aaa(3,[28288,28263])
#     print("resultb",len(result),result)
#     for item in result['result']:
#         print("itemb",item,len(item))
#     

#     host = zb_api.get_host_from_ip('192.168.216.128')
#     print("host",host)
#     if host['result']==[]:
#         print("host is null")
#     host = zb_api.get_host_from_name('sss')
#     print("host",host)
#     result = zb_api.get_item(host['result'][0]['hostid'])
#     print("result",len(result),result)
#     for item in result['result']:
#         print("item",item,len(item))
    #result = zb_api.get_history(28274)
#     #10254
#     result = zb_api.get_history(['28272'],1514736052,1517414452)
    #result = zb_api.get_history('28279')
#     print("resultaa",len(result),result)
#     count = 0;
#     for item in result['result']:
#         count +=1;
#         print("itemaa",item,len(item))
# #         print("description",item['description'])
#         print("key_",item['key_'])
#         print("clock",item['clock'])
#         a=time.time()
#         print("time.time()",a)
#         print("当前时间",datetime.datetime.utcfromtimestamp(a))
#         time_local = time.localtime(int(item['clock']))
#         dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
#         print("value",item['value'])
        #dateArray = datetime.datetime.utcfromtimestamp(int(item['clock']))
#         print("dt",type(dt),dt)
#         print("lastvalue",item['lastvalue'])
        #print("lastvalue",float(item['lastvalue'])/60/60)
        #print("lastvalue",int(item['lastvalue'])/1024/1024/1024)
#     print("总个数",count)
    

