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
import platform
from pprint import pprint
from struct import *

from util import Log
from util import toolsPath
from util import FileHelper

tpDir = toolsPath

gzipBin = FileHelper.gzipBin
convertBin = FileHelper.convertBin
pvrTexToolBin = FileHelper.pvrTexToolBin


#压缩参数路径下的所有图片成mng
def work_png(filename): 
    filepath = FileHelper.realpath(filename)
    filedir = FileHelper.dirname(filepath)
    os.chdir(tpDir)
    
    isSaveTransFile = False
    isPng = True
    useGZIP = False
    
    if isPng:
        jpgCMD = """%s %s -background black %s """ % (convertBin, filepath, filepath.replace(".png", ".rgb.jpg"))
        alphaCMD = """%s %s -alpha extract %s """ % (convertBin, filepath, filepath.replace(".png", ".alpha.jpg"))        
    
        try:                   
            os.system(jpgCMD) 
            os.system(alphaCMD)   
        except Exception:
            Log.printDetailln ("error33 !!!", filename, "cannot convert.")
            return 2
        finally:
            pass
    
        tmpfilename = filepath.replace(".png", ".tmp")
        FileHelper.remove(tmpfilename)
        
        isSuccess = True
        with open(tmpfilename, 'wb+') as tmpFile:
            try: 
                tmpFile.write(b'MNG')
                
                rgbname = filepath.replace(".png", ".rgb.jpg") 
                FileHelper.writeWithSize(tmpFile, rgbname)
                
                alphaname = filepath.replace(".png", ".alpha.jpg") 
                FileHelper.writeWithSize(tmpFile, alphaname)
                
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
            if useGZIP:
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
            return 2


def work2JPG(filename, isPng = False):
    filepath = FileHelper.realpath(filename)
    filedir = FileHelper.dirname(filepath)
    name = FileHelper.basename(filepath)
  
    os.chdir(tpDir)
 
    jpgCMD = """%s -quality 90 %s %s """ % (convertBin, filepath, filepath)                 
    os.system(jpgCMD)  
    #return           
            
    tmpfilename = FileHelper.join(filedir, hashlib.md5(name.encode('utf-8')).hexdigest())
        
    isSuccess = True
    with open(tmpfilename, 'wb+') as tmpFile:
        try: 
            tmpFile.write(b'MNG')
            
            rgbname = filepath 
            FileHelper.writeWithSize(tmpFile, filepath)      

        except Exception:
            Log.printDetailln ("error00 !!!", filename, "cannot convert.")
            isSuccess = False
        finally: 
            pass
    if isSuccess:        
        FileHelper.remove(filepath)
        FileHelper.rename(tmpfilename, filepath)      
        return 5  
    else:
        return 2                
 

def convert(filename, isPng = False):
    if isPng:
        ret = work_png(filename)
    else:
        ret = work2JPG(filename)
    return ret