'''
Created on 2017年8月4日

@author: admin
'''
# -*- coding:utf-8 -*-
import datetime

import pymysql


#sql是否执行成功，成功返回1，否则返回-1
res_code = ''

#处理多个参数时，计算应该有几个%s的方法
def format_args(args):
    s=''
    for a in args:
        s=s+'%s,'
    print(s)
    print('('+ s[:-1]+ ')')
    return '('+ s[:-1]+ ')'

def connect():
    config={'host':'127.0.0.1',
                'user':'root',
                'password':'root',
                'port':3306,
                'database':'my_devpos',
                'charset':'utf8',
                #要加上下面一行返回的是list，否则默认返回的是tuple
                'cursorclass':pymysql.cursors.DictCursor,
            }
    try:
        conn=pymysql.connect(**config)
        print("conn is success!")
        return conn
    except Exception as e:
        print("conn is fails{}".format(e))
        
def select_table(table_name,ip):

    #sql_select = "select ip from host where ip ='127.0.0.1'"
    #sql_select = 'select ip from ' + table_name
    try:
        conn=connect()
        cursor=conn.cursor()
        if table_name=='host':
            sql_select = "SELECT * FROM "+'`host`'+" WHERE `ip` = %s"
        elif table_name=='host_details':
            sql_select = "SELECT * FROM "+'`host_details`'+" WHERE `ip` = %s"
        elif table_name== 'host_group':
            sql_select = "SELECT * FROM "+'`host_group`'+" WHERE `group_name` = %s"
        elif table_name== 'salt_host_details':
            sql_select = "SELECT * FROM "+'`salt_host_details`'+" WHERE `ip` = %s"
        elif table_name== 'disk_usage':
            sql_select = "SELECT * FROM "+'`disk_usage`'+" WHERE `ip` = %s"
        elif table_name== 'project_manage':
            sql_select = "SELECT ip,project_name FROM "+'`project_manage`'+" WHERE `ip` = %s"
        elif table_name=='service_manage':
            sql_select = "SELECT * FROM "+'`service_manage`'+" WHERE `ip` = %s"
            print("sql_select",sql_select)
        cursor.execute(sql_select,(ip))
        # 获取剩余结果的第一行数据
#         row_1 = cursor.fetchone()
#         
#         # 获取剩余结果前n行数据
#         row_2 = cursor.fetchmany(3)
         
        # 获取剩余结果所有数据
        row_3 = cursor.fetchall()
        conn.commit()
        res_code=1
        return row_3
    except Exception as e:
        print("select_table execute fails{}".format(e))
        res_code=-1

def select_all(table_name):
    try:
        conn=connect()
        cursor=conn.cursor()
        if table_name=='host':
            sql_select='select * from ' +table_name + ' order by ip'
        elif table_name=='host_details':
            sql_select='select * from ' +table_name + ' order by ip'
        elif table_name=='host_group':
            sql_select='select * from ' +table_name + ' order by group_id'
        elif table_name=='project_manage':
            sql_select='select * from ' +table_name + ' order by id'
        elif table_name=='service_manage':
            sql_select='select * from ' +table_name + ' order by ip'
        cursor.execute(sql_select)
        # 获取剩余结果所有数据,结果类型为list
        row_3 = cursor.fetchall()
        conn.commit()
        return row_3 
    except Exception as e:
        print("select_all execute fails{}".format(e))
        
#插入hostname表
def insert_table(table_name,data):
        res_code=-1
        try:
            conn=connect()
            cursor = conn.cursor()
            #元组连接插入方式
            if table_name=='host':
                sql_insert = "insert into `host` (ip,hostname,ostype,application,pwd,username,port,group_name,minion_id) \
                values(%s,%s,%s,%s,md5(%s),%s,%s,%s,%s)"
                print(sql_insert)
                cursor.execute(sql_insert, (data['ip'],data['hostname'],data['ostype'],data['application'],data['pwd'],data['username'],data['ports'],data['group_name'],data['minion_id']))
                conn.commit()
                res_code=1      
                return res_code  
            elif table_name=='host_details':
                sql_insert = "insert into host_details (ip,hostname,ostype,application,pwd,username,port) \
                values(%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql_insert, data)
                conn.commit()   
                res_code=1      
                return res_code    
            elif table_name=='host_group':
                sql_insert = "insert into host_group (group_name,remark) \
                values(%s,%s)"
                cursor.execute(sql_insert, (data['group_name'],data['remark']))
                conn.commit()   
                res_code=1      
                return res_code  
            elif table_name=='service_manage':
                sql_insert = "insert into service_manage (ip,`port`,`group`) \
                values(%s,%s,%s)"
                try:
                    cursor.execute(sql_insert, (data['ip'],data['ports'],data['group_name']))
                    conn.commit()   
                    res_code=1      
                except Exception as e:
                    print("insert service_manage fails:%s,%s" %(str(e),sql_insert))
                    res_code=0
                return res_code  
            
            elif table_name=='salt_host_details':
                sql_insert = "insert into salt_host_details (ip,minion_id,kernel,osversion,cpu_model,num_cpus,manufacturer,osfullname,mem_total,windowsdomain,fqdn,\
                os,cpuarch,roles,osrelease,kernelrelease,saltversion,osmanufacturer,saltpath,timezone,os_family,shell,username,domain) \
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql_insert,((data['ip'],data['minion_id'],data['kernel'],data['osversion'],data['cpu_model'],data['num_cpus'],
                                            data['manufacturer'],data['osfullname'],data['mem_total'],data['windowsdomain'],data['fqdn'],data['os'],
                                            data['cpuarch'],data['roles'],data['osrelease'],data['kernelrelease'],data['saltversion'],data['osmanufacturer'],data['saltpath'],
                                            data['timezone'],data['os_family'],data['shell'],data['username'],data['domain'])))
                conn.commit()   
                res_code=1 
                return res_code  
            elif table_name=='project_manage':
                sql_insert = "insert into project_manage (project_name,ip,center_path,dest_path) \
                            values(%s,%s,%s,%s)"
                cursor.execute(sql_insert,(data['project_name'],data['ip'],data['center_path'],data['dest_path']))
                conn.commit()   
                res_code=1      
                return res_code  
            elif table_name=='disk_usage':
                #更新也是用到insert
                for v in data:
                    sql_insert = "insert into disk_usage(capacity,total,`partition`,used,available,ip,minion_id) \
                    values(%s,%s,%s,%s,%s,%s,%s)"
                    print("sql_insert",sql_insert)
                    cursor.execute(sql_insert,(v['capacity'],v['1K-blocks'],v['filesystem'],v['used'],v['available'],v['ip'],v['minion_id']))
                    conn.commit()
                    res_code=1     
                return res_code  
        except Exception as e:
            print("insert_table disk_usage execute fails{}".format(e))
            res_code=-1
            return res_code
            
def delete_table(table_name,ip):
        res_code=-1
        try:
            conn=connect()
            cursor = conn.cursor()
            #元组连接插入方式
            sql_delete = 'delete  from '+table_name+' where ip= %s'
            cursor.execute(sql_delete,(ip,))
            conn.commit()
            res_code=1
        except Exception as e:
            print("delete_table execute fails{}".format(e))
            res_code=-1
        finally:
            cursor.close()
            conn.close()
            print("conn has chosed")
            return res_code
def update_table(table_name,data):
        res_code=-1
        error=''
        try:
            conn=connect()
            cursor = conn.cursor()
            #元组连接插入方式md5对密码进行加密
            if table_name=='host':
                sql_update = "update "+table_name+" set `ip`=%s,`hostname`=%s,`ostype`=%s,`application`=%s,`port`=%s,`username`=%s,`group_name`=%s,`pwd`=md5(%s),`minion_id`=%s where `ip`=%s and minion_id=%s"
                print("sql_update",sql_update)
                try:
                    cursor.execute(sql_update, (data['ip'],data['hostname'],data['ostype'],data['application'],data['ports'],data['username'],data['group_name'],data['pwd'],data['minion_id'],data['old_ip'],data['old_minion_id']))
                    conn.commit()
                    res_code=1
                except Exception as e:
                    error = str(e)
                    print("errrrrrrrror",str(e))
            elif table_name=='device_status':
                sql_update = "update "+table_name+" set `cpu`=%s,`memory`=%s,`location`=%s,`product`=%s,`platform`=%s,`sn`=%s where `ip`=%s"
                cursor.execute(sql_update, (data['cpu'],data['memory'],data['location'],data['product'],data['platform'],data['sn'],data['ip']))
                conn.commit()
                res_code=1
            elif table_name=='salt_host_details':
                sql_update = '''update salt_host_details set ip=%s,minion_id=%s,kernel=%s,osversion=%s,cpu_model=%s,num_cpus=%s,
                                manufacturer=%s,osfullname=%s,mem_total=%s,windowsdomain=%s,fqdn=%s,os=%s,cpuarch=%s,                            
                                roles=%s,osrelease=%s,kernelrelease=%s,saltversion=%s,osmanufacturer=%s,saltpath=%s,                            
                                timezone=%s,os_family=%s,shell=%s,username=%s,domain=%s 
                                where ip=%s and minion_id=%s'''
                cursor.execute(sql_update,((data['ip'],data['minion_id'],data['kernel'],data['osversion'],data['cpu_model'],data['num_cpus'],
                                                data['manufacturer'],data['osfullname'],data['mem_total'],data['windowsdomain'],data['fqdn'],data['os'],
                                                data['cpuarch'],data['roles'],data['osrelease'],data['kernelrelease'],data['saltversion'],data['osmanufacturer'],data['saltpath'],
                                                data['timezone'],data['os_family'],data['shell'],data['username'],data['domain'],data['ip'],data['minion_id'])))
                conn.commit()
                res_code=1     
            elif table_name=='disk_usage':
                for v in data:
                    sql_update = '''update disk_usage set capacity=%s,total=%s,`partition`=%s,used=%s,available=%s,ip=%s,minion_id=%s
                                    where ip=%s and minion_id=%s and `partition`= %s'''
                    print("sql_update",sql_update)
                    cursor.execute(sql_update,(v['capacity'],v['1K-blocks'],v['filesystem'],v['used'],v['available'],v['ip'],v['minion_id'],v['ip'],v['minion_id'],v['filesystem']))
                    conn.commit()
                    res_code=1  
                res_code=1      
        except Exception as e:
            print("update_table execute fails{}".format(e))
            res_code=-1
        finally:
            cursor.close()
            conn.close()
            print("conn has chosed")
            return res_code,error
        
#这个方法是处理添加group时，处理host表的
def exec_add_group(data):
    res_code=-1
    conn=connect()
    cursor = conn.cursor()
    group_args=(data['group_id'],data['group_name'])
    group_ip=(data['ip'])
    args = group_args+group_ip#将两个tuple连起来
    sql = 'update host set group_id=%s,group_name=%s where ip in '+format_args(data['ip'])#处理in后面（%s,s%,s%,s%,s%,s%,s%）
    try:
        cursor.execute(sql,args)
        conn.commit()
        res_code = 1
    except Exception as e:
        print("update_table execute fails{}".format(e))
        res_code=-1
    finally:
        cursor.close()
        conn.close()
        print("conn has chosed")
        return res_code
'''
将每次的操作记录写入数据库中
'''
def  operation_record(target_ids,user_id='None',user_name='None',action='None',result='None'):
    error=''
    exec_time = datetime.datetime.now()
    #处理操作记录表
    sql_record = "insert into operation_record (user_id,user_name,target_ids,action,result,exec_time) \
                    values (%s,%s,%s,%s,%s,%s)"
    try:
        conn=connect()
        cursor=conn.cursor()
        cursor.execute(sql_record, (user_id,user_name,target_ids,action,result,exec_time))
        conn.commit()
        res_code=1
    except Exception as e:
        error = str(e)
        print("operation_record_error",error)
    return error
'''
将每次操作的目标minion_id写入数据库中
'''
def  opertion_minions(target_ids='None',minion_id='None',edit_before='None',edit_after='None',remark='None',):
    error=''
    #处理每步操作的服务器对象表（记录minion_id）
    sql_minions = "insert into opertion_minions (target_ids,minion_id,edit_before,edit_after,remark) \
                    values (%s,%s,%s,%s,%s)"
    try:
        conn=connect()
        cursor=conn.cursor()
        cursor.execute(sql_minions, (target_ids,minion_id,edit_before,edit_after,remark))
        conn.commit()
        res_code=1
    except Exception as e:
        print("opertion_minions_error",str(e))
        error = str(e)       
        
def exec_sql(sql,**args):
    res_code=0
    row_3=''
    try:
        conn=connect()
        cursor = conn.cursor()
        conn.commit()
        res_code=1
        cursor.execute(sql)
        row_3 = cursor.fetchall()
    except Exception as e:
        print("exec_sql execute fails:%s,%s" %(str(e),sql))
        res_code=0
        return res_code
    finally:
        cursor.close()
        conn.close()
        print("conn has chosed")
        return row_3
    
def exec_sql_args(sql,args):
    res_code=0
    row_3=''
    try:
        conn=connect()
        cursor = conn.cursor()
        conn.commit()
        res_code=1
        cursor.execute(sql,args)
        row_3 = cursor.fetchall()
        conn.commit()
    except Exception as e:
        print("exec_sql execute fails:%s,%s" %(str(e),sql))
        res_code=-1
        return res_code
    finally:
        cursor.close()
        conn.close()
        print("conn has chosed")
        return row_3
if __name__=='__main__':
#     args = ('ip','minion_id','kernel','osversion','cpu_model','num_cpus','manufacturer','osfullname','mem_total','windowsdomain','fqdn','os','cpuarch','roles','osrelease','kernelrelease','saltversion','osmanufacturer','saltpath','timezone','os_family','shell','username','domain')
#     print(format_args(args))
    conn=connect()
    cursor = conn.cursor()
    test='test'
    #sss = cursor.execute("select * from operation_record where user_name like %%s%"+('test2')  )
    sql = "select * from operation_record where user_name like '%%%%%s%%%%'"  
    t = 'test'
    aaa = exec_sql_args(sql, (t))
    sql = sql %("test")
    sss = exec_sql(sql)
    #sss = cursor.execute(sql)
    print(cursor.fetchall())
    print("结果",type(cursor.fetchall()))
    
    #sss = conn.execute("SELECT * FROM operation_record WHERE user_name LIKE ?", ('%'+'test'+'%',))
    print("sss",type(aaa),aaa)
#     #多个%s需要传参数为数组
#     #所以，在你只传递一个参数之前，一个包含所有参数的元组。
#     #args = ('112','db组','127.0.0.3', '127.0.0.5', '127.0.0.9', '127.0.0.9', '192.168.0.1')
#     data = {'group_id': '4', 'group_name': 'redis组', 'ip': ('127.0.0.3', '127.0.0.5', '127.0.0.9', '127.0.0.9', '192.168.0.1')}
#     #in_p=','.join(map(lambda x: '%s', args['ip']))
#     sql2 = 'update host set group_id=%s,group_name=%s where ip in '+format_args(data['ip'])#处理in后面（%s,s%,s%,s%,s%,s%,s%）
#     arg = (data['group_id'],data['group_name'],data['ip'])
#     args = ('4', 'redis组', '127.0.0.3', '127.0.0.5', '127.0.0.9', '127.0.0.9', '192.168.0.1')
#     
#     group_args=(data['group_id'],data['group_name'])
#     group_ip=(data['ip'])
#     args = group_args+group_ip#将两个tuple连起来
#     #取最后5个参数
#     cursor.execute(sql2,args)
#     conn.commit()
    '''insert into disk_usage(available,capacity,total,partition,used,ip,minion_id) values[%s,%s,%s,%s,%s,%s,%s)
    '''
    args=('172.17.39.208','ip','127000','172.17.39.96','192.168.174.133')
    args=['172.17.39.208', 'ip', '127000', '172.17.39.96', '192.168.174.133']
    format_args(args)
    #sql = "select minion_id from `host` where ip in" +format_args(args)
    data= [['/dev/sda1', '36690', '245435', '14%', '297485', '192.168.160.128', '192.168.160.128_oracledb'], 
         ['tmpfs', '124', '953328', '1%', '953452', '192.168.160.128', '192.168.160.128_oracledb'], 
         ['/dev/sda3', '19979704', '24888884', '45%', '47269816', '192.168.160.128', '192.168.160.128_oracledb']]
    #insert_table('disk_usage',data)
#     print(exec_sql_args(sql,args))
