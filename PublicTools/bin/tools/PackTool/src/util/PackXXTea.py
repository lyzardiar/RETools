# -*- coding: utf-8 -*-
from util import xxtea

def Is(absFilePath):
    return xxtea.Is(absFilePath)
    
def encode(absFilePath):
    KEY = b"XG"
    HEAD = b"DDTX"
    
    tmpFile = open(absFilePath, "rb")
    content = tmpFile.read()    
    tmpFile.close()
    
    # already encoded
    if len(content) >=4 and content[0:4] == b'DDTX':
        return 0        
    
    content = HEAD + xxtea.encrypt(content, KEY)
    
    tmpFile = open(absFilePath, "wb+")
    tmpFile.write(content)
    tmpFile.close()
        
    return 0