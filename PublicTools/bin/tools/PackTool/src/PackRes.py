# -*- coding: utf-8 -*-

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
from util import xxtea
from util import PackXXTea, PackLua, RemoveUtf8Bom, PackImg2Mng_ETC

threadPool = ThreadPoolExecutor(1)

projectdir = os.path.dirname(os.path.realpath(__file__))

errorFils = []

def _compileLuaJit(tid, absFilePath, relativepath):
    print("[线程%02d] 编译: %s" % (tid, relativepath))
    ret = PackLua.compile(absFilePath, relativepath)
    if ret != 0:
        errorFils.append(relativepath)
    return ret == 0

def _XXTeaEncode(tid, absFilePath, relativepath):
    print("[线程%02d] 加密: %s" % (tid, relativepath))
    
    ret = PackXXTea.encode(absFilePath)
        
    return ret == 0
 
def _convertImage(tid, absFilePath, relativepath):
    print("[线程%02d] 转换: %s" % (tid, relativepath))
    ret = PackImg2Mng_ETC.convert(absFilePath)
    
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
            
        self.taskQueue = Queue()
    
    def start(self):
        if self.isOK:
            threadPool.submit(self.process)
        else:
            print("路径错误, 请重试...")
    
    def process(self):
        for r, d, fileList in os.walk(self.dir) :
            for file in fileList :
                absFilePath = os.path.join(r, file)
                self._FileCat(absFilePath)
        errorQueue = queueProcess(self.taskQueue, os.cpu_count() * 5)
        
        if len(errorFils) > 0:
            print("This files ocurs ERROR:")
            for file in errorFils:
                print('\t' + file)
                
        print("Compeleted.")
        os.system('pause')
        return not errorQueue.empty()
 
    '''
        文件分类
    '''
    def _FileCat(self, absFilePath):   
        realpath = absFilePath.replace(self.dir, '')
        if absFilePath[-4:] == '.lua' :
            self.taskQueue.put((_compileLuaJit, absFilePath, realpath))
        elif absFilePath.find(".xml") != -1 :
            self.taskQueue.put((_XXTeaEncode, absFilePath, realpath))
        elif absFilePath.find(".png") != -1 :
            self.taskQueue.put((_convertImage, absFilePath, realpath))
        elif absFilePath.find(".jpg") != -1 :
            self.taskQueue.put((_convertImage, absFilePath, realpath))
        
  
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
finally:
    pass