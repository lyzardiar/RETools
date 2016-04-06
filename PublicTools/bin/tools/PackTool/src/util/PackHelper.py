#coding=utf-8  
'''
Created on 2015年12月26日

@author: Administrator
'''
'''
返回打大图的文件夹列表
'''

import hashlib
import os

from Config import FILE_FOLDER_PACK_INCLUDE, FILE_FOLDER_PACK_EXCLUDE


def getFolderPackList(resPath):
    excludeList = [os.path.join(resPath,x) for x in FILE_FOLDER_PACK_EXCLUDE if os.path.exists(os.path.join(resPath,x))]
    folderList = []
    for includeSub in FILE_FOLDER_PACK_INCLUDE :
        includeSubAbs = os.path.join(resPath, includeSub)
        if not os.path.exists(includeSubAbs) :
            continue
        for subFolder in os.listdir(includeSubAbs) :
            subFolderAbs = os.path.join(includeSubAbs, subFolder)
            if os.path.isfile(subFolderAbs) :
                continue
            isExclude = False
            if os.path.isdir(subFolderAbs) :
                for excludeFolder in excludeList :
                    if os.path.samefile(excludeFolder, subFolderAbs) :
                        isExclude = True
                        break;
            if not isExclude :
                folderList.append(os.path.normpath(subFolderAbs))
    return folderList

def calcMd5(path):
    fd = open(path, 'rb')
    fcont = fd.read()
    fd.close()
    fmd5 = hashlib.md5(fcont)
    return fmd5.hexdigest()