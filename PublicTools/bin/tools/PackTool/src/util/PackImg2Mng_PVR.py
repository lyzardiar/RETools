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

from util import PackImgJPG, ImageInfo

def iter_find_files(path, fnexp):
    for root, dirs, files, in os.walk(path):
        for filename in fnmatch.filter(files, fnexp):
            yield os.path.join(root, filename)

            
projectdir = os.path.dirname(os.path.realpath(__file__)) + '/../../../'
tpDir = projectdir

if platform.system() == "Windows":
    gzipBin = "gzip.exe " #os.path.join(projectdir, "gzip.exe ")  
    convertBin = "convert.exe " #os.path.join(projectdir, "convert.exe ") 
    pvrTexToolBin = "PVRTexToolCLI.exe "
else:
    convertBin = os.path.join(projectdir, "/bin/ios/x86/convert ") 
    gzipBin = "gzip "
    pvrTexToolBin = os.path.join(projectdir, "/bin/ios/x86/PVRTexToolCLI ")

isUseGzip = True
isSaveTransFile = False

RGBMode = "PVR"

def work_file_PVR(filename, isDTC4Module = False, isTC4 = False):
    filepath = os.path.realpath(filename)
    filedir = os.path.dirname(filepath)

    sys.stdout.flush() 
       
    os.chdir(tpDir)
    
    isTC4 = True
    isAlphaJPG = False
    if isDTC4Module:
        isTC4 = False
    
    preCMD = " -p "
    preCMD = ""
    
    info = ImageInfo.size(filepath)
    
    # 只支持png纹理
    if info[0] != 'PNG':
        return 2
    
    width = info[1]
    height = info[2]
    
    # 只支持正方形2的幂纹理
    if width & (width-1) != 0 or width != height:
        return 2
        
    
    rgbCMD = """ %s -f PVRTC1_4_RGB %s -q pvrtcbest -i %s -o %s """ % (pvrTexToolBin, preCMD, filepath, filepath.replace(".png", ".pvr"))
    alphaCMD = """%s %s -alpha extract %s """ % (convertBin, filepath, filepath.replace(".png", ".alpha.jpg"))
    alphaJPGCMD = """ %s -f PVRTC1_4_RGB -q pvrtcbest -i %s -o %s """ % (pvrTexToolBin, filepath.replace(".png", ".alpha.jpg"), filepath.replace(".png", ".alpha.pvr"))
    
    if isTC4:
        rgbCMD = """ %s -f PVRTC1_4 %s -q pvrtcbest -i %s -o %s """ % (pvrTexToolBin, preCMD, filepath, filepath.replace(".png", ".pvr"))
    
    try:   
        if os.path.exists(filepath.replace(".png", ".pkm")):
            os.remove(filepath.replace(".png", ".pkm"))
        if os.path.exists(filepath.replace(".png", "_alpha.pkm")):
            os.remove(filepath.replace(".png", "_alpha.pkm"))
    
        os.system(rgbCMD) 
        
        if not isTC4:
            os.system(alphaCMD) 
        
        if not isAlphaJPG and not isTC4:
            os.system(alphaJPGCMD) 
        
        if not os.path.exists(filepath.replace(".png", ".pvr")):
            return 2
            
        os.rename(filepath.replace(".png", ".pvr"), filepath.replace(".png", ".pkm"))   
        
        if not isTC4:
            if not isAlphaJPG:
                os.rename(filepath.replace(".png", ".alpha.jpg"), filepath.replace(".png", "_alpha.pkm")) 
            else:
                os.rename(filepath.replace(".png", ".alpha.pvr"), filepath.replace(".png", "_alpha.pkm")) 

            if os.path.exists(filepath.replace(".png", ".alpha.jpg")):
                os.remove(filepath.replace(".png", ".alpha.jpg"))
            if os.path.exists(filepath.replace(".png", ".alpha.pvr")):
                os.remove(filepath.replace(".png", ".alpha.pvr"))  
        
    except Exception:
        t, v, tb = sys.exc_info()
        print(t, v)
        return 2
    finally:
        pass
    
    tmpfilename = filepath.replace(".png", ".tmp")
    if os.path.exists(tmpfilename):
        os.remove(tmpfilename)
    
    isSuccess = True
    with open(tmpfilename, 'wb+') as tmpFile:
        try: 
            tmpFile.write(b'MNG')
            
            rgbname = filepath.replace(".png", ".pkm") 
            
            statinfo = os.stat(rgbname)
            fileSize = statinfo.st_size
            
            tmpFile.write(pack("i", fileSize))
            rgbfile = open(rgbname, "rb")
            tmpFile.write(rgbfile.read())
            rgbfile.close()
            
            alphaname = filepath.replace(".png", "_alpha.pkm") 
            if not isTC4:
                statinfo = os.stat(alphaname)
                fileSize = statinfo.st_size
                
                tmpFile.write(pack("i", fileSize))
                alphafile = open(alphaname, "rb")
                tmpFile.write(alphafile.read())
                alphafile.close()
            
            # if preAlpha:
                # tmpFile.write('p')
            # else:
                # tmpFile.write('P')
            
            if not isSaveTransFile:
                if os.path.exists(rgbname):
                    os.remove(rgbname)
                if os.path.exists(alphaname):
                    os.remove(alphaname)
                
        except Exception:
            t, v, tb = sys.exc_info()
            print(t, v)
            isSuccess = False
            pass
        finally: 
            pass
            
            
    if isSuccess:  
        if isUseGzip:
            gzip_cmd = gzipBin + tmpfilename + " -n -f -9"
            os.system(gzip_cmd)
            if os.path.exists(tmpfilename.replace(".tmp", ".png")):
                os.remove(tmpfilename.replace(".tmp", ".png"))
            os.rename(tmpfilename + ".gz", tmpfilename.replace(".tmp", ".png"))
            return 3
        else: 
            if os.path.exists(tmpfilename.replace(".tmp", ".png")):
                os.remove(tmpfilename.replace(".tmp", ".png"))
            os.rename(tmpfilename, tmpfilename.replace(".tmp", ".png"))
            return 5

def convert(filename, isDTC4Module = False, isTC4 = False):
    ret = work_file_PVR(filename, isDTC4Module, isTC4)
    return ret