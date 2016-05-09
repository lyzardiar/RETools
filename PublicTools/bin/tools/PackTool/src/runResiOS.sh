#!/bin/sh

CURPATH=`pwd`
echo "CURPATH:" $CURPATH

PackPath=$CURPATH/PackResiOS.py

#PackPath=/Volumes/F/Workspace/Tools/RETools/trunk/PublicTools/bin/tools/PackTool/src/PackResiOS.py

echo "PackPath:" $PackPath

#python3 /Volumes/F/Workspace/Tools/RETools/trunk/PublicTools/bin/tools/PackTool/src/PackResiOS.py $*

python3 $PackPath $*