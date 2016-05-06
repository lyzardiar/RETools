import sys, os
import Image

curPath = os.path.dirname(os.path.realpath(__file__))

argCount = len(sys.argv)
fileName = curPath + "/icon.png"

if (argCount > 1):
    fileName = os.path.realpath(sys.argv[1])

print(fileName)
fileDir = os.path.dirname(fileName)
print(fileDir)
    
imgSize = [29, 40, 50, 57, 58, 72, 76, 80, 87, 100, 114, 120, 144, 152, 167, 180]

img = Image.open(fileName)
img = img.convert("RGBA")

for size in imgSize:
    newImg = img.resize((size, size), Image.ANTIALIAS)
    newFileName = fileDir + ("/Icons/Icon%d.png" % (size))
    if not os.path.exists(os.path.dirname(newFileName)):
        os.makedirs(os.path.dirname(newFileName))
    newImg.save(newFileName, quality=100)
    pass
    
