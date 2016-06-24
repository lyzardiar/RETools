# -*- coding: utf-8 -*-

'''
Created on 2016年4月8日

@author: yun.bo
'''

from concurrent.futures.thread import ThreadPoolExecutor
from distutils import dir_util
from functools import cmp_to_key

import multiprocessing
import queue
import hashlib
import sys
import traceback
import os
import re
import shutil
import time

from process import queueProcess, queueThread, execCmd

from util import Log
from util.data import xxtea, PackXXTea, PackMap, RemoveUtf8Bom
from util.lua.PackLua import PackLua
from util.image.PackImage import PackImage


useThread = False

if useThread:
    from process.thread.ThreadWork import Task
    from process.thread.ThreadWork import Work
else:
    from process.thread.ProcessWork import Task
    from process.thread.ProcessWork import Work

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
        self.file_count = 0
        self.file_tot_count = 0
        
        self.work = Work(count=os.cpu_count())
 
        self.errorFils = []        
        
        if self.dir is None :
            self.isOK = False
        
        if self.platform == 'iOS':
            self.luaPacker = PackLua(True, True)
            self.imgPacker = PackImage(True)
        else:
            self.luaPacker = PackLua(True, False)
            self.imgPacker = PackImage(False)
    
    def start(self):
        if self.isOK:
            self.process()
        else:
            Log.printDetailln("路径错误, 请重试...")
    
    def process(self):
        tstart = time.clock()

        if not os.path.isdir(self.dir):
            if self._FileCat(os.path.realpath(self.dir)):
                self.file_tot_count = self.file_tot_count + 1
        else:
            for r, d, fileList in os.walk(self.dir) :
                for file in fileList :
                    absFilePath = os.path.join(r, file)
                    if self._FileCat(absFilePath):
                        self.file_tot_count = self.file_tot_count + 1

        Log.printDetailln("%d Files loaded Completed, Compiling..." % (self.file_tot_count))         
        
        self.work.start(self.file_tot_count)
        self.work.join()
        
        tend = time.clock()

        errs = self.work.errs
        if not errs.empty():
            Log.printDetailln("This files ocurs ERROR:")
            while not errs.empty():
                task = errs.get()
                absFilePath, realpath, *args = task.param
                Log.printDetailln('\t', realpath)

        Log.printDetailln("\n\nCompeleted in %.3fs." % (tend - tstart))
        
        if len(self.imgPacker.passFiles) > 0 :
            Log.printDetailln("Pass Files:")
            for passfile in self.imgPacker.passFiles:
                Log.printDetailln('\t' + passfile)

        return True
        
 
    '''
        文件分类
    '''
    def _FileCat(self, absFilePath):   
        realpath = absFilePath.replace(self.dir, '')
        
        ret = True

        if absFilePath[-4:] == '.lua' :
            self.work.putTask(Task(target=task_compileLuaJit2, args=(absFilePath, realpath, self.luaPacker, self.file_tot_count + 1)))
        elif absFilePath.find(".xml") != -1 :
            self.work.putTask(Task(target=task_XXTeaEncode2, args=(absFilePath, realpath, self.file_tot_count + 1)))
        elif absFilePath.find(".png") != -1 :
            self.work.putTask(Task(target=task_convertImage2, args=(absFilePath, realpath, self.imgPacker, self.file_tot_count + 1)))
        elif absFilePath.find(".jpg") != -1 :
            self.work.putTask(Task(target=task_convertImage2, args=(absFilePath, realpath, self.imgPacker, self.file_tot_count + 1)))
        elif absFilePath.find(".map") != -1 :
            self.work.putTask(Task(target=task_convertMap2, args=(absFilePath, realpath, self.file_tot_count + 1)))
        else:
            ret = False
        return ret
    
def task_compileLuaJit2(tid, taskTotSize, absFilePath, relativepath, luaPacker, taskSize):
    ret = luaPacker.compile(absFilePath, relativepath)

    Log.printDetailln("编译[%d/%d]: %s" % (taskSize, taskTotSize, relativepath))

    return ret == 0

def task_XXTeaEncode2(tid, taskTotSize, absFilePath, relativepath, taskSize):   
    ret = PackXXTea.encode(absFilePath)
    
    Log.printDetailln("加密[%d/%d]: %s" % (taskSize, taskTotSize, relativepath)) 

    return ret == 0

def task_convertImage2(tid, taskTotSize, absFilePath, relativepath, imgPacker, taskSize):   
    ret = imgPacker.convert(absFilePath) 
    
    Log.printDetailln("转换[%d/%d]: %s" % (taskSize, taskTotSize, relativepath)) 

    return ret == 0 
    
def task_convertMap2(tid, taskTotSize, absFilePath, relativepath, taskSize):
    ret = PackMap.convert(absFilePath) 
    
    Log.printDetailln("转换[%d/%d]: %s" % (taskSize, taskTotSize, relativepath))

    return ret == 0 