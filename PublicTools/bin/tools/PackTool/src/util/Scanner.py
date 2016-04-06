#coding=utf-8  
'''
Created on 2015年12月25日

@author: Administrator
'''
import hashlib
import os
import itertools


class FileData :
    def __init__(self, parentPath, relativePath, md5, size):
        self.parentPath = os.path.normpath(parentPath)
        self.relativePath = os.path.normpath(relativePath)
        self.md5 = md5
        self.size = size
        
    def getAbsPath(self):
        return os.path.normpath(os.path.join(self.parentPath, self.relativePath))
    
#     def __hash__(self):  
#         return hash(self.parentPath + ' ' + self.relativePath + ' ' + self.md5)
#     
#     def __eq__(self, obj):
#         if isinstance(obj, FileData) and obj.relativePath == self.relativePath :
#             return True;
#         return False;
    
class FileScanner :
    
    def __init__(self):
        self.fileList = []
        self.fileDict = {}
        self.rootPath = ''
        
    def initFromXml(self, fileList, fileDict):
        self.fileList = fileList
        self.fileDict = fileDict

    def initFromRootPath(self, rootPath):
        self.rootPath = rootPath
        self.fileList.clear()
        for root, dirs, files in os.walk(rootPath) :
            for file in files :
                absFilePath = os.path.join(root, file)
                md5, size = self.readFile(absFilePath)
                fileData = FileData(rootPath, os.path.relpath(absFilePath, rootPath), md5, size)
                self.fileList.append(fileData)
                self.fileDict[fileData.relativePath] = fileData
                
    '''
            对比取删除的
    '''     
    def getRemoveFileLists(self, fileScanner):
        removePaths = []
        for targetFileData in fileScanner.fileList :
            if self.fileDict.get(targetFileData.relativePath) is None :
                removePaths.append(targetFileData)
        return removePaths
    
    '''
            对比更新的
    '''
    def getUpdateFileLists(self, fileScanner):
        updatePaths = []
        for sourceFileData in self.fileList :
            targetFileData = fileScanner.fileDict.get(sourceFileData.relativePath)
            if targetFileData is None :
                updatePaths.append(sourceFileData)
            elif sourceFileData.md5 != targetFileData.md5 :
                updatePaths.append(sourceFileData)
        return updatePaths
                
    def readFile(self, filePath):
        fd = open(filePath, 'rb')
        fcont = fd.read()
        fd.close()
        fmd5 = hashlib.md5(fcont)
        size = len(fcont)
        return fmd5.hexdigest(), size
