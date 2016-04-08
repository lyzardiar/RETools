#coding=utf-8

'''
Created on 2016年4月8日

@author: yun.bo
'''

from concurrent.futures.thread import ThreadPoolExecutor
from distutils import dir_util
from functools import cmp_to_key
from queue import Queue
import hashlib
import sys
import traceback
import os
import re
import shutil

from process import queueProcess, execCmd
from util import Log

threadPool = ThreadPoolExecutor(1)

projectdir = os.path.dirname(os.path.realpath(__file__))
LuaJitBin = os.path.join(projectdir, "../../bin/win32/luajit.exe")

JitCompileCMD = LuaJitBin + " -b {filename} {filename}" 

def _compileLuaJit(tid, absFilePath) :
    print("[线程%d] 编译: %s" % (tid, absFilePath))
    ret = execCmd(JitCompileCMD.format(filename = absFilePath))
    return ret == 0

class PackLuajit(object):
    '''
    classdocs
    '''

    def __init__(self, fileDir):
        '''
        Constructor
        '''
        self.isOK = True
        
        self.dir = fileDir
        if self.dir is None :
            self.isOK = False
    
    def start(self):
        if self.isOK:
            threadPool.submit(self.process)
        else:
            print("路径错误, 请重试...")
    
    def process(self):
        taskQueue = Queue()
        for r, d, fileList in os.walk(self.dir) :
            for file in fileList :
                absFilePath = os.path.join(r, file)
                if absFilePath.find(".lua") != -1 :
                    taskQueue.put((_compileLuaJit, absFilePath))
        errorQueue = queueProcess(taskQueue, os.cpu_count() * 5)
        print("Compeleted.")
        return not errorQueue.empty()
    
  
try:
    if len(sys.argv) > 1:
        print("start compile...")
        jit = PackLuajit(sys.argv[1])
        jit.start()
    else:
        print("use PackLuaJit {dir} to compile...")

except :
    t, v, tb = sys.exc_info()
    print(t, v)