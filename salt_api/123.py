# -*- coding:utf-8 -*-
import urllib.request
import ssl
import json
import re
import os
import logging
from collections import OrderedDict
logger = logging.getLogger("scripts")

# 定义一个有序字典,在后面的代码中使用urllib.parse.urlencode(params),保证转换后的参数顺序和传入的顺序一致
# 否则在使用cp.get_file等需要多个参数指令时，会导致参数混乱
params = OrderedDict()

# 测试环境 salt-master的IP
salturl='http://172.17.39.93:9999/'
user='saltapi'
password='saltapi'

def get_token():
    params = {'eauth': 'pam', 'username': user, 'password': password}
    headers = {'X-Auth-Token': ''}
    # 将params转换为password=salt%21%2313&eauth=pam&username=saltapi格式
    data = urllib.parse.urlencode(params)
    # 将data转换为bytes格式,因为request.Request只接受bytes格式的数据
    data = data.encode('utf-8')
    url = salturl + '/login'
    req = urllib.request.Request(url, data, headers)
    opener = urllib.request.urlopen(req)
    # 获取返回的结果
    resData = opener.read()
    # 将返回的结果转换成json格式
    resData = json.loads(resData.decode())
    token = resData['return'][0]['token']
    return token


def send_command(serverlist, command):
    params = OrderedDict([('client', 'local'), ('fun', 'cmd.run'), ('arg1', command), ('tgt', serverlist), ('expr_form', 'list')])
    return send_request(params)


def upload_file(filename):
    webserver = '127.0.0.1'
    uploadfile = '/home/project/mysite/collectedstatic/upload/' + filename
    params = OrderedDict([('client', 'local'), ('fun', 'cp.push'), ('tgt', webserver), ('arg', uploadfile)])
    return send_request(params)


def rsync_file(serverlist, spath, dpath):
    params = OrderedDict([('client', 'local'), ('fun', 'cp.get_dir'), ('arg1', spath), ('arg2', dpath), ('tgt', serverlist)])
    return send_request(params)


def custom_command(serverlist, customorder, arg1, arg2=""):
    if customorder == "cmd.run":
        command = arg1 + " " + arg2
        params = OrderedDict([('client', 'local'), ('fun', customorder), ('arg', command), ('tgt', serverlist), ('expr_form', 'list')])
    else:
        params = OrderedDict([('client', 'local'), ('fun', customorder), ('arg1', arg1), ('arg2', arg2), ('tgt', serverlist), ('expr_form', 'list')])
    return send_request(params)


def update_command(arg1, arg2, arg3, arg4):
    params = OrderedDict([('client', 'runner'), ('fun', 'master.buildproject'), ('arg1', arg1), ('arg2', arg2), ('arg3', arg3), ('arg4', arg4)])
    return send_request(params)


def send_request(params):
    url = salturl + '/'
    print("url",url)
    tokenid = get_token()
    headers = {'X-Auth-Token': tokenid}
    data = urllib.parse.urlencode(params)
    print("data",data)
    data, num = re.subn("arg\d", 'arg', data)
    print("data1",data)
    data = data.encode('utf-8')
    print("data2",data)
    req = urllib.request.Request(url, data, headers)
    print("req",req)
    opener = urllib.request.urlopen(req)
    resData = opener.read()
    print("resData",resData)
    resData = json.loads(resData.decode())
    return resData
if __name__ == '__main__':
    #print(rsync_file('172.17.39.208_windows10_app','salt://temp/1.txt','D:/1012/1.txt'))
    print(rsync_file('172.17.39.208_windows10_app','salt://temp/','D:/1012/'))