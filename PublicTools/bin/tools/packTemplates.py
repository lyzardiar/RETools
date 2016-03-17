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

projectdir = os.path.dirname(os.path.realpath(__file__))

luaPackBin = os.path.join(projectdir, "packTemplates.lua")

def iter_find_files(path, fnexp):
    for root, dirs, files, in os.walk(path):
        for filename in fnmatch.filter(files, fnexp):
            yield os.path.join(root, filename)

def work_file(filepath):
    if filepath.find(".lua") == -1:
        print("Pass none lua file.")
        return
    
    filepath = os.path.realpath(filepath)
    os.system("lua %s %s" % (luaPackBin, filepath))
    pass
    
def work_async(tardir):
    for filename in iter_find_files(tardir, "*.*"):
        if filename.find(".lua") != -1:
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
        curdir = r"C:\WorkSpace\Public\TX\Android\main\config\maps\Scene"
        curdir = r"E:\Workspace\Mobilephone_DDT\trunk\Client\Develop\Resource\config\template"
        work_async(curdir)    
    os.system("pause")
    
if __name__ == '__main__': 
    try:
        work()
    except Exception, e:
        print Exception, e