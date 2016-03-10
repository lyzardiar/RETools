import os, sys

projectdir = os.path.dirname(os.path.realpath(__file__))
packBin = os.path.join(projectdir, "bin/pack_files.bat")

if len(sys.argv) >= 3:
    cmd = "%s -i %s -o %s -ek XG -es DDTX" % (packBin, sys.argv[1], sys.argv[2])

    os.system(cmd) 
    
else:
    inputpath = r"E:\Workspace\Mobilephone_DDT\trunk\Client\Develop\Resource\MEFramework2"
    outputpath = r"E:\Workspace\Mobilephone_DDT\trunk\Client\Develop\Resource\MEFramework"
    inputpath = r"E:\Workspace\Mobilephone_DDT\trunk\Client\Develop\Resource_test\xx"
    outputpath = r"E:\Workspace\Mobilephone_DDT\trunk\Client\Develop\Resource_test\xx"
    cmd = "%s -i %s -o %s -ek XG -es DDTX" % (packBin, inputpath, outputpath)

    os.system(cmd) 
    
    
    #print "Invalid input"