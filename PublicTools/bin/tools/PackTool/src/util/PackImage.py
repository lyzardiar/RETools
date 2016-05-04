# -*- coding: utf-8 -*- 

import os
import os.path
import shutil
import sys
import getopt
import string  
import fnmatch
import hashlib
import hashlib
import zipfile
import time
import threading
import struct
from pprint import pprint
from struct import *

from util import PackImg2Mng_ETC, PackImg2Mng_PVR, PackImgJPG

ERROR = 1
PASS = 2

GZIP = 3
PKM = 4
MNG = 5

GzipCnt = 0
MngCnt = 0
PkmCnt = 0
PassCnt = 0

isIOS = False
    

passFiles = []

filters = ["crater"] 


TC4Module = []
DTC4Module = []
RGB_JPGModule = []
JPGModule = []

def updateCMD(_isIOS = True): 
    global isIOS
    global TC4Module, DTC4Module, RGB_JPGModule, JPGModule
    
    isIOS = _isIOS
    
    if isIOS:
        TC4Module = [ "/bomb/", "\\bomb\\", "/unit/", "\\unit\\", "/living/", "\\living\\" ]
        DTC4Module = [ "/show/", "\\show\\", "/effect/", "\\effect\\", "/fight/", "\\fight\\" ]
        RGB_JPGModule = [  ]
        JPGModule = [  ]
    else:
        TC4Module = [  ]
        DTC4Module = [  ]
        RGB_JPGModule = [ "/gj/", "\\gj\\" ]
        JPGModule = [  ]
 
updateCMD()   
   
def work(filename):    
    global GzipCnt, MngCnt, PkmCnt, PassCnt, filters
    filepath = os.path.realpath(filename)
   
 
    for filtername in filters:
        if filepath.find(filtername) != -1:
            PassCnt = PassCnt + 1
            passFiles.append(filename)
            return 2
    
    with open(filepath, 'rb') as tmpFile:
        tmpContent = tmpFile.read(3)
        if tmpContent[0:2] == b'\x1f\x8b':
            print ("Gzip File, pass.")
            GzipCnt = GzipCnt + 1
            return
        if tmpContent == b"MNG":
            print ("MNG File, pass.")
            MngCnt = MngCnt + 1
            return
        if tmpContent == b"PKM":
            print ("PKM File, pass.")
            PkmCnt = PkmCnt + 1
            return
         
    isAlphaJPG = False
    isTC4 = False
    isDTC4 = False
   
    for filtername in TC4Module:
        if filepath.find(filtername) != -1:
            isTC4 = True 
            break
   
    for filtername in DTC4Module:
        if filepath.find(filtername) != -1:
            isDTC4 = True 
            break
   
    for filtername in RGB_JPGModule:
        if filepath.find(filtername) != -1:
            isAlphaJPG = True 
            break       
    
    isPng = True
    if filename.find(".png") != -1:
        isPng = True
    elif filename.find(".jpg") != -1:
        isPng = False
        
    ret = 0
    if isIOS:
        ret = PackImgJPG.convert(filepath, isPng)
        # if isPng:
        #     if isDTC4:   
        #         ret = PackImg2Mng_PVR.convert(filepath)
        #         if ret == 2:
        #             ret = PackImgJPG.convert(filepath, isPng)
        #     elif isTC4:
        #         ret = PackImg2Mng_PVR.convert(filepath, isAlphaJPG, isTC4)
        #         if ret == 2:
        #             ret = PackImgJPG.convert(filepath, isPng)
        # else:
        #     ret = PackImgJPG.convert(filepath, isPng)
    else:
        ret = PackImg2Mng_ETC.convert(filepath, isAlphaJPG)    
    
    if ret == 1:
        print("ocurr Error")
        passFiles.append(filepath)
        
    elif ret == 2:
        PassCnt = PassCnt + 1
        passFiles.append(filepath)
    elif ret == 3:
        GzipCnt = GzipCnt + 1
    elif ret == 4:
        PkmCnt = PkmCnt + 1
    elif ret == 5:
        MngCnt = MngCnt + 1   
             
    return ret
    
    
    
def convert(filename):
    ret = work(filename)
    return ret