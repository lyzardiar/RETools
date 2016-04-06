#coding=utf-8  
'''
Created on 2015年12月23日

@author: Administrator
'''
import configparser
import os
from xml.dom import minidom


ROOT_FILE_XML = 'packroots.xml'
ROOT_FILE_INI = 'root.ini'

rootPathList = []

def updateRoot(rootPath):
    if rootPath not in rootPathList:
        rootPathList.insert(0, rootPath)
        write()
    else :
        index = rootPathList.index(rootPath)
        rootPathList[index:index + 1] = []
        rootPathList.insert(0, rootPath)
        write()

def load():
    if os.path.exists(ROOT_FILE_XML) :
        rootPathList.clear()
        doc = minidom.parse(ROOT_FILE_XML)
        rootTags = doc.getElementsByTagName('root')
        for rootTag in rootTags :
            rootPathList.append(rootTag.childNodes[0].nodeValue)

def write():
    impl = minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'roots', None)
    roots = dom.documentElement
    for root in rootPathList :
        nodeT = dom.createElement('root')
        nodeV = dom.createTextNode(root)
        nodeT.appendChild(nodeV)
        roots.appendChild(nodeT)
    f = open(ROOT_FILE_XML, 'w', encoding='utf-8')
    dom.writexml(f, addindent='  ', newl='\n', encoding='utf-8')
    f.close()

class RootInfo:
    
    srcPath = ''
    platform = ''
    
    def __init__(self, srcPath, platform):
        self.srcPath = srcPath
        self.platform = platform
    
def loadRootInfo(path):
    iniFilePath = path + '/' + ROOT_FILE_INI
    if os.path.exists(iniFilePath) :
        conf = configparser.ConfigParser();
        conf.read(iniFilePath)
        _srcPath = conf.get('option', 'srcpath')
        _platform = conf.get('option', 'platform')
        return RootInfo(_srcPath, _platform)
    return None

def writeRootInfo(path, srcPath, platform):
    conf = configparser.ConfigParser();
    conf.add_section('option')
    conf.set('option', 'srcpath', srcPath)
    conf.set('option', 'platform', platform)
    f = open(path + '/' + ROOT_FILE_INI, 'w')
    conf.write(f)
    f.close()
