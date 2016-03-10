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

def work_file(filepath):
    filepath = os.path.realpath(filepath)

    with open(filepath, 'rb') as tmpFile:
        tmpContent = tmpFile.read(3)
        if tmpContent[0] == '\x1f' and tmpContent[1] == '\x8b':
            print "Gzip File, pass."
            return
    
    gzip_cmd = "gzip " + filepath + " -n -f -9"
    os.system(gzip_cmd)
    
    if os.path.exists(filepath):
        os.remove(filepath)
    
    if os.path.exists(filepath + ".gz"):
        os.rename(filepath + ".gz", filepath) 
    pass
    
def work_async(tardir):
    for filename in iter_find_files(tardir, "*.*"):
        if filename.find(".map") != -1:
            work_file(filename)
            pass             
            
def work():   
    if len(sys.argv) > 1:
        inputFile = sys.argv[1]
        for i in range(1, len(sys.argv)):
            filepath = os.path.realpath(sys.argv[i])
            if os.path.isdir(filepath):
                work_async(filepath)
            else:
                work_file(filepath)
    else:
        curdir = r"E:\Workspace\Mobilephone_DDT\trunk\Client\Develop\Resource_JPG"
        work_async(curdir)    
    os.system("pause")
    
if __name__ == '__main__': 
    try:
        work()
    except Exception, e:
        print Exception, e