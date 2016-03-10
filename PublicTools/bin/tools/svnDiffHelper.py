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
import re
import commands
import xml.dom.minidom
from pprint import pprint 
from struct import *
from subprocess import Popen, PIPE


def iter_find_files(path, fnexp):
    for root, dirs, files, in os.walk(path):
        for filename in fnmatch.filter(files, fnexp):
            yield os.path.join(root, filename)

            
projectdir = os.path.dirname(os.path.realpath(__file__))

def getCurRevision(path):
    p = Popen("svn info %s" % (path), shell=True, stdout=PIPE, stderr=PIPE)  
    p.wait()  
    if p.returncode != 0:  
        print "Error."  
        return '0'
    content = p.stdout.read()
    print content
    m = re.compile(r'Revision: (\d+)')
    ret = m.search(content)   
    if ret:       
        return ret.group(1)
    else:
        return '0'

def work():
    
    left = '0'
    right = '0'
    tarpath = r"E:\Workspace\Mobilephone_DDT\trunk\Client\Develop\Resource_release"
    
    publicpath = r"E:\Workspace\Mobilephone_DDT\trunk\Client\Develop\Resource_Android"
    
    opts, args = getopt.getopt(sys.argv[1:], "r:l:i:")
    for op, value in opts:
        if op == "-l":
            left = value
        elif op == "-r":
            right = value
        elif op == "-i":
            tarpath = value
    
    
    os.system("svn update %s" % (tarpath))
    
    
    if left == '0':
        with open(os.path.join(publicpath, "Revision")) as tempFile:
            left = tempFile.readline().strip()
        if left == '0':
            return
        
    if right == '0':
        right = getCurRevision(tarpath)
        if right == '0': 
            return
    
    tmpfilename = os.path.join(projectdir, "svndifftemp.xml")
    if os.path.exists(tmpfilename):
        os.remove(tmpfilename)
    
    
    
    cmd = "svn diff --summarize --xml -r%s:%s %s >> %s" % (left, right, tarpath, tmpfilename)
    print cmd
    
    os.system(cmd)
    
    if os.path.exists(tmpfilename):
        dom = xml.dom.minidom.parse(tmpfilename)
        root = dom.documentElement
        paths = root.getElementsByTagName('path')
        
        changeList = []
        deleteList = {}
        
        for path in paths:
            kind = path.getAttribute("kind")
            if kind == "file":
                item = path.getAttribute("item")
                path = path.firstChild.data
                if item == "modified":
                    changeList.append(path)
                elif item == "added":
                    changeList.append(path)
                elif item == "deleted":
                    deleteList[path] = True
               
        filterExt = [".lua", ".map", ".png", "jpg", ".json", ".xml", ".txt", ".atlas"]
        filterFile = [r"LuaScript\MEGameStartup.lua", r"MEFramework\init.lua", r"MEFramework\Main.lua", "config1"]
        for path in changeList:
            if deleteList.get(path):
                del deleteList[path]
            relpath = os.path.relpath(path, tarpath)
            isNeedCopy = False
            for ext in filterExt:
                if relpath.find(ext) != -1:
                    isNeedCopy = True
                    break
            for ext in filterFile:
                if relpath.find(ext) != -1:
                    isNeedCopy = False
                    break
            if not isNeedCopy:
                continue
            # if relpath.startswith("res"):
            print 'copy file:', os.path.join(publicpath, relpath)
            pathdir = os.path.dirname(os.path.join(publicpath, relpath))
            if not os.path.isdir(pathdir):
                os.makedirs(pathdir) 
            shutil.copy(path, os.path.join(publicpath, relpath))
            sys.stdout.flush() 
        
        for key in deleteList.keys(): 
            relpath = os.path.relpath(key, tarpath) 
            if relpath.startswith(""):
                if os.path.exists(os.path.join(publicpath, relpath)):
                    print 'del file:', os.path.join(publicpath, relpath)
                    os.remove(os.path.join(publicpath, relpath))
                    sys.stdout.flush() 

    
    if os.path.exists(tmpfilename):
        os.remove(tmpfilename)
        
    with open(os.path.join(publicpath, "Revision"), "wb+") as tempFile:
        tempFile.write(str(right))
    pass

if __name__ == '__main__': 
    # try:
    work()
    os.system("pause")
    # except Exception, e:
        # print e