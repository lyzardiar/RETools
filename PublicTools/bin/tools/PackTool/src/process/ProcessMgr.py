#coding=utf-8  
'''
Created on 2015年12月23日

@author: Administrator
'''
from concurrent.futures.thread import ThreadPoolExecutor
from distutils import dir_util
from functools import cmp_to_key
import hashlib
import os
import re
import shutil
import sys
import traceback

from process import Context, PackProcess
from util import Log, PackHelper, XmlMgr, Constant
from util.Scanner import FileScanner


ctx = Context()
threadPool = ThreadPoolExecutor(1)

'''
创建打包上下文环境
'''
def createContext(rootPath):
    global ctx
    ctx = Context()
    ctx.rootPath = rootPath
    
    dataPath = ctx.getDataFolder()
    if not os.path.exists(dataPath) :
        os.makedirs(dataPath, exist_ok=True)
    
    # 找到所有版本文件
    Log.printInfoln('Root path : ' + dataPath)
    
    releaseList = []
    for file in os.listdir(dataPath) :
        absPath = os.path.join(dataPath, file)
        if os.path.isdir(absPath) and re.match(Constant.VERSION_REGEX, file):
            if os.path.exists(absPath + os.sep + Constant.BEFORE_XML) and os.path.exists(absPath + os.sep + Constant.AFTER_XML) :
                releaseList.append(absPath);
    
    if len(releaseList) == 0 :
        Log.printInfoln('找不到已release包,当前打包为全新打包')
        return;
    
    releaseList.sort(key=lambda x : int(os.path.basename(x)), reverse=True)
    lastReleaseFolderPath = releaseList[0];
    Log.printInfoln('当前对比路径为 : ' + lastReleaseFolderPath)
    ctx.lastReleasePath = lastReleaseFolderPath
        
'''
开始打包
'''
def start(resPath, platformType, isNew, isFull):
    ctx.resPath = resPath
    ctx.platformType = platformType
    ctx.isNew = isNew
    ctx.isFull = isFull
    
    threadPool.submit(process, ctx)
    
def process(ctx=Context()):
    try:
        Log.printInfoln('==============开始打包==============')
        if not os.path.isdir(ctx.resPath) :
            Log.printInfoln('源目录不存在, resPath : ' + ctx.resPath)
            return;
        
        if os.path.exists(ctx.getOutputPath()) :
            shutil.rmtree(ctx.getOutputPath(), True)
            Log.printDetailln('删除目录 : ' + ctx.getOutputPath())
        
        if os.path.exists(ctx.getTempPath()) :
            shutil.rmtree(ctx.getTempPath(), True)
            Log.printDetailln('删除目录 : ' + ctx.getTempPath())
            
        # 不管新包还是旧包，release数据备份都不已md5命名，只有export里用md5命名
        if os.path.exists(ctx.getExportPath()) :
            shutil.rmtree(ctx.getExportPath(), True)
            Log.printDetailln('删除目录 : ' + ctx.getExportPath())
            
        Log.printInfo('【1/4】<1/1> 扫描并计算MD5...')
        ctx.curScanner = FileScanner()
        ctx.curScanner.initFromRootPath(ctx.resPath)
        Log.printInfoln('完成')
        
        os.makedirs(ctx.getDataFolder(), exist_ok=True)
        
        # 路径比较的时候加入root前缀，然后判断是不是同一个文件，不需要直接判断相对路径
        ctx.folderPackList = PackHelper.getFolderPackList(ctx.resPath)
        
        # 从output文件件到release文件夹的备份
        if ctx.isNew or ctx.lastReleasePath == '':
            Log.printInfo('复制完整文件夹, from : ' + ctx.resPath + ", to : " + ctx.getOutputResPath() + ' ...')
            shutil.copytree(ctx.resPath, ctx.getOutputResPath())
            Log.printInfoln('完成')
            if not PackProcess.process(ctx) :
                return
            Log.printInfo('复制完整文件夹, from : ' + ctx.getOutputResPath() + ", to : " + ctx.getReleaseOutputPath() + ' ...')
            shutil.copytree(ctx.getOutputPath(), ctx.getReleaseOutputPath())
            Log.printInfoln('完成')
        else :
            removeSet = set()
            if not compareAndPack(ctx, removeSet) :
                return
            Log.printInfo('复制最近release版本 to : ' + ctx.getReleaseOutputPath() + ' ...')
            shutil.copytree(ctx.lastReleasePath, ctx.getReleaseOutputPath())
            Log.printInfoln('完成')
            
            Log.printInfo('删除失效文件(' + str(len(removeSet)) + '个)...')
            # 删除removeSet中的文件和文件夹
            for removeRelPath in removeSet :
                removeAbsPath = os.path.join(ctx.getReleaseOutputPath() + os.sep + 'res', removeRelPath)
                if not os.path.exists(removeAbsPath) :
                    continue
                if os.path.isfile(removeAbsPath) :
                    os.remove(removeAbsPath)
                elif os.path.isdir(removeAbsPath) :
                    shutil.rmtree(removeAbsPath)
            
            dir_util.copy_tree(ctx.getOutputPath(), ctx.getReleaseOutputPath())
            Log.printInfoln('完成')
            
        # 生成xml-before
        Log.printInfo('生成Xml-before...')
        beforeXml = ctx.getReleaseOutputPath() + os.sep + Constant.BEFORE_XML
        XmlMgr.write(beforeXml, ctx.curScanner.fileList)
        Log.printInfoln('完成')
        
        # 生成xml-after
        Log.printInfo('生成Xml-after...')
        afterScanner = FileScanner()
        afterScanner.initFromRootPath(ctx.getReleaseOutputPath() + os.sep + 'res')
        afterXml = ctx.getReleaseOutputPath() + os.sep + Constant.AFTER_XML
        XmlMgr.write(afterXml, afterScanner.fileList)
        Log.printInfoln('完成')
        
        os.makedirs(ctx.getExportPath(), exist_ok=True)
        
        Log.printInfo('导出变更文件到export目录...')
        if ctx.isFull :
            for r, d, fileList in os.walk(ctx.getReleaseOutputPath() + os.sep + 'res') :
                for file in fileList :
                    srcAbsPath = os.path.join(r, file)
                    relativePath = os.path.relpath(srcAbsPath, ctx.getReleaseOutputPath())
                    targetPath = os.path.join(ctx.getExportPath(), relativePath + '_' + PackHelper.calcMd5(srcAbsPath))
                    os.makedirs(os.path.dirname(targetPath), exist_ok=True)
                    shutil.copyfile(srcAbsPath, targetPath)
        else :
            for r, d, fileList in os.walk(ctx.getOutputPath()) :
                for file in fileList :
                    srcAbsPath = os.path.join(r, file)
                    relativePath = os.path.relpath(srcAbsPath, ctx.getOutputPath())
                    targetPath = os.path.join(ctx.getExportPath(), relativePath + '_' + PackHelper.calcMd5(srcAbsPath))
                    os.makedirs(os.path.dirname(targetPath), exist_ok=True)
                    shutil.copyfile(srcAbsPath, targetPath)
        xmlMd5 = PackHelper.calcMd5(afterXml)
        
        # 生成文件列表
        shutil.copyfile(afterXml, ctx.getExportPath() + os.sep + xmlMd5)
        
        # 生成version文件
        output = open(ctx.getExportPath() + os.sep + 'version.html', 'w')
        output.write('{\n')
        output.write('\tmd5:\"' + xmlMd5 + '\"\n')
        output.write('}')
        output.close()
        Log.printInfoln('完成')
        
    except :
        t, v, tb = sys.exc_info()
        print(t, v)
        traceback.print_tb(tb)   
        
def compareAndPack(ctx, removeSet):
    if os.path.exists(ctx.getOutputPath()) :
        shutil.rmtree(ctx.getOutputPath(), True)
        
    Log.printInfo('扫描对比列表...')
    lastScanner = XmlMgr.read(ctx.lastReleasePath + os.sep + Constant.BEFORE_XML)
    
    # 遍历更新文件夹找出需要copy到工作区的文件
    fileDatas = ctx.curScanner.getUpdateFileLists(lastScanner)
    copySet = set()
    for fileData in fileDatas :
        path = fileData.getAbsPath()
        relPath = fileData.relativePath
        # 打了大图的文件夹需要整个删除重来
        for folderPath in PackHelper.getFolderPackList(ctx.resPath) :
            if str(path + os.sep).find(folderPath + os.sep) >= 0 :
                relPath = os.path.relpath(folderPath, ctx.resPath)
                removeSet.add(relPath)
                break;
        copySet.add(relPath)
    
    # 遍历删除的文件，找出大图文件有删除的重新打包
    removeDatas = ctx.curScanner.getRemoveFileLists(lastScanner)
    for fileData in removeDatas :
        path = os.path.normpath(os.path.join(ctx.resPath, fileData.relativePath))
        relPath = fileData.relativePath
        # 打大图的文件夹内有文件被删除,需要整个大图文件夹重新打包一遍
        for folderPath in PackHelper.getFolderPackList(ctx.resPath) :
            if str(path + os.sep).find(folderPath + os.sep) >= 0 :
                relPath = os.path.relpath(folderPath, ctx.resPath)
                copySet.add(relPath)
                break;
        removeSet.add(relPath)
        if re.match(r'^.*\.((jpg)|(png)|(jpeg))$', relPath) :
            noneExtPath = os.path.splitext(relPath)[0]
            removeSet.add(noneExtPath + '.pvr')
            removeSet.add(noneExtPath + '._alpha.pvr')
    Log.printInfoln('完成')
    
    # 复制文件
    os.makedirs(ctx.getOutputPath())
    Log.printDetail('复制打包文件...')
    for relativePath in copySet :
        targetPath = ctx.getOutputResPath() + os.sep + relativePath;
        sourcePath = ctx.resPath + os.sep + relativePath;
        if not os.path.exists(sourcePath) :
            Log.printDetailln('复制失败, 文件或文件夹不存在, path : ' + sourcePath)
            continue
        if os.path.isdir(sourcePath) :
            shutil.copytree(sourcePath, targetPath)
        elif os.path.isfile(sourcePath) :
            os.makedirs(os.path.dirname(targetPath), exist_ok=True)
            shutil.copyfile(sourcePath, targetPath)
        else :
            Log.printDetailln('复制失败, path : ' + sourcePath)
    Log.printDetailln('完成')
    
    # 开始打包
    Log.printDetailln('开始打包')
    if len(copySet) != 0 :
        if not PackProcess.process(ctx) :
            return False
    Log.printDetailln('打包完成')
    return True
    
