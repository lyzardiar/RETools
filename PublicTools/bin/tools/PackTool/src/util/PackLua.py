# -*- coding: utf-8 -*-
import os
from process import queueProcess, execCmd
from util import PackXXTea, RemoveUtf8Bom

projectdir = os.path.dirname(os.path.realpath(__file__))
LuaJitBin = os.path.join(projectdir, "../../../bin/win32/luajit.exe")
LuaBin = os.path.join(projectdir, "../../../bin/win32/luac.exe")

useJit = False

if useJit:
    JitCompileCMD = LuaJitBin + " -b {filename} {filename}" 
else:
    JitCompileCMD = LuaBin + " -s -o {filename}c {filename}" 

errorFils = []

def __compileLuac(absFilePath, relativepath = ''):
    if PackXXTea.Is(absFilePath):
        return 0
        
    RemoveUtf8Bom.remove(absFilePath, relativepath)
    
    ret = 0    
    ret = execCmd(JitCompileCMD.format(filename = absFilePath))    
   
    if os.path.exists(absFilePath + 'c'):
        ret = PackXXTea.encode(absFilePath + 'c')  
            
        if os.path.exists(absFilePath):
            os.remove(absFilePath)
            
        os.rename(absFilePath + 'c', absFilePath)         
    else:
        return 1
        
    return 0
    
    
def __compileLua(absFilePath, relativepath = ''):
    ret = 0
    if absFilePath.find('LuaScript') != -1 or absFilePath.find('MEFramework') != -1:
        if absFilePath.find('/ui/') == -1 and absFilePath.find('\\ui\\') == -1:
            if absFilePath.find('/Scene/') == -1 and absFilePath.find('\\Scene\\') == -1:
                ret = PackXXTea.encode(absFilePath)        
    return ret

def __compileLuaJit(absFilePath, relativepath = ''):
    if useJit:
        ret = execCmd(JitCompileCMD.format(filename = absFilePath))
    else:
        # return __compileLuac(absFilePath, relativepath) 
        return __compileLua(absFilePath, relativepath)  
    return ret
    
 
def compile(absFilePath, relativepath = ''):
    return __compileLuaJit(absFilePath, relativepath)    