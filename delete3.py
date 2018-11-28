#-*- coding:utf-8 –*-
import os,os.path,datetime
import sys,shutil,ctypes
import logging

def PrepareDir(MyDIR):
    if not os.path.exists(MyDIR):
        os.mkdir(MyDIR);
def CheckFreeSpace(DiskName):
    free_bytes = ctypes.c_ulonglong(0);
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(DiskName), None, None, ctypes.pointer(free_bytes));
    if free_bytes.value / 1024 / 1024 < 512 :
        return 0;
    else:
        return 1;

def GetSourcePathList(LogPath,DayTime):
    BackupDir_List=[];
    l = os.listdir(LogPath);
    for tmpdir in l:
        subLogpath=LogPath+"\\"+tmpdir+"\\"+DayTime;
        if os.path.isdir(subLogpath) and os.path.exists(subLogpath):
            SubLogPair=[subLogpath,tmpdir];
            BackupDir_List.append(SubLogPair);
    return BackupDir_List;

def MoveAndBackup(FromDir,TargetDir):
    StopState=1;
    PrepareDir(FromDir);
    PrepareDir(TargetDir);
    MoveFileList=os.listdir(FromDir);
    for MoveFile in MoveFileList:
        try:
            shutil.move(FromDir+"\\"+MoveFile,TargetDir+"\\"+MoveFile);
        except OSError:
            if CheckFreeSpace(TargetDir.split(':')+'\\') == 0:
                StopState=0;
                break
        else:
            StopState=1;
    if StopState==1:
        shutil.rmtree(FromDir);
    return StopState;

def CompressDir(RARPath,SourceDir):
    StopState=1;
    if os.path.exists(SourceDir):
        try :
            os.popen(RARPath+" a -df "+SourceDir+".rar "+SourceDir);
        except OSError:
            if CheckFreeSpace(SourceDir.split(':') + '\\') == 0:
                StopState = 0;
        else:
            StopState = 1;
    return StopState;

if __name__=="__main__":
    LogSourcePath='C:\\Program Files (x86)\\BAISON_PG\\MW-DI\\Log';
    LogBackupPath='E:\\LOG_BACKUP';
    RarPath='C:\\"Program Files (x86)"\\WinRAR\\rar';
    ExitSingle=1;
    WHLogPath=os.path.split(os.path.realpath(__file__))[0]+'\\Log';

    Beforday=datetime.datetime.now() - datetime.timedelta(days=1);
    if len(str(Beforday.day)) == 1:
        besuplite='0';
    else:
        besuplite='';

    if len(str(Beforday.month)) == 1:
        msuplite='0';
    else:
        msuplite='';    
    BackupDate=str(Beforday.year)+ "-" + msuplite + str(Beforday.month) + "-" + besuplite + str(Beforday.day);

    if sys.argv[1] is not None :
        BackupDate=sys.argv[1];

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=WHLogPath + '\\WH_file_Backup.log',
                        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)

    logging.info('Start Backup ' + LogSourcePath + ', data date is BackupDate ...');

    PrepareDir(LogBackupPath+"\\"+BackupDate);

    for BackupPair in GetSourcePathList(LogSourcePath,BackupDate):
        TmpTargetPath=LogBackupPath+"\\"+BackupDate+"\\"+BackupPair[1];
        if MoveAndBackup(BackupPair[0],TmpTargetPath) == 0:
            ExitSingle=0;
            logging.error('Bckup File '+BackupPair[0]+ ' to '+TmpTargetPath+' fail , program will exit ...');
            break;
        else:
            logging.info('Bckup File '+BackupPair[0]+ ' to '+TmpTargetPath+' success ...');

    if CompressDir(RarPath,LogBackupPath+"\\"+BackupDate)==0:
        ExitSingle = 0;
        logging.info('Compress File ' + RarPath + ' Fail ...');
    else:
           logging.info('Compress File ' + RarPath + ' success ...');

    if ExitSingle==0:
        logging.info(' Backup data in ' + LogSourcePath + ' fail  ...');
        exit(1);
    else :
        logging.info(' Backup data in ' + LogSourcePath + ' success  ...');
        exit(0);
