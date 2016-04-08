#coding=utf-8
'''
Created on 2015骞�12鏈�24鏃�

@author: Administrator
'''
import os
from queue import Queue
import re
import shutil

import Config
from process import Context, queueProcess, execCmd
from util import PackHelper, Log, Constant


def process(ctx):
    if run(ctx, removebom) :
        Log.printInfoln('鎰忓缁撴潫,removebom')
        return False
    if run(ctx, packimgdata) :
        Log.printInfoln('鎰忓缁撴潫,packimgdata')
        return False
    if run(ctx, poweroftwo_mapres_and_battlebg) :
        Log.printInfoln('鎰忓缁撴潫,poweroftwo_mapres_and_battlebg')
        return False
    if run(ctx, packimg_rgba_or_rgb_a8) :
        Log.printInfoln('鎰忓缁撴潫,packimg_rgba_or_rgb_a8')
        return False
    if run(ctx, packimg_rgb) :
        Log.printInfoln('鎰忓缁撴潫,packimg_rgb')
        return False
    if run(ctx, packimg_rgb_a8) :
        Log.printInfoln('鎰忓缁撴潫,packimg_rgb_a8')
        return False
    if run(ctx, gzip_pvr) :
        Log.printInfoln('鎰忓缁撴潫,gzip_pvr')
        return False
    if run(ctx, rename_alpha_jpg) :
        Log.printInfoln('鎰忓缁撴潫,rename_alpha_jpg')
        return False
    if run(ctx, data_encrypt) :
        Log.printInfoln('鎰忓缁撴潫,data_encrypt')
        return False
    return True
    
def run(ctx, createQueueFunc):
    if(os.path.exists(ctx.getTempPath())):
        shutil.rmtree(ctx.getTempPath(), True)
    os.makedirs(ctx.getTempPath(), exist_ok=True)
    errorQueue = createQueueFunc(ctx)
    if(os.path.exists(ctx.getTempPath())):
        shutil.rmtree(ctx.getTempPath(), True)
    return not errorQueue.empty()

# 鎵撳寘data鏂囦欢澶癸紝鎸夋枃浠跺す杞崲
def packimgdata(ctx):
    taskQueue = Queue()
    folderPackList = PackHelper.getFolderPackList(ctx.getOutputResPath())
    for folderPack in folderPackList :
        taskQueue.put((_packimgdata, ctx, folderPack))
    errorQueue = queueProcess(taskQueue);
    return errorQueue
    

# 闃熷垪涓苟琛屽鐞嗙殑瀛愭柟娉�
def _packimgdata(tid, ctx, folderPack):
    # 鍒犻櫎绾跨▼鎵�灞炰复鏃舵枃浠跺す
    tidPath = ctx.getTempPath() + os.sep + str(tid)
    if os.path.exists(tidPath) :
        shutil.rmtree(tidPath, True)
    # 澶嶅埗骞剁Щ闄よ繙鏂囦欢澶�
    dirName = os.path.basename(folderPack)
    dest = tidPath + os.sep + 'res' + os.sep + 'data' + os.sep + dirName
    shutil.copytree(folderPack, dest)
    shutil.rmtree(folderPack)
    # 鎵ц鎵撳寘鍛戒护
    cmd = str(Config.CMD_PACKIMG_DATA).format(tempPath=os.path.normpath(tidPath), srcPath=os.path.normpath(folderPack), baseName=dirName)
    retval = execCmd(cmd)
    # 鍒犻櫎绾跨▼涓存椂鏂囦欢澶�
    shutil.rmtree(tidPath)
    return retval == 0

# 鎵撳寘鎴樻枟鑳屾櫙
def poweroftwo_mapres_and_battlebg(ctx):
    taskQueue = Queue()
    for r, d, fileList in os.walk(ctx.getOutputResPath()) :
        for file in fileList :
            absFilePath = os.path.join(r, file)
            if re.match(Config.FILE_PACKIMG_SQUARE_REGEX, absFilePath) :
                taskQueue.put((_poweroftwo_mapres_and_battlebg, ctx, absFilePath))
    errorQueue = queueProcess(taskQueue);
    return errorQueue

# 闃熷垪涓苟琛屽鐞嗙殑瀛愭柟娉�
def _poweroftwo_mapres_and_battlebg(tid, ctx, filePath):
    cmd = str(Config.CMD_POWER_OF_TWO).format(fileName=filePath)
    retval = execCmd(cmd)
    return retval == 0

def packimg_rgba_or_rgb_a8(ctx):
    taskQueue = Queue()
    for r, d, fileList in os.walk(ctx.getOutputResPath()) :
        for file in fileList :
            absFilePath = os.path.join(r, file);
            if re.match(Config.FILE_PACKIMG_MODEL_REGEX, absFilePath) :
                taskQueue.put((_packimg_rgba_or_rgb_a8, ctx, absFilePath))
    errorQueue = queueProcess(taskQueue);
    return errorQueue

def _packimg_rgba_or_rgb_a8(tid, ctx, filePath):
    noneExt = os.path.splitext(filePath)[0]
    Log.printDetailln('exec packimg_data_single : ' + filePath)
    cmd = str(Config.CMD_CONVERT_COLOR_LEVEL).format(fileName=filePath)
    retval = execCmd(cmd)
    if retval != 0 : 
        return False
    if ctx.platformType == Constant.PLATFORM_IOS :
        # IOS鎵撳寘
        cmd = str(Config.CMD_PACKIMG_RGBA_PVR).format(fileName=filePath, noneExtName=noneExt)
        retval = execCmd(cmd)
    else:
        # 瀹夊崜鎵撳寘
        cmd = str(Config.CMD_PACKIMG_RGB_ETC).format(fileName=filePath, noneExtName=noneExt)
        retval = execCmd(cmd)
        if retval == 0 and re.match(r".*\.png", filePath) :
            cmd = str(Config.CMD_PACKIMG_A8).format(fileName=filePath, noneExtName=noneExt)
            retval = execCmd(cmd)
    os.remove(filePath)
    return retval == 0

# 鎵撳寘data鏂囦欢澶�  鍗曠嫭杞崲
def packimg_rgb(ctx):
    taskQueue = Queue()
    for r, d, fileList in os.walk(ctx.getOutputResPath()) :
        for file in fileList :
            absFilePath = os.path.join(r, file);
            if re.match(Config.FILE_PACKIMG_RGB_REGEX, absFilePath) :
                taskQueue.put((_packimg_rgb, ctx, absFilePath))
    errorQueue = queueProcess(taskQueue);
    return errorQueue

def _packimg_rgb(tid, ctx, filePath):
    noneExt = os.path.splitext(filePath)[0]
    Log.printDetailln('exec packimg_data_single : ' + filePath)
    cmd = str(Config.CMD_CONVERT_COLOR_LEVEL).format(fileName=filePath)
    retval = execCmd(cmd)
    if retval != 0 :
        return False
    if ctx.platformType == Constant.PLATFORM_IOS :
        # IOS鎵撳寘
        cmd = str(Config.CMD_PACKIMG_RGB_PVR).format(fileName=filePath, noneExtName=noneExt)
        retval = execCmd(cmd)
    else:
        # 瀹夊崜鎵撳寘
        cmd = str(Config.CMD_PACKIMG_RGB_ETC).format(fileName=filePath, noneExtName=noneExt)
        retval = execCmd(cmd)
    os.remove(filePath)
    return retval == 0
         
# 姣忓紶鍥捐浆鎹㈡垚 RGBA4444   
def packimg_rgb_a8(ctx):
    taskQueue = Queue()
    for r, d, fileList in os.walk(ctx.getOutputResPath()) :
        for file in fileList :
            absFilePath = os.path.join(r, file);
            if re.match(Config.FILE_PACKIMG_EFFECT_REGEX, absFilePath) :
                taskQueue.put((_packimg_rgb_a8, ctx, absFilePath))
    errorQueue = queueProcess(taskQueue);
    return errorQueue

def _packimg_rgb_a8(tid, ctx, filePath):
    noneExt = os.path.splitext(filePath)[0]
    Log.printDetailln('exe packimg_data_single : ' + filePath)
    if ctx.platformType == Constant.PLATFORM_IOS :
        # IOS鎵撳寘
        cmd = str(Config.CMD_PACKIMG_RGB_PVR).format(fileName=filePath, noneExtName=noneExt)
        retval = execCmd(cmd)
    else:
        # 瀹夊崜鎵撳寘
        cmd = str(Config.CMD_PACKIMG_RGB_ETC).format(fileName=filePath, noneExtName=noneExt)
        retval = execCmd(cmd)
    if retval == 0 and re.match(r".*\.png", filePath) :
        cmd = str(Config.CMD_PACKIMG_A8).format(fileName=filePath, noneExtName=noneExt)
        retval = execCmd(cmd)
    os.remove(filePath)
    return retval == 0

# PVR鍘嬬缉
def gzip_pvr(ctx):
    taskQueue = Queue()
    for r, d, fileList in os.walk(ctx.getOutputResPath()) :
        for file in fileList :
            absFilePath = os.path.join(r, file);
            if re.match(Config.FILE_GZIP_PVR_REGEX, absFilePath) :
                taskQueue.put((_gzip_pvr, ctx, absFilePath))
    errorQueue = queueProcess(taskQueue);
    return errorQueue

def _gzip_pvr(tid, ctx, filePath):
    cmd = str(Config.CMD_GZIP_PVR).format(fileName=filePath)
    retval = execCmd(cmd)
    os.remove(filePath)
    os.rename(filePath + '.gz', filePath)
    return retval == 0

def rename_alpha_jpg(ctx) :
    taskQueue = Queue()
    for r, d, fileList in os.walk(ctx.getOutputResPath()) :
        for file in fileList :
            absFilePath = os.path.join(r, file);
            if re.match(Config.FILE_ALPHA_JPG_REGEX, absFilePath) :
                taskQueue.put((_rename_alpha_jpg, ctx, absFilePath))
    errorQueue = queueProcess(taskQueue);
    return errorQueue

def _rename_alpha_jpg(tid, ctx, filePath) :
    os.rename(filePath, str(filePath).replace("jpg", "pvr"))
    return True

# lua杞瓧鑺傜爜
def lua_to_byte(ctx):
    taskQueue = Queue()
    for r, d, fileList in os.walk(ctx.getOutputResPath()) :
        for file in fileList :
            absFilePath = os.path.join(r, file);
            if re.match(Config.FILE_LUA_TO_BYTE_REGEX, absFilePath) :
                taskQueue.put((_lua_to_byte, ctx, absFilePath))
    errorQueue = queueProcess(taskQueue);
    return errorQueue

def _lua_to_byte(tid, ctx, filePath):
    cmd = str(Config.CMD_LUA_TO_BYTE).format(fileName=filePath)
    retval = execCmd(cmd)
    return retval == 0

# lua缂栬瘧
def luac_scriptlua(ctx):
    taskQueue = Queue()
    for r, d, fileList in os.walk(ctx.getOutputResPath()) :
        for file in fileList :
            absFilePath = os.path.join(r, file);
            if re.match(Config.FILE_LUAC_SCRIPTLUA_REGEX, absFilePath) :
                taskQueue.put((_luac_scriptlua, ctx, absFilePath))
    errorQueue = queueProcess(taskQueue);
    return errorQueue

def _luac_scriptlua(tid, ctx, filePath):
    cmd = str(Config.CMD_LUAC_SCRIPTLUA).format(fileName=filePath)
    retval = execCmd(cmd)
    return retval == 0

# 鏁版嵁鍔犲瘑
def data_encrypt(ctx):
    outCocosPath = ctx.getOutputResPath() + os.sep + 'scriptlua' + os.sep + 'cocos'
    tempCocosPath = ctx.getTempPath() + os.sep + 'cocos'
    if os.path.exists(outCocosPath) :
        shutil.copytree(outCocosPath, tempCocosPath)
    shutil.rmtree(outCocosPath)
    taskQueue = Queue()
    for folder in Config.FILE_DATA_ENCRYPT_INCLUDE :
        taskQueue.put((_data_encrypt, ctx, ctx.getOutputResPath() + os.sep + folder))
    errorQueue = queueProcess(taskQueue)
    if os.path.exists(tempCocosPath) :
        shutil.copytree(tempCocosPath, outCocosPath)
    return errorQueue
        
def _data_encrypt(tid, ctx, filePath):
    cmd = str(Config.CMD_DATA_ENCRYPT).format(folderName=filePath)
    retval = execCmd(cmd)
    return retval == 0
    
# 鏁版嵁搴撳姞瀵�
def sqlite_encrypt(ctx):
    dbFile = ctx.getOutputResPath() + os.sep + 'db' + os.sep + 'runehero.db'
    tempFile = Config.EXE_DBENCRYPT + os.sep + 'runehero.db'
    if os.path.exists(dbFile) and os.path.isfile(dbFile) :
        shutil.copyfile(dbFile, tempFile)
        os.remove(dbFile)
        retval = execCmd(Config.CMD_SQLITE_ENCRYPT)
        shutil.copyfile(tempFile, dbFile)
    return Queue()

# 澶勭悊绮掑瓙鐨刡om澶撮棶棰�
def removebom(ctx):
    taskQueue = Queue()
    for r, d, fileList in os.walk(ctx.getOutputResPath()) :
        for file in fileList :
            absFilePath = os.path.join(r, file);
            if re.match(Config.FILE_REMOVE_BOM_REGEX, absFilePath) :
                taskQueue.put((_removebom, ctx, absFilePath))
    errorQueue = queueProcess(taskQueue);
    return errorQueue

def _removebom(tid, ctx, filePath):
    Log.printDetailln('UTF-8 remove bom : ' + filePath)
    cmd = str(Config.CMD_REMOVE_BOM).format(fileName=filePath)
    retval = execCmd(cmd)
    return retval == 0
