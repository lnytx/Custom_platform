# -*- coding:utf-8 -*-
'''
Created on 2017年12月28日

@author: ning.lin
'''
'''
    import schedule
import time
def job():
    print("I'm working...")
schedule.every(10).seconds.do(job)#每隔10秒执行函数job
schedule.every(10).minutes.do(job)#每隔10分钟执行函数job
schedule.every().hour.do(job)#每隔1小时执行函数job
schedule.every().day.at("10:30").do(job) #每天的10点半执行函数job 
schedule.every().monday.do(job)#每周一执行函数job
schedule.every().wednesday.at("13:15").do(job)  #每周三下午1点14分执行函数job
while True:
    schedule.run_pending() #执行任务
    time.sleep(1)
'''
# from salt_api.Mytoolkits import format_result, format_result
# from salt_api.salt_api_requests import get_salt_api, format_minionIDs

import os
import time

from apscheduler.scheduler import Scheduler

from pymysql_conn import exec_sql, exec_sql_args, format_args
from salt_api.salt_api_requests import get_salt_api

'''
install apscheduler==2.1.2 定时运行函数
在url中定义运行
#定时任务脚本
from apscheduler.scheduler import Scheduler  
#要执行的方法  
from cmdb.cron.host_status import update_host
from cmdb.cron.host_status2 import update_host
'''
sched = Scheduler()

@sched.interval_schedule(minutes=1)
def update_host():
    '''
                    执行sql根据对应的状态修改simion_key的状态
        1为接受
        2为未接受
        3为Denied0为已删除的
        4为拒绝的
    '''
    salt_api = get_salt_api()
    #根据minion_id状态，Unaccepted,Rejected等更新对应minion_id的数据库状态
    #Unaccepted
    unaccepted_keys=salt_api.get_all_keys()['minions_pre']
    if unaccepted_keys:
        exec_sql_args("update `host` set minion_key_stat=2 where minion_id in "+format_args(unaccepted_keys),unaccepted_keys)
    #exec_sql("update `host` set minion_key_stat=1 where ")
    #Accepted
    accepted_keys=salt_api.get_all_keys()['minions']
    if accepted_keys:
        exec_sql_args("update `host` set minion_key_stat=1 where minion_id in "+format_args(accepted_keys),accepted_keys)
    #Rejected
    rejected_keys=salt_api.get_all_keys()['minions_rejected']
    if rejected_keys:
        exec_sql_args("update `host` set minion_key_stat=4 where minion_id in "+format_args(rejected_keys),rejected_keys)
    #Denied
    '''
        如果有两个相同的minion_id的话，其中一个会被Denied，另一个在Unaccepted
    '''
    denied_keys=salt_api.get_all_keys()['minions_denied']
    if denied_keys: 
        exec_sql_args("update `host` set minion_key_stat=3 where minion_id in "+format_args(denied_keys),denied_keys)
    '''
        根据manage.status来确定accepted_keys对应的主机是否是down或者up
        salt主机是否能连上客户机，能为1，否为0
    '''
    host_up=salt_api.minion_status()['up']
    print("host_up",host_up)
    if host_up:
        exec_sql_args("update `host` set status=1 where minion_id in "+format_args(host_up),host_up)
    host_down=salt_api.minion_status()['down']
    if host_down:
        exec_sql_args("update `host` set status=0 where minion_id in "+format_args(host_down),host_down)
    
sched.start()
