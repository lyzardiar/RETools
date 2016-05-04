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

def iter_find_files(path, fnexp):
    for root, dirs, files, in os.walk(path):
        for filename in fnmatch.filter(files, fnexp):
            yield os.path.join(root, filename)

            
projectdir = os.path.dirname(os.path.realpath(__file__)) + '/../../../'
tpDir = projectdir

tpPath = "etcpack.exe " #os.path.join(projectdir, "etcpack.exe ")
etcBin = "etcpack.exe " #os.path.join(projectdir, "etcpack.exe ")
gzipBin = "gzip.exe " #os.path.join(projectdir, "gzip.exe ")  
convertBin = "convert.exe " #os.path.join(projectdir, "convert.exe ") 
pvrTexToolBin = "PVRTexToolCLI.exe "

iosPngCmd = """%s %%s %%s -c etc1 -s slow -as """ % (tpPath)
iosJpgCmd = """%s %%s %%s -c etc1 -s slow  """ % (tpPath)

isUseGzip = True
isSaveTransFile = False

RGBMode = "ETC"

def work_file_ETC(filename, isAlphaJPG = False):
    filepath = os.path.realpath(filename)
    filedir = os.path.dirname(filepath)

    sys.stdout.flush() 

    #preAlpha = needPreAplha(filedir)
    preAlpha = False
    preCMD = " -p "
    if not preAlpha:
        preCMD = ""
            
    os.chdir(tpDir)
    
    isPng = True
    if filename.find(".png") != -1:
        isPng = True
    elif filename.find(".jpg") != -1:
        isPng = False
    else:
        return 2

    if isPng: 
        imgCmd = iosPngCmd           
    else:
        imgCmd = iosJpgCmd 
        
    if imgCmd == "":
        return 2
       
    imgCmd = imgCmd % (filepath, filedir) 
    
    rgbCMD = """ %s -f ETC1 %s -q etcslow -i %s -o %s """ % (pvrTexToolBin, preCMD, filepath, filepath.replace(".png", ".pvr"))
    alphaCMD = """%s %s -alpha extract %s """ % (convertBin, filepath, filepath.replace(".png", ".alpha.jpg"))
    alphaJPGCMD = """ %s -f ETC1 -q etcslow -i %s -o %s """ % (pvrTexToolBin, filepath.replace(".png", ".alpha.jpg"), filepath.replace(".png", ".alpha.pvr"))
    
    try:   
        if isPng:
            if os.path.exists(filepath.replace(".png", ".pkm")):
                os.remove(filepath.replace(".png", ".pkm"))
            if os.path.exists(filepath.replace(".png", "_alpha.pkm")):
                os.remove(filepath.replace(".png", "_alpha.pkm"))
        
            os.system(rgbCMD) 
            os.system(alphaCMD) 
            
            if not isAlphaJPG:
                os.system(alphaJPGCMD) 

            os.rename(filepath.replace(".png", ".pvr"), filepath.replace(".png", ".pkm"))   
            
            if isAlphaJPG:
                os.rename(filepath.replace(".png", ".alpha.jpg"), filepath.replace(".png", "_alpha.pkm")) 
            else:
                os.rename(filepath.replace(".png", ".alpha.pvr"), filepath.replace(".png", "_alpha.pkm")) 

            if os.path.exists(filepath.replace(".png", ".alpha.jpg")):
                os.remove(filepath.replace(".png", ".alpha.jpg"))
            if os.path.exists(filepath.replace(".png", ".alpha.pvr")):
                os.remove(filepath.replace(".png", ".alpha.pvr"))            
        else:    
            if os.path.exists(filepath.replace(".jpg", ".pkm")):
                os.remove(filepath.replace(".jpg", ".pkm"))         
            rgbCMD = """ %s -f ETC1 -p -q etcslow -i %s -o %s """ % (pvrTexToolBin, filepath, filepath.replace(".jpg", ".pvr"))
            os.system(rgbCMD)
            os.rename(filepath.replace(".jpg", ".pvr"), filepath.replace(".jpg", ".pkm"))  
        
    except Exception:
        t, v, tb = sys.exc_info()
        print(t, v)
        pass
    finally:
        pass
  
    if isPng:   
        tmpfilename = filepath.replace(".png", ".tmp")
        if os.path.exists(tmpfilename):
            os.remove(tmpfilename)
        
        isSuccess = True
        with open(tmpfilename, 'wb+') as tmpFile:
            try: 
                tmpFile.write(b'MNG')
                
                rgbname = filepath.replace(".png", ".pkm") 
                alphaname = filepath.replace(".png", "_alpha.pkm") 
                
                statinfo = os.stat(rgbname)
                fileSize = statinfo.st_size
                
                tmpFile.write(pack("i", fileSize))
                rgbfile = open(rgbname, "rb")
                tmpFile.write(rgbfile.read())
                rgbfile.close()
                
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
        else:
            if os.path.exists(tmpfilename):
                os.remove(tmpfilename)
            return 2
            
    else:
        tmpfilename = filepath.replace(".jpg", ".pkm") 
        
        if not os.path.exists(tmpfilename):
            print ("error !!!", filepath, "cannot convert.")
            return 2
        
        if isUseGzip:
            gzip_cmd = gzipBin + tmpfilename + " -n -f -9"
            os.system(gzip_cmd)
            if os.path.exists(tmpfilename.replace(".pkm", ".jpg")):
                os.remove(tmpfilename.replace(".pkm", ".jpg"))
            os.rename(tmpfilename + ".gz", tmpfilename.replace(".pkm", ".jpg"))
            return 3
        else:
            if os.path.exists(tmpfilename.replace(".pkm", ".jpg")):
                os.remove(tmpfilename.replace(".pkm", ".jpg"))
            os.rename(tmpfilename, tmpfilename.replace(".pkm", ".jpg"))
            return 4
 

def convert(filename, isAlphaJPG = False):
    print("work_file_ETC")
    ret = work_file_ETC(filename, isAlphaJPG)
    return ret