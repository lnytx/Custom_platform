#-*- coding:utf-8 –*-
import os,os.path,time,datetime
import socket,sys
import re
import logging


'''
检测到日志中有死锁字样
并且在日志目录中如果当前时间减去文件最后文件修改时间之差大于15分钟时，没有生成别的文件（此时list为空）
上面两种情况就重启进程
'''

def CheckPort(IPStr,Port):
    Status='Ok';
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  ;
    try :
        sock1.connect((IPStr, Port));
    except socket.error , e:
       Status='Fail' ;
    
    
    if Status=='Ok' :
        return "1";
    else:
        return "0";
    sock1.close();

def GetLastFile(base_dir,MinGap):    
    def compare(x, y):#x,y在后面表示传入两个文件
        stat_x = os.stat(base_dir + "\\" + x)
        stat_y = os.stat(base_dir + "\\" + y)
        #st_mtime  文件最后修改时间
        if stat_x.st_mtime > stat_y.st_mtime:
            #0表示等于，正数表示大于
            return -1
        elif stat_x.st_mtime < stat_y.st_mtime:
            return 1
        else:
            return 0
    l=os.listdir(base_dir);#列出所有文件
    l.sort(compare);#按文件修改时间排序
    LastFileList=[]
    for i in l :
        File=base_dir + "\\" + i;
        File_stat=os.stat(File);
        #datetime.timedelta(hours=8)当前时间+8小时
        dt = datetime.datetime.utcfromtimestamp(File_stat.st_mtime) + datetime.timedelta(hours=8) ;#文件修改时间
        if (datetime.datetime.now() - dt).seconds <= MinGap :#与当前时间减最后修改时间之差小于15分钟，MinGap=900秒
            LastFileList.append(File);
        else:
             break;
    return LastFileList

def GetKeyLog(LogFile,Mykeyword):
    Outstate=0;
    f=open(LogFile,'r');
    fline=f.readlines();
    for line in fline:
        line = line.decode('UTF8');
        if re.search( Mykeyword , line) :
            print line;
            Outstate=1;
            break;
    f.close();
    return Outstate;

if __name__=="__main__":
    RestartSingle=0;#重启参数为1则重启
    TargList=["SUPERDRY门店POS销售数据上传","FP结算中心零售单主表","FP结算中心调整单主表","OCH结算中心零售单主表","OCH结算中心调整单主表","TD结算中心零售单主表","TD结算中心调整单主表"];
    WordDir="C:\\Program Files (x86)\\BAISON_PG\\MW-DI\\Log";
    TimeGap=900;#15分钟
    Key='死锁';
    Key=Key.decode('UTF8');
    BaseDir=os.path.split(os.path.realpath(__file__))[0];
    LogDIR=BaseDir+'\\Log';
    
    if not os.path.exists( LogDIR ) :
        os.mkdir(LogDIR);

    logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',  
                    datefmt='%m-%d %H:%M',  
                    filename=LogDIR+'\\JKWH.log',  
                    filemode='a') 
    console = logging.StreamHandler()  
    console.setLevel(logging.INFO)  
  
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')  
    console.setFormatter(formatter)  
  
    logging.getLogger('').addHandler(console)  
    Today = datetime.datetime.now();
    if len(str(Today.day)) == 1:
        suplite='0';
    else:
        suplite='';

    if len(str(Today.month)) == 1:
        msuplite='0';
    else:
        msuplite='';

    ToDir= str(Today.year)+ "-" + msuplite + str(Today.month) + "-" + suplite + str(Today.day);
    Beforday = datetime.datetime.now() - datetime.timedelta(days=1);

    if len(str(Beforday.day)) == 1:
        besuplite='0';
    else:
        besuplite='';
    if len(str(Beforday.month)) == 1:
        bemsuplite='0';
    else:
        bemsuplite='';

    BeDir= str(Beforday.year)+ "-" + bemsuplite + str(Beforday.month) + "-" + besuplite + str(Beforday.day);
    
    MyDirList=[];
    CheckFileList=[];
    for TmpDir in TargList:
        TmpDir=TmpDir.decode('UTF8');
        if os.path.exists( WordDir + '\\' + TmpDir + '\\' + ToDir ) :
            MyDirList.append( WordDir + '\\' + TmpDir + '\\' + ToDir );#加上目录为当前日期的log
        elif os.path.exists( WordDir + '\\' + TmpDir + '\\' + BeDir ) :
            MyDirList.append( WordDir + '\\' + TmpDir + '\\' + BeDir );

    
    for CheckDir in MyDirList:
        logging.info('Dir '+CheckDir.encode('GBK')+' will be checked ...');
        print CheckDir;
        CheckFileList=CheckFileList+GetLastFile(CheckDir,TimeGap)#将最后修改时间小于当前时间900秒的文件名存储进来
    
    for MyCheckLogFile in CheckFileList:
        if MyCheckLogFile is not None:
            logging.info('Checking log file '+ MyCheckLogFile.encode('GBK') + '...');
            if GetKeyLog(MyCheckLogFile,Key) == 1 :#key关键字前面定义为死锁
                RestartSingle=1;
                logging.info(MyCheckLogFile.encode('GBK')+' is checked dead lock ...');
                break;
    
    if Today.hour % 3==2 and Today.minute == 30 :#1,5,8,11,14,17,20,23点半
        for CheckDir in MyDirList:
            if GetLastFile(CheckDir,TimeGap*4*3) is None :#这里取相隔的时间为15分钟*12为3小时，时目录为空，则说明这段时间没有生成文件
                logging.info('Directory  '+CheckDir.encode('GBK')+' in the last 3 hour did not generate any file , try to restart app  ....');
                RestartSingle = 1;
                break;

    if CheckPort('127.0.0.1',8001)== "0" or CheckPort('127.0.0.1',8003)== "0":
        logging.info('JK app port 8001/8003 is down ....');
        RestartSingle=1;

    if RestartSingle == 1:
        logging.info('Retart restart JK app...');
        os.system("taskkill /im IControl.exe /f");#kill进程
        os.system("taskkill /im WCFHost.exe /f");
        os.system("taskkill /im WCFHostHelper.exe /f");
        os.popen('cmd.exe /c "D:\\WH\\StartWCHost.vbs"');#启动进程
    else:
        logging.info('JK app is running well ...') ;
