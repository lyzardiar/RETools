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

projectdir = os.path.dirname(os.path.realpath(__file__)) + '/../../../'
tpDir = projectdir

if platform.system() == "Windows":
    gzipBin = "gzip.exe "
else:
    gzipBin = "gzip "

def work_file_GZIP(filename, nameType = 1):
    filepath = os.path.realpath(filename)
    filedir = os.path.dirname(filepath)

    sys.stdout.flush() 
    
    with open(filepath, 'rb') as tmpFile:
        tmpContent = tmpFile.read(3)
        if tmpContent[0:2] == b'\x1f\x8b':
            print ("Gzip File, pass.")
            return 0
 
    os.chdir(tpDir)
    
    if not os.path.exists(filepath):
        print ("error !!!", filepath, "cannot convert.")
        return 2
    
    gzip_cmd = gzipBin + filepath + " -n -f -9"
    os.system(gzip_cmd)
    if os.path.exists(filepath):
        os.remove(filepath)
    os.rename(filepath + ".gz", filepath)
    return 0
 

def convert(filename, nameType = 1):
    ret = work_file_GZIP(filename, nameType)
    return ret