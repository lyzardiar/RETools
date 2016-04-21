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

#压缩参数路径下的所有图片成mng
def work_png(filename):
    filepath = os.path.realpath(filename)
    filedir = os.path.dirname(filepath)
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
            print ("error33 !!!", filename, "cannot convert.")
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
                
                rgbname = filepath.replace(".png", ".rgb.jpg") 
                            
                statinfo = os.stat(rgbname)
                fileSize = statinfo.st_size
                
                tmpFile.write(pack("i", fileSize))
                rgbfile = open(rgbname, "rb")
                tmpFile.write(rgbfile.read())
                rgbfile.close()
                
                alphaname = filepath.replace(".png", ".alpha.jpg") 
                statinfo = os.stat(alphaname)
                fileSize = statinfo.st_size
                
                tmpFile.write(pack("i", fileSize))
                alphafile = open(alphaname, "rb")
                tmpFile.write(alphafile.read())
                alphafile.close()
                
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
            if useGZIP:
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
            return 2


def work2JPG(filename, isPng = False):
    filepath = os.path.realpath(filename)
    filedir = os.path.dirname(filepath)
    name = os.path.basename(filepath)
  
    os.chdir(tpDir)
 
    jpgCMD = """%s -quality 85 %s %s """ % (convertBin, filepath, filepath)                 
    os.system(jpgCMD)  
    return           
            
    tmpfilename = os.path.join(filedir, hashlib.md5(name.encode('utf-8')).hexdigest())
        
    isSuccess = True
    with open(tmpfilename, 'wb+') as tmpFile:
        try: 
            tmpFile.write(b'MNG')
            
            rgbname = filepath 
            
            statinfo = os.stat(rgbname)
            fileSize = statinfo.st_size
            
            tmpFile.write(pack("i", fileSize))
            rgbfile = open(rgbname, "rb")
            tmpFile.write(rgbfile.read())
            rgbfile.close()
                
        except Exception:
            print ("error00 !!!", filename, "cannot convert.")
            isSuccess = False
        finally: 
            pass
    if isSuccess:        
        if os.path.exists(filepath):
            os.remove(filepath)
        os.rename(tmpfilename, filepath)      
        return 5  
    else:
        return 2                
 

def convert(filename, isPng = False):
    if isPng:
        ret = work_png(filename)
    else:
        ret = work2JPG(filename)
    return ret