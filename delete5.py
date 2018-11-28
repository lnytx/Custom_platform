#-*- coding:utf-8 –*-
from _functools import cmp_to_key
import datetime
import logging
import os, os.path
import re
import socket, sys


def GetLastFile(base_dir,MinGap):    
    print("base_dir",base_dir)
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
    print("l",l)
    key = cmp_to_key(compare)
    l.sort(key=key);
    l.reverse()
    print("ll",l)#32-a5a5-47157034f119.txt'
    LastFileList=[]
    for i in l :
        print("i",i)
        File=base_dir + "\\" + i;
        print("file",File)
        File_stat=os.stat(File);
        print("File_stat",File_stat)#st_mtime是文件的最后的修改时间
        dt = datetime.datetime.utcfromtimestamp(File_stat.st_mtime) + datetime.timedelta(hours=8) ;
        print("dt",type(dt),dt)
#         2018-03-18 23:57:36.343306
        a = '2018-03-18 06:01:01'
        b = datetime.datetime.strptime("2018-03-18 00:01:01.917782", "%Y-%m-%d %H:%M:%S")
        dt = datetime.datetime.strptime(datetime.datetime.utcfromtimestamp(File_stat.st_mtime) + datetime.timedelta(hours=8),"%Y-%m-%d %H:%M:%S")
        print("dt2",type(dt),dt)
        print("b",type(b),b)
        print("datetime.datetime.now()",datetime.datetime.now())
        print("(b - dt).seconds",(b - dt).seconds)
#         if (datetime.datetime.now() - dt).seconds <= MinGap :
        if (b - dt).seconds <= MinGap :#当前时间与第一个文件的最后时间相减
            LastFileList.append(File);
            print("ssss")
        else:
            print("break")
            break;
    print("LastFileList",LastFileList)
    #文件时间从晚到早排序，第一个为当天的24点 最后一个为当天的0点
    return LastFileList

if __name__=="__main__":
    dir = "d:\\2018-03-18"
    MinGap = 900
    print(GetLastFile(dir,MinGap))
    if GetLastFile(dir,MinGap)==[]:
        print("为空")