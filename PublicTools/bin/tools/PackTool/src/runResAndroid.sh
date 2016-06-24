#!/bin/sh

CURPATH=$(cd `dirname $0`; pwd)
echo "CURPATH:" $CURPATH
PackPath=$CURPATH/PackResAndroid.py

python3 $PackPath $*

pause