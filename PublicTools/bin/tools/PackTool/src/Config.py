#coding=utf-8  
# 根文件夹
import os
EXE_FOLDER = os.path.normpath(r'G:\pack_Tool')

EXE_TEXTUREPACKERHELP = os.path.normpath(EXE_FOLDER + r'/TexturePacker/TexturePacker-help.py')
EXE_TEXTUREPACKER = os.path.normpath(EXE_FOLDER + r'/TexturePacker/TexturePacker.exe')
EXE_PVRTEXTOOL = os.path.normpath(EXE_FOLDER + r'/pvrtextool/PVRTexTool.exe')
EXE_PNGQUANT = os.path.normpath(EXE_FOLDER + r'/pngquant/pngquant.exe')
EXE_LUAJIT = os.path.normpath(EXE_FOLDER + r'/luajit_win32/luajit.exe')
EXE_LUAC = os.path.normpath(EXE_FOLDER + r'/luajit_win32/luac.exe')
EXE_7Z = os.path.normpath(EXE_FOLDER + r'/7z/7z.exe')
EXE_PHPPACK = os.path.normpath(EXE_FOLDER + r'/enCode_Res/pack_files.bat')
EXE_DBENCRYPT = os.path.normpath(EXE_FOLDER + r'/enCode_sqlite')
EXE_REMOVEBOM = os.path.normpath(EXE_FOLDER + r'/removebom.exe')
EXE_CONVERT = os.path.normpath(EXE_FOLDER + r'/imagemagick/convert.exe')

ENCRYPT_KEY = 'jasontian'

CMD_PACKIMG_DATA = 'python ' + EXE_TEXTUREPACKERHELP + ' -t ' + EXE_TEXTUREPACKER + ' -i {tempPath} -d {srcPath}\{baseName}_{{n}}.plist -s {srcPath}\{baseName}_{{n}}.png'
CMD_POWER_OF_TWO = EXE_TEXTUREPACKER + ' {fileName} --force-squared --data c:/temp.plist --sheet {fileName} --padding 0 --trim-mode None'
CMD_CONVERT_COLOR_LEVEL = EXE_CONVERT + ' {fileName} -level 5%,100% {fileName} '
CMD_PACKIMG_RGB_PVR = EXE_PVRTEXTOOL + ' -f PVRTC1_4_RGB -q pvrtcbest -l -i {fileName} -o {noneExtName}.pvr'
CMD_PACKIMG_RGBA_PVR = EXE_PVRTEXTOOL + ' -f PVRTC1_4_RGBA -q pvrtcbest -l -i {fileName} -o {noneExtName}.pvr'
CMD_PACKIMG_RGB_ETC = EXE_PVRTEXTOOL + ' -f ETC1 -q etcslow -i {fileName} -o {noneExtName}.pvr'
CMD_PACKIMG_A8 = EXE_CONVERT + ' {fileName} -alpha extract -quality 80 {noneExtName}_alpha.jpg'
CMD_PACKIMG_RGBA_PVR = EXE_PVRTEXTOOL + ' -f PVRTC1_4 -q pvrtcbest -l -i {fileName} -o {noneExtName}.pvr'
CMD_PNG_COMP_ALL = EXE_PNGQUANT + ' -f --ext .png --quality 50-60 {fileName}'
CMD_GZIP_PVR = EXE_7Z + ' a -tgzip {fileName}.gz {fileName}'
CMD_LUA_TO_BYTE = EXE_LUAJIT + ' -b {fileName} {fileName}'
CMD_LUAC_SCRIPTLUA = EXE_LUAC + ' -o {fileName} {fileName}'
CMD_DATA_ENCRYPT = EXE_PHPPACK + ' -i {folderName} -o {folderName} -ek ' + ENCRYPT_KEY + ' -es sign'
CMD_SQLITE_ENCRYPT = EXE_DBENCRYPT + os.sep + 'PngEnCodeTool.exe ' + ENCRYPT_KEY 
CMD_REMOVE_BOM = EXE_REMOVEBOM + ' {fileName}'
# 需要重启的文件列表
FILE_RESTART_INCLUDE = [r'typedefine/language.lua',
                        r'scriptlua/module/mgr/frameutils.lua',
                        r'scriptlua/module/mgr/lualogmgr.lua',
                        r'scriptlua/net/protocol/serverprotocol.lua',
                        r'scriptlua/net/protocol/clientprotocol.lua',
                        r'scriptlua/net/protocol/protocolmgr.lua',
                        r'scriptlua/removefiles.lua',
                        r'scriptlua/netconfig.lua',
                        r'scriptlua/userconfig.lua',
                        r'scriptlua/main.lua']

# 打大图的文件夹
FILE_FOLDER_PACK_INCLUDE = [r'data/']
FILE_FOLDER_PACK_EXCLUDE = [r'data/uibg/',
                            r'data/mapres/',
                            r'data/icon/',
                            r'data/battlebg/',
                            r'data/head/',
                            r'data/num/',
                            r'data/loadres/',
                            r'data/tips/',
                            r'data/tool/',
                            r'data/tiled/']

FILE_DATA_ENCRYPT_INCLUDE = [r'animation/effect',
                             r'animation/hero',
                             r'animation/mon',
                             r'animation/role',
                             r'data',
                             r'scriptlua']

FILE_PACKIMG_SQUARE_REGEX = r'.*data[\\/]((mapres)|(battlebg))[\\/](?!((mapblock)|(mapimage))).*\.((jpg)|(png)|(jpeg))$'
FILE_PACKIMG_RGB_REGEX = r'.*data[\\/]((mapres)|(innercity)|(battlebg))[\\/](?!((mapblock)|(mapimage))).*\.((jpg)|(png)|(jpeg))$'
FILE_PACKIMG_EFFECT_REGEX = r'.*animation[\\/]effect[\\/](?!((ef7_self244_)|(ef7_self246_)|(ef7_self248_)|(ef7_self247_)|(ef7_self245_)|(ef7_self56_)|(ef8_self184_)|(ef7_self132_)|(ef8_self195_)|(ef8_self282_))).*\.((jpg)|(png)|(jpeg))$'
FILE_PACKIMG_MODEL_REGEX = r'.*animation[\\/]((hero)|(mon)|(role))[\\/].*\.((jpg)|(png)|(jpeg))$'
FILE_PNG_COMP_ALL_REGEX = r'.*\.png$'
FILE_ALPHA_JPG_REGEX = r'.*_alpha\.jpg$'
FILE_GZIP_PVR_REGEX = r'.*\.pvr$'
FILE_LUA_TO_BYTE_REGEX = r'.*[\\/]res[\\/](?!(scriptlua[\\/]cocos[\\/])).*\.lua$'
FILE_LUAC_SCRIPTLUA_REGEX = r'.*[\\/]res[\\/](?!(scriptlua[\\/]((cocos)|(test))[\\/])).*\.lua$'
FILE_REMOVE_BOM_REGEX = r'.*\.((lua)|(plist)|(f)|(v))$'
