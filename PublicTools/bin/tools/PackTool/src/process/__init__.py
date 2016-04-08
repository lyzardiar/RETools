#coding=utf-8  

from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
import os
from queue import Queue, Empty
import subprocess
import sys
import traceback

from util import Log
from util.Constant import VERSION_TYPE_PLATFORM, VERSION_TYPE_MILESTONE
from util.Scanner import FileScanner


class Context:
    
    def __init__(self):
        self.rootPath = ''
        self.lastReleasePath = ''
        self.curScanner = FileScanner()
        self.folderPackList = []
        
        self.resPath = ''
        self.platformType = 0
        self.isNew = False
        self.isFull = False
        
        self.datetime = datetime.now().strftime('%Y%m%d%H%M%S')
    
    def getDataFolder(self):
        return self.rootPath + os.sep + 'data'
    
    def getReleaseOutputPath(self):
        return self.getDataFolder() + os.sep + self.datetime
    
    def getOutputPath(self):
        return self.rootPath + os.sep + 'output'
    
    def getOutputResPath(self):
        return self.getOutputPath() + os.sep + 'res'
    
    def getTempPath(self):
        return self.rootPath + os.sep + 'temp'
    
    def getBakPath(self):
        return self.rootPath + os.sep + 'bak'
    
    def getExportPath(self):
        return self.rootPath + os.sep + 'export'
    
def queueProcess(queue, tcnt=4):
    errorQueue = Queue()
    #threads = os.cpu_count();
    threads = tcnt;
    print('threads : ' + str(threads))
    with ThreadPoolExecutor(threads) as pool :
        for i in range(1, threads + 1) :
            pool.submit(run, i, queue, errorQueue)
    return errorQueue

def run(tid, queue, errorQueue):
    try:
        while True:
            func, *args = queue.get_nowait()
            if not func(tid, *args) :
                errorQueue.put((func, *args))
    except Empty:
        pass
    except :
        t, v, tb = sys.exc_info()
        print(t, v)
        traceback.print_tb(tb)
        Log.printDetailln('线程异常,' + str(sys.exc_info()))
    finally :
        Log.printDetailln('线程结束, tid : ' + str(tid))

def execCmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Log.printDetailln(str(p.stdout.read(), encoding='utf-8'))
    return p.wait()
