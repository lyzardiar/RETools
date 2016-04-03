from PIL import Image
import sys, os, math

curPath = os.path.dirname(os.path.realpath(__file__))

sizeList = [(320, 480), (640, 960), (640, 1136), (750, 1334), (1242, 2208), (1024, 748), (1024, 768), (2048, 1496), (2048, 1536), (2208, 1242)]

scale = 0.9 * 0.7 * 0.6

for size in sizeList:
    imgContent = Image.open(curPath + "/ui_logo_01.jpg")
    
    logoWidth = imgContent.size[0]
    logoHeight = imgContent.size[1]
    
    screenWidth = size[0]
    screenHeight = size[1]
    
    localScale = scale
    isLandscape = True
    if screenWidth < screenHeight:
        isLandscape = False
        screenWidth = size[1]
        screenHeight = size[0]        
    
    width = int(screenWidth * localScale)
    height = int(width * logoHeight / logoWidth)
    
    x = (screenWidth - width + width * 0.1)/2.0
    y = (screenHeight - height)/2.0
    pos = (int(x), int(y))
    
    imgContent = imgContent.resize((width, height), Image.ANTIALIAS)

    im = Image.new("RGB", (screenWidth, screenHeight), "white")
    im.paste(imgContent, (pos[0], pos[1]))
    if not isLandscape:
        im = im.rotate(90)
    im.save(curPath + "/Default" + str(size[0]) + "x" + str(size[1]) + ".png" , quality=95)