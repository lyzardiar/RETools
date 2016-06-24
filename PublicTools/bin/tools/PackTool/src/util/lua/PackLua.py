# -*- coding: utf-8 -*-
import os
from process import queueProcess, execCmd
from util.data import PackXXTea, RemoveUtf8Bom

import util

projectdir      = util.toolsPath

# win32 and android
LuaJitBin       = os.path.join(projectdir, "bin/win32/luajit.exe")
LuaBin          = os.path.join(projectdir, "bin/win32/luac.exe")


# iOS 
LuaJitiOSx86Dir = os.path.join(projectdir, "bin/ios/x86/")
LuaJitiOSx64Dir = os.path.join(projectdir, "bin/ios/x86_64/")

LuaJitiOSx86Bin = os.path.join(projectdir, "bin/ios/x86/luajit")
LuaJitiOSx64Bin = os.path.join(projectdir, "bin/ios/x86_64/luajit")

class PackLua():
    """
        PackLua
    """
    def __init__(self, useJit = True, isiOS = False):
        self.useJit = useJit
        self.isiOS = isiOS
        self.JitCompileCMD = ""
        self.JitCompileCMD2 = ""

        self.updateCMD(self.useJit, self.isiOS)

    def updateCMD(self, _useJit = True, _isiOS = False):        
        self.useJit = _useJit
        self.isiOS = _isiOS

        if self.useJit:
            if self.isiOS:
                self.JitCompileCMD = LuaJitiOSx86Bin + " -b {filename} {filename}.32" 
                self.JitCompileCMD2 = LuaJitiOSx64Bin + " -b {filename} {filename}.64" 
            else:
                self.JitCompileCMD = LuaJitBin + " -b {filename} {filename}" 
        else:
            self.JitCompileCMD = LuaBin + " -s -o {filename}c {filename}" 

    def __compileLuaJitiOS(self, absFilePath):
        os.chdir(LuaJitiOSx86Dir)
        execCmd(self.JitCompileCMD.format(filename = absFilePath))
        
        os.chdir(LuaJitiOSx64Dir)
        execCmd(self.JitCompileCMD2.format(filename = absFilePath))
        
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

    def __compileLuac(self, absFilePath, relativepath = ''):
        if PackXXTea.Is(absFilePath):
            return 0
            
        RemoveUtf8Bom.remove(absFilePath, relativepath)
        
        ret = 0    
        ret = execCmd(self.JitCompileCMD.format(filename = absFilePath))    
    
        if os.path.exists(absFilePath + 'c'):
            ret = PackXXTea.encode(absFilePath + 'c')  
                
            if os.path.exists(absFilePath):
                os.remove(absFilePath)
                
            os.rename(absFilePath + 'c', absFilePath)         
        else:
            return 1
            
        return 0
        
        
    def __compileLua(self, absFilePath, relativepath = ''):
        ret = 0
        if absFilePath.find('LuaScript') != -1 or absFilePath.find('Core') != -1:
            if absFilePath.find('/ui/') == -1 and absFilePath.find('\\ui\\') == -1:
                if absFilePath.find('/Scene/') == -1 and absFilePath.find('\\Scene\\') == -1:
                    ret = PackXXTea.encode(absFilePath)        
        return ret

    def __compileLuaJit(self, absFilePath, relativepath = ''):
        if self.useJit:
            if self.isiOS:
                ret = self.__compileLuaJitiOS(absFilePath)
            else:
                ret = execCmd(self.JitCompileCMD.format(filename = absFilePath))
        else:
            return self.__compileLua(absFilePath, relativepath)  
        return ret
        
    
    def compile(self, absFilePath, relativepath = ''):
        return self.__compileLuaJit(absFilePath, relativepath)    