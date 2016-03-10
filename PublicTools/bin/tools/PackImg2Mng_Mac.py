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

texturePackerBin = os.path.join(projectdir, "TexturePacker.exe")
tpPath = os.path.join(projectdir, "etcpack.exe ")
etcBin = os.path.join(projectdir, "etcpack.exe ")
gzipBin = os.path.join(projectdir, "gzip.exe ")  
mpBin = os.path.join(projectdir, "MPConvert.exe ")  
convertBin = os.path.join(projectdir, "convert.exe ") 
pvrTexToolBin = os.path.join(projectdir, "PVRTexToolCLI.exe ") 

etcTPBin = """%s --quiet --texture-format pkm --opt ETC1 --dither-type FloydSteinberg --sheet "%%s" --disable-rotation --max-size 4096 --size-constraints AnySize %%s""" % (texturePackerBin)

iosPngCmd = """%s %%s %%s -c etc1 -s slow -as """ % (tpPath)
iosJpgCmd = """%s %%s %%s -c etc1 -s slow  """ % (tpPath)

iosPngCmd = """%s %%s %%s -c etc1  -as """ % (tpPath)
iosJpgCmd = """%s %%s %%s -c etc1  """ % (tpPath)

isUseGzip = True
isSaveTransFile = False
isConvertMP = False

isUseEtcInJpg = False

RGBMode = "ETC"

isShowFilesCount = False
GzipCnt = 0
MngCnt = 0
PkmCnt = 0
PassCnt = 0

filters = ["crater"]

def updateConvertCMD(fastTag):
    global RGBMode, iosPngCmd, iosJpgCmd, tpPath, gzipBin, mpBin, convertBin, isUseGzip
  
    tpPath = os.path.join(tpDir, "etcpack.exe ")
    gzipBin = os.path.join(tpDir, "gzip.exe ")
    mpBin = os.path.join(tpDir, "MPConvert.exe ") 
    convertBin = os.path.join(tpDir, "convert.exe ") 
        
    if RGBMode == "ETC":
        iosPngCmd = """%s %%s %%s -c etc1 -s %s -as """ % (tpPath, fastTag)
        iosJpgCmd = """%s %%s %%s -c etc1 -s %s """ % (tpPath, fastTag)
        isUseGzip = True
        
    elif RGBMode == "JPG":  
        # convert Bird.png -quality 95  -background black -alpha remove Bird.jpg
        # convert Bird.png -sample 75%%%%x75%%%% -quality 95  -alpha extract Bird_alpha_mask.png
        iosPngCmd = """%s %%s -background black -alpha remove %%s """ % (convertBin)
        iosJpgCmd = """%s %%s -alpha extract %%s """ % (convertBin)
        
        if isUseEtcInJpg:
            iosPngCmd = """%s %%s -quality 85 -background black -alpha remove %%s """ % (convertBin)
            iosJpgCmd = """%s %%s -quality 85 -alpha extract %%s """ % (convertBin)
        
        isUseGzip = False
        
    elif RGBMode == "PVR":
        isUseGzip = True
        pass
 
def convertJPG2ETC2(filename):
    filepath = os.path.realpath(filename)
    filedir = os.path.dirname(filepath)
    
    imgCmd = """%s %s %s -c etc1 """ % (etcBin, filepath, filedir) 
    try:    
        os.system(imgCmd)   
    except Exception:
        print "convertJPG2ETC, error !!!", filename, "cannot convert."
        return False
    finally:
        pass
    tmpfilename = filepath.replace(".jpg", ".pkm") 
        
    if not os.path.exists(tmpfilename):
        print "error2 !!!", filepath, "cannot convert."
        return False
    
    if os.path.exists(tmpfilename.replace(".pkm", ".jpg")):
        os.remove(tmpfilename.replace(".pkm", ".jpg"))
    os.rename(tmpfilename, tmpfilename.replace(".pkm", ".jpg"))    
    return True
 
def convertJPG2ETC(filename):
    filepath = os.path.realpath(filename)
    filedir = os.path.dirname(filepath)
    
    tempFile = filepath.replace(".jpg", ".tmp.png")
    tempCMD = """ %s %s %s """ % (convertBin, filepath, tempFile)
    os.system(tempCMD)  
    
    imgCmd = etcTPBin % (filepath.replace(".jpg", ".pkm"), tempFile) 
    try:    
        print imgCmd
        os.system(imgCmd) 
        if os.path.exists(tempFile):  
            os.remove(tempFile)
    except Exception:
        print "convertJPG2ETC, error !!!", filename, "cannot convert."
        return False
    finally:
        pass
    tmpfilename = filepath.replace(".jpg", ".pkm") 
        
    if not os.path.exists(tmpfilename):
        print "error2 !!!", filepath, "cannot convert."
        return False
    
    if os.path.exists(tmpfilename.replace(".pkm", ".jpg")):
        os.remove(tmpfilename.replace(".pkm", ".jpg"))
    os.rename(tmpfilename, tmpfilename.replace(".pkm", ".jpg"))    
    return True

#压缩参数路径下的所有图片成mng
def work_file_Jpg(filename):
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
        PassCnt = PassCnt + 1
        return
    else:
        PassCnt = PassCnt + 1
        return
    
    jpgCMD = iosPngCmd % (filepath, filepath.replace(".png", ".jpg")) 
    alphaCmd = iosJpgCmd % (filepath, filepath.replace(".png", ".alpha.jpg"))
    # print jpgCMD, alphaCmd     
    try:                   
        os.system(jpgCMD) 
        os.system(alphaCmd)   
    except Exception:
        print "error33 !!!", filename, "cannot convert."
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
                
                rgbname = filepath.replace(".png", ".jpg") 
                alphaname = filepath.replace(".png", ".alpha.jpg") 
                
                if isUseEtcInJpg and ((not convertJPG2ETC(rgbname)) or (not convertJPG2ETC(alphaname))):
                    print "convert Error : jpg to etc"
                    return
                                 
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
                    
            except Exception, e:
                print "error !!!", filename, "cannot convert.", e
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
                
def work_file_ETC(filename):
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
        
    if imgCmd == "":
        PassCnt = PassCnt + 1
        return
       
    imgCmd = imgCmd % (filepath, filedir) 
    
    rgbCMD = """ %s -f ETC1 -p -q etcslow -i %s -o %s """ % (pvrTexToolBin, filepath, filepath.replace(".png", ".pvr"))
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
            os.system(alphaJPGCMD) 

            print "comp"
            os.rename(filepath.replace(".png", ".pvr"), filepath.replace(".png", ".pkm"))   
            os.rename(filepath.replace(".png", ".alpha.pvr"), filepath.replace(".png", "_alpha.pkm")) 

            if os.path.exists(filepath.replace(".png", ".alpha.jpg")):
                os.remove(filepath.replace(".png", ".alpha.jpg"))            
        else:        
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

def work_file(filename):    
    if RGBMode == "ETC":
        work_file_ETC(filename)
    elif RGBMode == "JPG":
        work_file_Jpg(filename)
    elif RGBMode == "PVR":
        work_file_ETC(filename)
    
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
            if isConvertMP:
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
    
    global tpDir, tpPath, gzipBin, iosPngCmd, iosJpgCmd, isUseGzip, filters, RGBMode, isConvertMP
    
    fastTag = "fast"
    
    isCmdChange = False
    
    targetFiles = []
    
    opts, args = getopt.getopt(sys.argv[1:], "d:t:g:f:s:m:p")
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
        elif op == "-p":
            isConvertMP = True
                
    updateConvertCMD(fastTag)
        
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
            curdir = r"E:\Workspace\Mobilephone_DDT\trunk\Client\Develop\Resource_JPG"
            work_async(curdir)
    print( "Complete: Gzip:%d, Mng:%d, Pkm:%d, Pass:%d ==  %d" % ( GzipCnt, MngCnt, PkmCnt, PassCnt, GzipCnt + MngCnt + PkmCnt + PassCnt ) )    
    
if __name__ == '__main__': 
    try:
        work()
    except Exception, e:
        print Exception, e