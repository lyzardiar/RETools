#coding=utf-8  

import os
import os.path
import shutil
import sys
import getopt
import string  
import fnmatch
import md5
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

            
projectdir = os.path.dirname(os.path.realpath(__file__))
tpDir = projectdir
tpPath = os.path.join(projectdir, "etcpack.exe ")
gzipBin = os.path.join(projectdir, "gzip.exe ")  
mpBin = os.path.join(projectdir, "MPConvert.exe ")  

iosPngCmd = """%s %%s %%s -c etc1 -s slow -as """ % (tpPath)
iosJpgCmd = """%s %%s %%s -c etc1 -s slow  """ % (tpPath)

iosPngCmd = """%s %%s %%s -c etc1  -as """ % (tpPath)
iosJpgCmd = """%s %%s %%s -c etc1  """ % (tpPath)

isUseGzip = True
isSaveTransFile = False

RGBMode = "ETC"

isShowFilesCount = False
GzipCnt = 0
MngCnt = 0
PkmCnt = 0
PassCnt = 0

filters = ["crater"]

#压缩参数路径下的所有图片成mng
def work_file(filename):
    global GzipCnt, MngCnt, PkmCnt, PassCnt, filters
    filepath = os.path.realpath(filename)
    filedir = os.path.dirname(filepath)

    sys.stdout.flush() 
    
    for filtername in filters:
        if filepath.find(filtername) != -1:
            PassCnt = PassCnt + 1
            return
    
    with open(filepath, 'rb') as tmpFile:
        tmpContent = tmpFile.read(3)
        if tmpContent[0] == '\x1f' and tmpContent[1] == '\x8b':
            print "Gzip File, pass."
            GzipCnt = GzipCnt + 1
            return
        if tmpContent == "MNG":
            print "MNG File, pass."
            MngCnt = MngCnt + 1
            return
        if tmpContent == "PKM":
            print "PKM File, pass."
            PkmCnt = PkmCnt + 1
            return
            
    os.chdir(tpDir)
    
    isPng = True
    if filename.find(".png") != -1:
        isPng = True
    elif filename.find(".jpg") != -1:
        isPng = False
    else:
        return

    if isPng: 
        imgCmd = iosPngCmd           
    else:
        imgCmd = iosJpgCmd  
        
    imgCmd = imgCmd % (filepath, filedir) 
    try:    
        os.system(imgCmd)   
    except Exception:
        print "error !!!", filename, "cannot convert."
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
                tmpFile.write('MNG')
                
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
                
                if not isSaveTransFile:
                    if os.path.exists(rgbname):
                        os.remove(rgbname)
                    if os.path.exists(alphaname):
                        os.remove(alphaname)
                    
            except Exception:
                print "error !!!", filename, "cannot convert."
                isSuccess = False
                pass
            finally: 
                pass
                
              
        if isSuccess:  
            if isUseGzip:
                GzipCnt = GzipCnt + 1 
                gzip_cmd = gzipBin + tmpfilename + " -N -f -9"
                os.system(gzip_cmd)
                if os.path.exists(tmpfilename.replace(".tmp", ".png")):
                    os.remove(tmpfilename.replace(".tmp", ".png"))
                os.rename(tmpfilename + ".gz", tmpfilename.replace(".tmp", ".png"))
            else: 
                MngCnt = MngCnt + 1
                if os.path.exists(tmpfilename.replace(".tmp", ".png")):
                    os.remove(tmpfilename.replace(".tmp", ".png"))
                os.rename(tmpfilename, tmpfilename.replace(".tmp", ".png"))
        else:
            PassCnt = PassCnt + 1
            if os.path.exists(tmpfilename):
                os.remove(tmpfilename)
            
    else:
        tmpfilename = filepath.replace(".jpg", ".pkm") 
        
        if not os.path.exists(tmpfilename):
            print "error !!!", filepath, "cannot convert."
            PassCnt = PassCnt + 1
            return
        
        if isUseGzip:
            GzipCnt = GzipCnt + 1 
            
            gzip_cmd = gzipBin + tmpfilename + " -N -f -9"
            os.system(gzip_cmd)
            if os.path.exists(tmpfilename.replace(".pkm", ".jpg")):
                os.remove(tmpfilename.replace(".pkm", ".jpg"))
            os.rename(tmpfilename + ".gz", tmpfilename.replace(".pkm", ".jpg"))
        else:
            PkmCnt = PkmCnt + 1
            
            if os.path.exists(tmpfilename.replace(".pkm", ".jpg")):
                os.remove(tmpfilename.replace(".pkm", ".jpg"))
            os.rename(tmpfilename, tmpfilename.replace(".pkm", ".jpg"))
    
           
    pass

def work_async(tardir):
    python_dir = tardir

    os.chdir(python_dir)

    files = []

    for filename in iter_find_files(python_dir, "*.*"):
        if filename.find(" ") != -1:
            msg = "Blank in File path:" + filename
            raise IOError, msg
        relativeFilename = os.path.relpath(filename, python_dir).replace("\\", '/')
        if filename.find(".png") != -1:
            files.append((relativeFilename, 0, filename))
        elif filename.find(".jpg") != -1:
            files.append((relativeFilename, 1, filename))
        elif filename.find(".mp3") != -1:
            pass
        elif filename.find(".mp") != -1:
            print("Convert mp:", filename)
            os.system("%s %s" % (mpBin, filename))
    
    trdcount = 10
    
    length = len(files)
    count = 0
    can_quiet = False
    
    for info in files:
        count = count + 1
        work_file(info[2])
        print("pack[%d/%d]: %s" % (count, length, info[0]))

    pass
    
def work():
    isShowFilesCount = True
    
    global tpDir, tpPath, gzipBin, iosPngCmd, iosJpgCmd, isUseGzip, filters, RGBMode
    
    fastTag = "fast"
    
    isCmdChange = False
    
    targetFiles = []
    
    opts, args = getopt.getopt(sys.argv[1:], "d:t:g:f:s:m:")
    for op, value in opts:
        if op == "-d":
            targetFiles.append(value)
        elif op == "-t":
            isCmdChange = True
            tpDir = value
        elif op == "-g":
            if value == 'true':
                isUseGzip = True
            else:
                isUseGzip = False
        elif op == "-s":
            isCmdChange = True
            if value == 'fast':
                fastTag = "fast"
            else:
                fastTag = "slow"
        elif op == "-f":
            filters.append(value)
        elif op == "-m":
            isCmdChange = True
            if value == "ETC":
                RGBMode = "ETC"
            elif value == "JPG":
                RGBMode = "JPG"
            elif value == "PVR":
                RGBMode = "PVR"
                
    if isCmdChange:    
        tpPath = os.path.join(tpDir, "etcpack.exe ")
        gzipBin = os.path.join(tpDir, "gzip.exe ")

        iosPngCmd = """%s %%s %%s -c etc1 -s %s -as """ % (tpPath, fastTag)
        iosJpgCmd = """%s %%s %%s -c etc1 -s %s """ % (tpPath, fastTag)
        
    print targetFiles
    if len(targetFiles) > 0:
        for i in range(0, len(targetFiles)):
            filepath = targetFiles[i]
            if os.path.isdir(filepath):
                work_async(filepath)
            else:
                work_file(filepath)
    else:    
        if len(sys.argv) > 1:
            inputFile = sys.argv[1]
            for i in range(1, len(sys.argv)):
                filepath = sys.argv[i]
                if os.path.isdir(filepath):
                    work_async(filepath)
                else:
                    work_file(filepath)
        else:
            curdir = r"E:\Workspace\Mobilephone_DDT\trunk\Client\Engine\proj.android\assets\res"
            work_async(curdir)
    print( "Complete: Gzip:%d, Mng:%d, Pkm:%d, Pass:%d ==  %d" % ( GzipCnt, MngCnt, PkmCnt, PassCnt, GzipCnt + MngCnt + PkmCnt + PassCnt ) )    
    
if __name__ == '__main__': 
    try:
        work()
    except Exception, e:
        print Exception, e