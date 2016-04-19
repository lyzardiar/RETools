import os, sys

projectdir = os.path.dirname(os.path.realpath(__file__))
packBin = os.path.join(projectdir, "bin/pack_files.bat")

if len(sys.argv) >= 3:
    cmd = "%s -i %s -o %s -ek XG -es DDTX" % (packBin, sys.argv[1], sys.argv[2])

    os.system(cmd) 
    
else:
    inputpath = r"E:\Workspace\Mobilephone_DDT\trunk\Client\Develop\Resource\MEFramework2"
    outputpath = r"E:\Workspace\Mobilephone_DDT\trunk\Client\Develop\Resource\MEFramework"
    
    inputpath = r"E:\Workspace\Mobilephone_DDT\trunk\Client\Engine\proj.android\assets\MEFramework"
    outputpath = r"E:\Workspace\Mobilephone_DDT\trunk\Client\Engine\proj.android\assets\MEFramework"
    
    inputpath = r"E:\Workspace\Mobilephone_DDT\trunk\Client\Engine\proj.android\assets\LuaScript"
    outputpath = r"E:\Workspace\Mobilephone_DDT\trunk\Client\Engine\proj.android\assets\LuaScript"
    
    inputpath = r"C:\WorkSpace\Public\TX\Android\Versions\Ver0.1.0.35878_origin_O\update\10007_pather_encode_2\config\ai"
    outputpath = r"C:\WorkSpace\Public\TX\Android\Versions\Ver0.1.0.35878_origin_O\update\10007_pather_encode_2\config\ai"
    
    
    
    cmd = "%s -i %s -o %s -ek XG -es DDTX" % (packBin, inputpath, outputpath)

    os.system(cmd) 
    
    
    #print "Invalid input"