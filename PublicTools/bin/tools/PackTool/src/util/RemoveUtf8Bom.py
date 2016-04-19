# -*- coding: utf-8 -*-

def remove(absFilePath, realPath = ''):
    tmpFile = open(absFilePath, "rb")
    content = tmpFile.read()    
    tmpFile.close()
    
    if len(content) < 3:
        return 0

    if content[0:3] == b'\xef\xbb\xbf':
        content = content[3:]
        tmpFile = open(absFilePath, "wb+")
        tmpFile.write(content)
        tmpFile.close()
        
        if realPath != '':
            print("[Bom] removed: %s" % (realPath))
    
    return 0
    