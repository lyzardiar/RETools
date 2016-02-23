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

tpDir = "E:/Workspace/Mobilephone_DDT/trunk/Client/Develop/Tools/android/etc/"
tpPath = tpDir + "etcpack.exe "
gzipBin = tpDir + "gzip.exe "

iosPngCmd = """%s %%s %%s -c etc1 -as """ % (tpPath)
iosJpgCmd = """%s %%s %%s -c etc1  """ % (tpPath)

isUseGzip = True

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
    
    trdcount = 10
    
    length = len(files)
    count = 0
    can_quiet = False
    
    for info in files:
        count = count + 1
        work_file(info[2])
        print("pack[%d/%d]: %s" % (count, length, info[2]))
    
    # while not can_quiet:
        # t = None
        # for i in range(0, trdcount): 
            # if count >= length:
                # can_quiet = True
                # break
            # info = files[count]
            # isPng = (info[1] == 0)
            # imgfilename = info[2]

            # t = threading.Thread(target=work_file,args=(imgfilename,))
            # # t.setDaemon(True)
            # t.start()
            # count = count + 1
        # t.join()
        # print("pack[%d/%d]: %s" % (count, length, imgfilename))
    pass
    

if __name__ == '__main__': 
    if len(sys.argv) > 1:
        inputFile = sys.argv[1]
        for i in range(1, len(sys.argv)):
            work_file(sys.argv[i])
        # os.system("pause")
    else:
        isShowFilesCount = True
        curdir = r"E:\Workspace\Mobilephone_DDT\trunk\Client\Engine\proj.android\assets\res"
        work_async(curdir)
        print( "Complete: Gzip:%d, Mng:%d, Pkm:%d, Pass:%d ==  %d" % ( GzipCnt, MngCnt, PkmCnt, PassCnt, GzipCnt + MngCnt + PkmCnt + PassCnt ) )