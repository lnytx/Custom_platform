#-*- coding:utf-8 –*-
import os,os.path,time,datetime
import socket,sys
import re
import logging

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
    def compare(x, y):
        stat_x = os.stat(base_dir + "\\" + x)
        stat_y = os.stat(base_dir + "\\" + y)
        if stat_x.st_mtime > stat_y.st_mtime:
            return -1
        elif stat_x.st_mtime < stat_y.st_mtime:
            return 1
        else:
            return 0
    l=os.listdir(base_dir);
    l.sort(compare);
    LastFileList=[]
    for i in l :
        File=base_dir + "\\" + i;
        File_stat=os.stat(File);
        dt = datetime.datetime.utcfromtimestamp(File_stat.st_mtime) + datetime.timedelta(hours=8) ;
        if (datetime.datetime.now() - dt).seconds <= MinGap :
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
            #print line;
            Outstate=1;
            break;
    f.close();
    return Outstate;

if __name__=="__main__":
    RestartSingle=0;
    TargList=["SUPERDRY门店POS销售数据上传","FP结算中心零售单主表","FP结算中心调整单主表","OCH结算中心零售单主表","OCH结算中心调整单主表","TD结算中心零售单主表","TD结算中心调整单主表","M60券实时联动","TRENDY券实时联动"];
    WordDir="C:\\Program Files (x86)\\BAISON_PG\\MW-DI\\Log";
    TimeGap=900;
    Key='死锁';
    Key=Key.decode('UTF8');
    BaseDir=os.path.split(os.path.realpath(__file__))[0];
    LogDIR=BaseDir+'\\Log';
    
    if not os.path.exists( LogDIR ) :
        os.mkdir(LogDIR);

    logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',  
                    datefmt='%m-%d %H:%M',  
                    filename=LogDIR+'\\JKWH_wh.log',  
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
            MyDirList.append( WordDir + '\\' + TmpDir + '\\' + ToDir );
        elif os.path.exists( WordDir + '\\' + TmpDir + '\\' + BeDir ) :
            MyDirList.append( WordDir + '\\' + TmpDir + '\\' + BeDir );

    
    for CheckDir in MyDirList:
        logging.info('Dir '+CheckDir.encode('GBK')+' will be checked ...');
        print CheckDir;
        CheckFileList=CheckFileList+GetLastFile(CheckDir,TimeGap)
    
    for MyCheckLogFile in CheckFileList:
        if MyCheckLogFile is not None:
            logging.info('Checking log file '+ MyCheckLogFile.encode('GBK') + '...');
            if GetKeyLog(MyCheckLogFile,Key) == 1 :
                RestartSingle=1;
                logging.info(MyCheckLogFile.encode('GBK')+' is checked dead lock ...');
                break;

    logging.info("now time"+str(Today.minute).encode('GBK'));
    #if Today.hour % 3==2 and Today.minute == 30 :
    if Today.minute >= 30:
    logging.info("exec_time"+str(Today.minute).encode('GBK'));
        for CheckDir in MyDirList:
            '''
            列表为空时表示在与TimeGap时间间隔内没有生成文件
            '''
            if GetLastFile(CheckDir,TimeGap*4*3) is None or GetLastFile(CheckDir,TimeGap*4*3)==[] :
                logging.info('Directory  '+CheckDir.encode('GBK')+' in the last 3 hour did not generate any file , try to restart app  ....');
                RestartSingle = 1;
                break;

    if CheckPort('127.0.0.1',8001)== "0" or CheckPort('127.0.0.1',8003)== "0":
        logging.info('JK app port 8001/8003 is down ....');
        RestartSingle=1;

    if RestartSingle == 1:
        logging.info('Retart restart JK app...');
        os.system("taskkill /im IControl.exe /f");
        os.system("taskkill /im WCFHost.exe /f");
        os.system("taskkill /im WCFHostHelper.exe /f");
        os.popen('cmd.exe /c "D:\\WH\\StartWCHost.vbs"');
    else:
        logging.info('JK app is running well ...') ;
