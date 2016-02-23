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
from pprint import pprint 

def iter_find_files(path, fnexp):
    for root, dirs, files, in os.walk(path):
        for filename in fnmatch.filter(files, fnexp):
            yield os.path.join(root, filename)


key1 = '88e5fd90'
key2 = 'b01f170e'
key3 = 'cffa905c'
key4 = '71ffb7f3'

usekey = False
usePlist = False

keyCmd = ''
plistCmd = ''

if usekey: 
    keyCmd = """--content-protection %s%s%s%s""" % ( key1, key2, key3, key4)

if usePlist: 
    plistCmd = '--data "%s.plist"'

tpPath = "D:/CodeAndWeb2/TexturePacker/bin/TexturePacker.exe"

tpPath = 'D:/CodeAndWeb3/TexturePacker/bin/TexturePacker.exe '

tpPath = r"E:\Workspace\Mobilephone_DDT\trunk\Client\Develop\Tools\ios\tp\TexturePacker.exe "

androidPngCmd = """%s "%%s" --quiet --format cocos2d --texture-format pvr3ccz --opt RGBA8888 --premultiply-alpha %s %%s --sheet "%%s" --disable-rotation --max-size 4096 """ % (tpPath, keyCmd)
androidJpgCmd = """%s "%%s" --quiet --format cocos2d --texture-format pvr3ccz --jpg-quality 95 --opt RGB565 %s %%s --sheet "%%s" --disable-rotation --max-size 4096 """ % (tpPath, keyCmd)

iosPngCmd = """%s "%%s" --quiet --format cocos2d --texture-format pvr3ccz --pvr-quality high --opt PVRTC4           --dither-type FloydSteinbergAlpha --premultiply-alpha   %s %%s --sheet "%%s" --disable-rotation --max-size 4096 --size-constraints AnySize """ % (tpPath, keyCmd)
iosJpgCmd = """%s "%%s" --quiet --format cocos2d --texture-format pvr3ccz --pvr-quality high --opt PVRTC4_NOALPHA   --dither-type FloydSteinberg                            %s %%s --sheet "%%s" --disable-rotation --max-size 4096 --size-constraints AnySize """ % (tpPath, keyCmd)

iosPngCmd = """%s "%%s" --quiet --format cocos2d --texture-format pvr2ccz --opt PVRTC4   --dither-fs-alpha   %s %%s --sheet "%%s" --disable-rotation --max-size 4096 """ % (tpPath, keyCmd)
# iosPngCmd = """%s "%%s" --quiet --format cocos2d --texture-format pvr2ccz --opt RGBA8888   --dither-fs-alpha   %s %%s --sheet "%%s" --disable-rotation --max-size 4096 --size-constraints AnySize """ % (tpPath, keyCmd)


#压缩参数路径下的所有图片成pvr.ccz
def work_file(filename):
    isPng = True
    if filename.find(".png") != -1:
        isPng = True
    elif filename.find(".jpg") != -1:
        isPng = False

    if isPng: 
        imgCmd = iosPngCmd
        ext = ".png"                
    else:
        imgCmd = iosJpgCmd
        ext = ".jpg"    

    imgfilename = filename  

    pvrfilename = imgfilename.replace(ext, ".pvr.ccz") 

    plstcmd = ''
    if usePlist: 
        plistfilename = imgfilename.replace(ext, ".plist")
        plstcmd = plistCmd % (plistfilename)
    
    cmdIosStr = imgCmd % (imgfilename, plstcmd, pvrfilename)

    print(cmdIosStr)
    
    os.system(cmdIosStr)
    #os.remove(imgfilename)
    os.rename(pvrfilename, imgfilename)

    #os.remove("out.plist")    

    pass


def work_dir(tardir):
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
    
    length = len(files)
    count = 0
    for info in files:
        count = count + 1
        isPng = (info[1] == 0)
        imgfilename = info[0]

        if isPng: 
            imgCmd = iosPngCmd
            ext = ".png"                
        else:
            imgCmd = iosJpgCmd
            ext = ".jpg"      

        pvrfilename = imgfilename.replace(ext, ".pvr.ccz") 

        plstcmd = ''
        if usePlist: 
            plistfilename = imgfilename.replace(ext, ".plist")
            plstcmd = plistCmd % (plistfilename)
        
        cmdIosStr = imgCmd % (imgfilename, plstcmd, pvrfilename)

        os.system(cmdIosStr)
        os.remove(imgfilename)
        os.rename(pvrfilename, imgfilename)
        print("pack[%d/%d]: %s" % (count, length, imgfilename))

    os.remove("out.plist")

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
    while not can_quiet:
        t = None
        for i in range(0, trdcount): 
            if count >= length:
                can_quiet = True
                break
            info = files[count]
            isPng = (info[1] == 0)
            imgfilename = info[0]

            t = threading.Thread(target=work_file,args=(imgfilename,))
            # t.setDaemon(True)
            t.start()
            count = count + 1
        t.join()
        print("pack[%d/%d]: %s" % (count, length, imgfilename))

    os.remove("out.plist")
    pass
    

if __name__ == '__main__': 
    if len(sys.argv) > 1:
        inputFile = sys.argv[1]
        for i in range(1, len(sys.argv)):
            work_file(sys.argv[i])
        # os.system("pause")
    else:
        curdir = r"F:\Workspace\Mobilephone_DDT\trunk\Client\Develop\Resource\res\uiNew\roleAndDevelop"
        work_async(curdir)