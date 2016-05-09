# -*- coding: utf-8 -*-
import os
from process import queueProcess, execCmd
from util import PackXXTea, RemoveUtf8Bom

projectdir = os.path.dirname(os.path.realpath(__file__))
LuaJitBin = os.path.join(projectdir, "../../../bin/win32/luajit.exe")
LuaBin = os.path.join(projectdir, "../../../bin/win32/luac.exe")

LuaJitiOSx86Dir = os.path.join(projectdir, "../../../bin/ios/x86/")
LuaJitiOSx64Dir = os.path.join(projectdir, "../../../bin/ios/x86_64/")

LuaJitiOSx86Bin = os.path.join(projectdir, "../../../bin/ios/x86/luajit")
LuaJitiOSx64Bin = os.path.join(projectdir, "../../../bin/ios/x86_64/luajit")

useJit = True
isiOS = True
JitCompileCMD = ""
JitCompileCMD2 = ""

def updateCMD(_useJit = True, _isiOS = True):
    global useJit, isiOS, JitCompileCMD, JitCompileCMD2
    
    useJit = _useJit
    isiOS = _isiOS

    if useJit:
        if isiOS:
            JitCompileCMD = LuaJitiOSx86Bin + " -b {filename} {filename}.32" 
            JitCompileCMD2 = LuaJitiOSx64Bin + " -b {filename} {filename}.64" 
            print(JitCompileCMD)
        else:
            JitCompileCMD = LuaJitBin + " -b {filename} {filename}" 
    else:
        JitCompileCMD = LuaBin + " -s -o {filename}c {filename}" 
        
updateCMD()

errorFils = []

def __compileLuaJitiOS(absFilePath):
    os.chdir(LuaJitiOSx86Dir)
    execCmd(JitCompileCMD.format(filename = absFilePath))
    
    os.chdir(LuaJitiOSx64Dir)
    execCmd(JitCompileCMD2.format(filename = absFilePath))
    
    filepath32 = absFilePath+'.32'
    filepath64 = absFilePath+'.64'
    
    if os.path.exists(filepath32) and os.path.exists(filepath64):
        if os.path.exists(absFilePath):
            os.remove(absFilePath)
        return 0
    else:
        if os.path.exists(filepath32):
            os.remove(filepath32)
        if os.path.exists(filepath64):
            os.remove(filepath64)
        return 1

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
    if absFilePath.find('LuaScript') != -1 or absFilePath.find('Core') != -1:
        if absFilePath.find('/ui/') == -1 and absFilePath.find('\\ui\\') == -1:
            if absFilePath.find('/Scene/') == -1 and absFilePath.find('\\Scene\\') == -1:
                ret = PackXXTea.encode(absFilePath)        
    return ret

def __compileLuaJit(absFilePath, relativepath = ''):
    if useJit:
        if isiOS:
            ret = __compileLuaJitiOS(absFilePath)
        else:
            ret = execCmd(JitCompileCMD.format(filename = absFilePath))
    else:
        # return __compileLuac(absFilePath, relativepath) 
        return __compileLua(absFilePath, relativepath)  
    return ret
    
 
def compile(absFilePath, relativepath = ''):
    return __compileLuaJit(absFilePath, relativepath)    