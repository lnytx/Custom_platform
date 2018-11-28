import json
import time

from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response

from pymysql_conn import exec_sql, exec_sql_args
from salt_api.Mytoolkits import read_config
from zabbix_api.zabbix_api import get_zabbix_api


# Create your views here.
def zabbix_minion(request):
    print("aaaaaaaaaaaaaaaaaa")
    '''判断用户是否登陆'''
    #.is_authenticated()通过判断session中是否有user_id 以及user_backend 来判断用户是否登陆。
    username=request.user.username
    sql = "select group_name from host_group"
    group_list=exec_sql(sql)
    print("group_list",group_list)
    #return HttpResponse(json.dumps(group_list), content_type='application/json')
    return render(request,'zabbix_monitor/zabbix_monitor.html',{'group_list':group_list})

#通过IP获取组名
def zabbix_get_group(request):
    if request.is_ajax(): 
        if 'host_ip' in request.GET:  
            host_ip = request.GET.get("host_ip")
    sql = 'select group_name from host where ip=%s'
    result = exec_sql_args(sql,(host_ip,))
    print("result",result)
    return HttpResponse(json.dumps(result), content_type='application/json')

def zabbix_get_host(request):
    if request.is_ajax(): 
        if 'group_name' in request.GET:  
            group_name = request.GET.get("group_name")
            print("group_name",type(group_name),group_name)
            sql = "select ip from host where group_name=%s"
            result = exec_sql_args(sql,(group_name,))
            print("result",type(result),result)
            return HttpResponse(json.dumps(result), content_type='application/json')

'''
通过前端提供的ip取得机器的所有的监控项
'''
def zabbix_get_items(request):
    if request.is_ajax(): 
        if 'ip' in request.GET:  
            item_list = []
            ip = request.GET.get("ip")
            print("ip",type(ip),ip)
            result={"1":2}
            zabbix_api = get_zabbix_api()
            host = zabbix_api.get_host_from_ip(ip)
            print("host",type(host),host)
            if host['result']==[]:
                return HttpResponse(json.dumps({"code":-1,"msg":"zabbix没有对应的主机:"+ip,'status':'error'}), content_type='application/json')
            #获取所有的监控项
            result = zabbix_api.get_item(host['result'][0]['hostid'])
            print("result",type(result),result)
            item_list = [{item['itemid']+"_"+str(item['units'])+'_'+str(item['value_type']):item['key_']} for item in result['result']]
            print("item_list",item_list)
            return HttpResponse(json.dumps(item_list), content_type='application/json')

def GGG(request):
#     myMap2 = request.GET.get('operatorIDs')
#     param= json.loads(request.body.decode('utf-8'))
#     print("myMap1",type(param),param)
    if 'item_id' in request.GET:  
        item_list = []
        myMap = request.GET.getlist('item_id')
        time_from = request.GET.get("time_from")
        time_till = request.GET.get("time_till")
        print("time_from",time_from)
        print("time_till",time_till)
        print("item_id",type(myMap),myMap)
        zabbix_api = get_zabbix_api()
        #根据前台的item_id获取zabbix监控数据
    else:
        return HttpResponse(json.dumps({'code':-1,"msg":'没有选择graph值'}), content_type='application/json')
    return HttpResponse(json.dumps({'1':2}), content_type='application/json')

def zabbix_get_graph(request):
    #time接收前台传过的时间并转成时间戳
    starttime=endtime=None
    zabbix_minion_name = request.GET.get("zabbix_minion_name")
    zabbix_minion_starttime = request.GET.get("time_from")
    zabbix_minion_endtime = request.GET.get("time_till")
    #获取key_itemid值
    key_itemids = json.loads(request.GET['key_itemid'])
    print("key_itemids",key_itemids)
        
    
    print("zabbix_minion_starttime",type(zabbix_minion_starttime),zabbix_minion_starttime)
    print("zabbix_minion_endtime",type(zabbix_minion_endtime),zabbix_minion_endtime)
    #转换成时间数组
    if zabbix_minion_starttime != '':
        time1 = time.strptime(zabbix_minion_starttime, "%Y-%m-%d %H:%M:%S")
        starttime = int(time.mktime(time1))
        print("time1",time1)
        print("starttime",starttime)
    if zabbix_minion_endtime != '':
        time2 = time.strptime(zabbix_minion_endtime, "%Y-%m-%d %H:%M:%S")
        endtime = int(time.mktime(time2))
        print("endtime",endtime)
    #转换成时间戳
    #1517338596
    print("timestampaaaaaaaaaaaaaaaaaaa",starttime,endtime)
    zabbix_api = get_zabbix_api()
    #执行zabbix_api此处可以使用多进程
    result={}
    result_temp=[]
    for item in key_itemids:
        print("iii",type(item),item)
        temp = zabbix_api.get_history(item['itemid'], starttime, endtime, item['history_type'])
        print("temp",type(temp),temp['result'])
        result_temp=temp['result']
        result[item['key_']+'_'+item['units']] = result_temp
    print("result",result)
    count=0;
    for k,v in result.items():
        print("kv",k,len(v),v)
#         for i in v:
#             count+=1;
#             print("总数",count)
#             continue;
    
    print("json.dumps(result['result']",json.dumps(result))
    print("len(result0['result']+result3['result'])",len(result))
    return HttpResponse(json.dumps(result), content_type='application/json')
    #return render(request,'zabbix_monitor/zabbix_monitor.html',{'zabbix_minion_graph':zabbix_minion_graph,"result":result})
