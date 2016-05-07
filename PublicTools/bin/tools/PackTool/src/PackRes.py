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
from util import PackXXTea, PackLua, RemoveUtf8Bom, PackImage

threadPool = ThreadPoolExecutor(1)

projectdir = os.path.dirname(os.path.realpath(__file__))      
    
class PackRes(object):
    '''
    classdocs
    '''

    def __init__(self, fileDir, platform = 'iOS'):
        '''
        Constructor
        '''
        self.isOK = True
        self.platform = platform
        
        self.dir = fileDir
            
        self.taskQueue = Queue()
 
        self.errorFils = []
        
        
        if self.dir is None :
            self.isOK = False
            
        if self.platform == 'iOS':
            PackLua.updateCMD(True, True)
            PackImage.updateCMD(True)
        else:
            PackLua.updateCMD(True, False)
            PackImage.updateCMD(False)
    
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
        
        if len(self.errorFils) > 0:
            print("This files ocurs ERROR:")
            for file in self.errorFils:
                print('\t' + file)
                
        print("Compeleted.")
        
        if len(PackImage.passFiles) > 0 :
            print("Pass Files:")
            for passfile in PackImage.passFiles:
                print('\t' + passfile)
        os.system('pause')
        return not errorQueue.empty()
        
 
    '''
        文件分类
    '''
    def _FileCat(self, absFilePath):   
        realpath = absFilePath.replace(self.dir, '')
        if absFilePath[-4:] == '.lua' :
            self.taskQueue.put((self._compileLuaJit, absFilePath, realpath))
        elif absFilePath.find(".xml") != -1 :
            self.taskQueue.put((self._XXTeaEncode, absFilePath, realpath))
        elif absFilePath.find(".png") != -1 :
            self.taskQueue.put((self._convertImage, absFilePath, realpath))
        elif absFilePath.find(".jpg") != -1 :
            self.taskQueue.put((self._convertImage, absFilePath, realpath))

    def _compileLuaJit(self, tid, absFilePath, relativepath):
        print("[线程%02d] 编译: %s" % (tid, relativepath))
        ret = PackLua.compile(absFilePath, relativepath)
        if ret != 0:
            self.errorFils.append(relativepath)
        return ret == 0

    def _XXTeaEncode(self, tid, absFilePath, relativepath):
        print("[线程%02d] 加密: %s" % (tid, relativepath))
        
        ret = PackXXTea.encode(absFilePath)
            
        return ret == 0
    
    def _convertImage(self, tid, absFilePath, relativepath):
        print("[线程%02d] 转换: %s" % (tid, relativepath))
        
        ret = PackImage.convert(absFilePath) 
        return ret == 0 