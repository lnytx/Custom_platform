'''
Created on 2018年1月26日

@author: ning.lin
'''

#coding=utf-8
import json
import time

import requests


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
        print("response",response)
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
                    "output":["itemids","key_","lastvalue","units","lastclock"],
                    "sortfield": "name"
                },
                "auth":  self.token,
                "id": 1
            }
        return self.get_data(data)
    
    def get_history(self,items_id):
        data =  {
                    "jsonrpc": "2.0",
                    "method": "history.get",
                    "params": {
                        "output": "extend",
                        "history": 0,
                        "itemids": items_id,
                        "sortfield": "clock",
                        "sortorder": "DESC",
                        "time_from": "1517377934",
                        "time_till": "1517378114"
                    },
                    "auth":  self.token,
                    "id": 1
                }
        return self.get_data(data)
if __name__ == '__main__':
    ZABBIX_URL = 'http://192.168.216.128:8080/zabbix/'
    ZABBIX_USERNAME = "Admin"
    ZABBIX_PASSWORD = "zabbix"
    zabbix_api=ZabbixApi(ZABBIX_URL,ZABBIX_USERNAME,ZABBIX_PASSWORD)
    #    3.0_agent_windows
    #master_129
    #print("aaa",zabbix_api.getgroupId(zabbix_api.token, ['3.0_agent_windows','master_129']))
    #result=zabbix_api.gethost(zabbix_api.token,['192.168.216.128','192.168.23.130'])
#     result=zabbix_api.template_get(['192.168.216.128','192.168.23.130'])
#     result=zabbix_api.get_item(10254)
#     
#     result = zabbix_api.get_history(28274)
    host = zabbix_api.get_host_from_ip('192.168.216.128')
    host = zabbix_api.get_host_from_name('sss')
    print("host",host)
    result = zabbix_api.get_item(host['result'][0]['hostid'])
    result = zabbix_api.get_history(28308)
    #10254
    print("result",len(result),result)
    for item in result['result']:
        print("item",item,len(item))
#         print("description",item['description'])
        print("key_",item['key_'])
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
    

