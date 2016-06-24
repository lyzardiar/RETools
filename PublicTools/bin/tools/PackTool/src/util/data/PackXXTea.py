# -*- coding: utf-8 -*-
from util.data import xxtea
from util import Log

def Is(absFilePath):
    return xxtea.Is(absFilePath)
    
def encode(absFilePath):
    KEY = b"XG"
    HEAD = b"DDTX"
    
    with open(absFilePath, "rb") as tmpFile:
        content = tmpFile.read()
    
    # already encoded
    if len(content) >=4 and content[0:4] == b'DDTX':
        return 0        
    
    content = HEAD + xxtea.encrypt(content, KEY)
    
    with open(absFilePath, "wb+") as tmpFile:
        tmpFile.write(content)
        
    return 0