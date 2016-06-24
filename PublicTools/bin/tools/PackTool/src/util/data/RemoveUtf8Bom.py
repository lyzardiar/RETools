# -*- coding: utf-8 -*-
from util import Log

def remove(absFilePath, realPath = ''):
    with open(absFilePath, "rb") as tmpFile:
        content = tmpFile.read()    
    
    if len(content) < 3:
        return 0

    if content[0:3] == b'\xef\xbb\xbf':
        content = content[3:]
        with open(absFilePath, "wb+") as tmpFile:
            tmpFile.write(content)
        
        if realPath != '':
            Log.printDetailln("[Bom] removed: %s" % (realPath))
    
    return 0
    