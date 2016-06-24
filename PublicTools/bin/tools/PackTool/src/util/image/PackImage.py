# -*- coding: utf-8 -*- 

import os
import os.path
import shutil
import sys
import getopt
import string  
import fnmatch
import hashlib
import zipfile
import time
import threading
import struct
from pprint import pprint
from struct import *

from util.image import PackImg2Mng_ETC, PackImg2Mng_PVR, PackImgJPG

from util import Log

class PackImage():

    def __init__(self, isIOS = True):
        self.ERROR = 1
        self.PASS = 2

        self.GZIP = 3
        self.PKM = 4
        self.MNG = 5

        self.GzipCnt = 0
        self.MngCnt = 0
        self.PkmCnt = 0
        self.PassCnt = 0

        self.isIOS = isIOS
            

        self.passFiles = []

        self.filters = ["crater"] 


        self.TC4Module = []
        self.DTC4Module = []
        self.RGB_JPGModule = []
        self.JPGModule = []

        self.updateCMD(isIOS)

    def updateCMD(self, isIOS = True): 
        self.isIOS = isIOS
        
        if self.isIOS:
            self.TC4Module = []
            self.DTC4Module = [ "/show/", "\\show\\", "/fight/", "\\fight\\" ]
            self.RGB_JPGModule = [  ]
            self.JPGModule = [  ]
        else:
            self.TC4Module = [  ]
            self.DTC4Module = [  ]
            self.RGB_JPGModule = [ "/gj/", "\\gj\\" ]
            self.JPGModule = [  ]
    
    def work(self, filename):    
        filepath = os.path.realpath(filename)    
    
        for filtername in self.filters:
            if filepath.find(filtername) != -1:
                self.PassCnt = self.PassCnt + 1
                self.passFiles.append(filename)
                return 2
        
        with open(filepath, 'rb') as tmpFile:
            tmpContent = tmpFile.read(3)
            if tmpContent[0:2] == b'\x1f\x8b':
                Log.printDetailln("Gzip File, pass.")
                self.GzipCnt = self.GzipCnt + 1
                return
            if tmpContent == b"MNG":
                Log.printDetailln("MNG File, pass.")
                self.MngCnt = self.MngCnt + 1
                return
            if tmpContent == b"PKM":
                Log.printDetailln("PKM File, pass.")
                self.PkmCnt = self.PkmCnt + 1
                return
            
        isAlphaJPG = False
        isTC4 = False
        isDTC4 = False
    
        for filtername in self.TC4Module:
            if filepath.find(filtername) != -1:
                isTC4 = True 
                break
    
        for filtername in self.DTC4Module:
            if filepath.find(filtername) != -1:
                isDTC4 = True 
                break
    
        for filtername in self.RGB_JPGModule:
            if filepath.find(filtername) != -1:
                isAlphaJPG = True 
                break       
        
        isPng = True
        if filename.find(".png") != -1:
            isPng = True
        elif filename.find(".jpg") != -1:
            isPng = False
            
        ret = 0
        if self.isIOS:
            if isPng:        
                ret = PackImg2Mng_PVR.convert(filepath, self.DTC4Module)
                if ret == 2:
                    ret = PackImgJPG.convert(filepath, isPng)
            else:
                ret = PackImgJPG.convert(filepath, isPng)
        else:
            ret = PackImg2Mng_ETC.convert(filepath, isAlphaJPG)    
        
        if ret == 1:
            Log.printDetailln("ocurr Error")
            self.passFiles.append(filepath)
            
        elif ret == 2:
            self.PassCnt = self.PassCnt + 1
            self.passFiles.append(filepath)
        elif ret == 3:
            self.GzipCnt = self.GzipCnt + 1
        elif ret == 4:
            self.PkmCnt = self.PkmCnt + 1
        elif ret == 5:
            self.MngCnt = self.MngCnt + 1   
                
        return ret        
        
    def convert(self, filename):
        ret = self.work(filename)
        return 0