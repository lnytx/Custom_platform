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
    print("ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
    
sched.start()
