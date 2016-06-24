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
import platform
from pprint import pprint
from struct import *

from util import toolsPath, Log
from util import FileHelper
            

gzipBin = FileHelper.gzipBin
convertBin = FileHelper.convertBin
pvrTexToolBin = FileHelper.pvrTexToolBin

isUseGzip = True
isSaveTransFile = False

RGBMode = "ETC"

def work_file_ETC(filename, isAlphaJPG = False, isFast = False):
    filepath = FileHelper.realpath(filename)
    filedir = FileHelper.dirname(filepath)

    sys.stdout.flush() 

    #preAlpha = needPreAplha(filedir)
    preAlpha = False
    preCMD = " -p "
    if not preAlpha:
        preCMD = ""
            
    os.chdir(toolsPath)
    
    isPng = True
    if filename.find(".png") != -1:
        isPng = True
    elif filename.find(".jpg") != -1:
        isPng = False
    else:
        return 2
    
    if isFast:
        quality = 'etcfast'
    else:
        quality = 'etcslow'

    rgbCMD = """ %s -f ETC1 %s -q %s -i %s -o %s """ % (pvrTexToolBin, preCMD, quality, filepath, filepath.replace(".png", ".pvr"))
    alphaCMD = """%s %s -alpha extract %s """ % (convertBin, filepath, filepath.replace(".png", ".alpha.jpg"))
    alphaJPGCMD = """ %s -f ETC1 -q %s -i %s -o %s """ % (pvrTexToolBin, quality, filepath.replace(".png", ".alpha.jpg"), filepath.replace(".png", ".alpha.pvr"))
    
    try:   
        if isPng:
            FileHelper.remove(filepath.replace(".png", ".pkm"))
            FileHelper.remove(filepath.replace(".png", "_alpha.pkm"))
        
            os.system(rgbCMD) 
            os.system(alphaCMD) 
            
            if not isAlphaJPG:
                os.system(alphaJPGCMD) 

            FileHelper.rename(filepath.replace(".png", ".pvr"), filepath.replace(".png", ".pkm"))   
            
            if isAlphaJPG:
                FileHelper.rename(filepath.replace(".png", ".alpha.jpg"), filepath.replace(".png", "_alpha.pkm")) 
            else:
                FileHelper.rename(filepath.replace(".png", ".alpha.pvr"), filepath.replace(".png", "_alpha.pkm")) 

            FileHelper.remove(filepath.replace(".png", ".alpha.jpg"))
            FileHelper.remove(filepath.replace(".png", ".alpha.pvr"))            
        else:    
            FileHelper.remove(filepath.replace(".jpg", ".pkm"))         
            rgbCMD = """ %s -f ETC1 -p -q %s -i %s -o %s """ % (pvrTexToolBin, quality, filepath, filepath.replace(".jpg", ".pvr"))
            os.system(rgbCMD)
            FileHelper.rename(filepath.replace(".jpg", ".pvr"), filepath.replace(".jpg", ".pkm"))  
        
    except Exception:
        t, v, tb = sys.exc_info()
        Log.printDetailln(t, v)
        pass
    finally:
        pass
  
    if isPng:   
        tmpfilename = filepath.replace(".png", ".tmp")
        FileHelper.remove(tmpfilename)
        
        isSuccess = True
        with open(tmpfilename, 'wb+') as tmpFile:
            try: 
                tmpFile.write(b'MNG')
                
                rgbname = filepath.replace(".png", ".pkm") 
                alphaname = filepath.replace(".png", "_alpha.pkm") 
                
                FileHelper.writeWithSize(tmpFile, rgbname)
                FileHelper.writeWithSize(tmpFile, alphaname)
                
                # if preAlpha:
                    # tmpFile.write('p')
                # else:
                    # tmpFile.write('P')
                
                if not isSaveTransFile:
                    FileHelper.remove(rgbname)
                    FileHelper.remove(alphaname)
                    
            except Exception:
                Log.printError()
                isSuccess = False
                pass
            finally: 
                pass
                
              
        if isSuccess:  
            if isUseGzip:
                gzip_cmd = gzipBin + tmpfilename + " -n -f -9"
                os.system(gzip_cmd)
                FileHelper.remove(tmpfilename.replace(".tmp", ".png"))
                FileHelper.rename(tmpfilename + ".gz", tmpfilename.replace(".tmp", ".png"))
                return 3
            else: 
                FileHelper.remove(tmpfilename.replace(".tmp", ".png"))
                FileHelper.rename(tmpfilename, tmpfilename.replace(".tmp", ".png"))
                return 5
        else:
            FileHelper.remove(tmpfilename)
            return 2
            
    else:
        tmpfilename = filepath.replace(".jpg", ".pkm") 
        
        if not FileHelper.exists(tmpfilename):
            Log.printDetailln ("error !!!", filepath, "cannot convert.")
            return 2
        
        if isUseGzip:
            gzip_cmd = gzipBin + tmpfilename + " -n -f -9"
            os.system(gzip_cmd)
            FileHelper.remove(tmpfilename.replace(".pkm", ".jpg"))
            FileHelper.rename(tmpfilename + ".gz", tmpfilename.replace(".pkm", ".jpg"))
            return 3
        else:
            FileHelper.remove(tmpfilename.replace(".pkm", ".jpg"))
            FileHelper.rename(tmpfilename, tmpfilename.replace(".pkm", ".jpg"))
            return 4

def convert(filename, isAlphaJPG = False):
    ret = work_file_ETC(filename, isAlphaJPG)
    return ret