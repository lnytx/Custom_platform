# -*- coding: utf-8 -*-

'''
使用的是request模块(理论上说python2与python3都可以使用)
'''

import http
import json

import requests


url="http://172.17.39.93:9999/login"
username='saltapi'
password='saltapi'


def token_id():
        ''' user login and get token id
        curl -k https://ip地址:8080/login
        -H "Accept: application/x-yaml" -d username='用户名' -d password='密码' -d eauth='pam'
        '''
        #获取token_id的请求数据
        par = {'username': username,'password': password,'eauth': 'pam' }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Content-type": "application/json"
            # "Content-type": "application/x-yaml"
        }
        #将请求的类型转成例如
        #password=salt&eauth=pam&username=salt
        #转成二进制
        #将二进制数据交给postRequest函数处理
        #s = json.dumps(params)
        send_data=json.dumps(par)
        content = requests.post(url, data=send_data, headers=headers, verify=False)
        print("url",content.url)
        response = content.json()
        print("response",type(response),response)
        try:
            token_id = response['return'][0]['token']
            print("token_id",token_id)
            return token_id
        except Exception as e:
            print(str(e))
 
def salt_command(tgt, method, arg=None):
        """远程执行命令，相当于salt 'client1' cmd.run 'free -m'"""
        if arg:
            params = {'client': 'local', 'fun': method, 'tgt': tgt, 'arg': arg}
        else:
            params = {'client': 'local', 'fun': method, 'tgt': tgt}
        url="http://192.168.160.130:9999/"
        send_data = json.dumps(params)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Content-type": "application/json"
            # "Content-type": "application/x-yaml"
        }

        request = requests.post(url, data=send_data, headers=headers, verify=False)
        response = request.json()
        return response


         
if __name__=='__main__':
    token_id()
    print(salt_command("*",'test.ping'))