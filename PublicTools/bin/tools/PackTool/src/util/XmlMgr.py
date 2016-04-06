#coding=utf-8  
'''
Created on 2015年12月26日

@author: Administrator
'''
from datetime import time, datetime
import os
from xml.dom import minidom

from util.Scanner import FileData, FileScanner


def read(path):
    doc = minidom.parse(path)
    fileDatas = []
    fileDict = {}
    fileTags = doc.getElementsByTagName('File')
    for fileTag in fileTags :
        relativePath = fileTag.getAttributeNode('RelativePath').nodeValue
        md5 = fileTag.getAttributeNode('Md5').nodeValue
        size = fileTag.getAttributeNode('Size').nodeValue
        fileData = FileData(parentPath='', relativePath=relativePath, md5=md5, size=size)
        fileDatas.append(fileData)
        fileDict[fileData.relativePath] = fileData
    fileScanner = FileScanner()
    fileScanner.initFromXml(fileDatas, fileDict);
    return fileScanner

def write(path, fileList):
    impl = minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'FileList', None)
    fileListNode = dom.documentElement
    fileListNode.setAttribute('Date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    fileListNode.setAttribute('Size', str(len(fileList)))
    for fileData in fileList :
        node = dom.createElement('File')
        node.setAttribute('Name', os.path.basename(fileData.relativePath))
        node.setAttribute('RelativePath', fileData.relativePath)
        node.setAttribute('Md5', fileData.md5)
        node.setAttribute('Size', str(fileData.size))
        fileListNode.appendChild(node)
    f = open(path, 'w', encoding='utf-8')
    dom.writexml(f, addindent='  ', newl='\n', encoding='utf-8')
    f.close()
