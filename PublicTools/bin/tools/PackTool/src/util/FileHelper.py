import os
import sys
import struct
import platform
from util import toolsPath

if platform.system() == "Windows":
    gzipBin = "gzip.exe " 
    convertBin = "convert.exe " 
    pvrTexToolBin = "PVRTexToolCLI.exe "
else:
    convertBin = os.path.join(toolsPath, "bin/ios/x86/convert ") 
    gzipBin = "gzip "
    pvrTexToolBin = os.path.join(toolsPath, "bin/ios/x86/PVRTexToolCLI ")


# iterator dir
def dir_iter(path, fnexp):
    for root, dirs, files, in os.walk(path):
        for filename in fnmatch.filter(files, fnexp):
            yield os.path.join(root, filename)

# remove file
def remove(filepath):
    if os.path.exists(filepath):
        return os.remove(filepath)
    return True

# rename file
def rename(oldname, newname):
    return os.rename(oldname, newname)

# real path
def realpath(path):
    return os.path.realpath(path)

# dir name
def dirname(path):
    return os.path.dirname(path)

# dir name
def basename(path):
    return os.path.basename(path)

# dir name
def exists(path):
    return os.path.exists(path)

def join(direct, path):
    return os.path.join(direct, path)

def writeWithSize(file, path):
    """
        write a file into another file with its size at front
    """

    filename = realpath(path)
    statinfo = os.stat(filename)
    fileSize = statinfo.st_size
    
    file.write(struct.pack("i", fileSize))
    with open(filename, "rb") as rgbfile:
        file.write(rgbfile.read())