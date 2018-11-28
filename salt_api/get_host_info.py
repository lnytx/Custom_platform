# -*- coding: utf-8 -*-
'''
Created on 2017年10月20日

@author: ning.lin
'''
'''
Salt API得到资产信息，进行格式化输出
'''
#获取接口

from salt_api.salt_api_requests import get_api, SaltAPI


def get_salt_host_details(tgt):
    connect=''
    api = get_api()
    print(api)
    salt_api = SaltAPI(api['url'],api['username'],api['password'])
    host_info = {}
    disk_usage = {}
    #判断是否连接上
    connect = salt_api.salt_alive(tgt)
    print("connect",connect)
    #connect {'windows10_app1': True} <class 'dict'>
    if tgt in connect and connect[tgt]==True:
        print("%s可以连上" %tgt)
        ret1 = salt_api.salt_command(tgt,'grains.items')
        for k,v in ret1.items():
            print("type(v)",type(v))
            if isinstance(v,dict):
                for k2,v2 in v.items():
                    #print("key:%s,value:%s" % (k2,v2),type(v))
                    if k2=='id':
                        host_info['minion_id']=v.get(k2, None)
#                     elif k2=='master':
#                         host_info['ip']=v.get(k2, None)
                    host_info[k2]=v2
            #print(k+":"+v)
        ret2 = salt_api.salt_command(tgt,'disk.usage')
        for k,v in ret2.items():
            if isinstance(v,dict):
                for k2,v2 in v.items():
                    disk_usage[k2]=v2
        #host_info与disk_usage两个dict合并起来
        result=dict(host_info,**disk_usage)
        #return host_info,disk_usage,connect
    else:
        print("连接异常",connect)
    return host_info,disk_usage,connect
    
if __name__=='__main__':
    result = get_salt_host_details('windows10_app1')
    print(type(result),len(result),result)
    #{'/boot': {'1K-blocks': '297485', 'capacity': '14%', 'used': '36690', 'filesystem': '/dev/sda1', 'available': '245435'}, '/': {'1K-blocks': '47269816', 'capacity': '45%', 'used': '19979660', 'filesystem': '/dev/sda3', 'available': '24888928'}, '/dev/shm': {'1K-blocks': '953452', 'capacity': '1%', 'used': '124', 'filesystem': 'tmpfs', 'available': '953328'}}
    #disk_usage {'D:\\': {'filesystem': 'D:\\', '1K-blocks': 1953512444, 'used': 398024044, 'capacity': '20%', 'available': 1555488400}, 'E:\\': {'filesystem': 'E:\\', '1K-blocks': 823159804, 'used': 805258976, 'capacity': '98%', 'available': 17900828}, 'C:\\': {'filesystem': 'C:\\', '1K-blocks': 152604152, 'used': 72042612, 'capacity': '47%', 'available': 80561540}}
#     print(type(result[0]),result[0])
    disk_info=[]
    temp=()
#     ip = result[0]['master']
# #     minion_id = result[0]['minion_id']
#     temp=(ip,minion_id)
# # #     result[1]['ip']=ip
# # #     result[1]['minion_id']=minion_id
# # #     print(type(result[1]),result[1])
# #     #<class 'dict'> {'C:\\': {'used': 71635812, '1K-blocks': 104864252, 'capacity': '68%', 'available': 33228440, 'filesystem': 'C:\\'}, 
#     for k,v in result[1].items():
#             print(k,type(v))
# #             disk_info.append(ip)
# #             disk_info.append(minion_id)
#             #两个tuple合并操作是相加
#             disk_info.append(tuple(v.values())+temp)
#             #disk_info +=temp
#     print("disk_info",disk_info)
#             
