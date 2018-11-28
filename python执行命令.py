'''
Created on 2017年8月16日

@author: ning.lin
'''
import paramiko


#根据提供的参数使用ssh连接到对应机器   
def ssh_connect_command(logfile,ip,port,username,password,command):
    no_con_server=[]
    try:
        ssh = paramiko.SSHClient()
        paramiko.util.log_to_file(logfile)
        #允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("ip+端口",ip,port)
        ssh.connect(ip, int(port),username, password,timeout=1)
        try:
            stdin,stdout,stderr = ssh.exec_command(command)
            channel = stdout.channel
            status = channel.recv_exit_status()
            print("status",status)
            if status==0:
                print("已经连接到该主机%s:%s，%s命令执行成功" %(ip,port,command))
                #打印执行的命令
                text=stdout.read().decode('utf-8')
                print ("text",type(text),text)
            else:
                print("执行命令%s报错,请查看日志"% (status,logfile))
                print (stderr.read().decode('utf-8'))
                sessions=ip+":"+port
                #执行命令异常的IP写入到数据库，这里是写入到一个配置文件中
        except Exception as e:
            print ("执行命令%s时报错，请看日志" % command,logfile,'\n',stderr.read().decode('utf-8'))
            sessions=ip+":"+port
            #执行命令异常的IP写入到数据库，这里是写入到一个配置文件中
    except Exception as e:
        print ("连接%s:%s时报错，请查看日志%s" % (ip,port,logfile),str(e),'\n')
        #记录IP加端口，将其写入未连接成功的配置文件中
        sessions=ip+":"+port
        #将连接异常的IP写入到数据库，这里是写入到一个配置文件中
if __name__ == '__main__':
    logfile='ssh_loggin.log'
    cmd='''
    salt '*' file.replace d:/1012/temp/1.txt pattern='sdf' repl='AAAAA'  backup='.bak' append_if_not_found='True'
    '''
    print(ssh_connect_command(logfile,'192.168.174.128','22','root','root',cmd))