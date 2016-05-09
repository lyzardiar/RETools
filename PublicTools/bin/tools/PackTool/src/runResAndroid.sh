#!/bin/sh

CURPATH=`pwd`
echo "CURPATH:" $CURPATH
PackPath=$CURPATH/PackResAndroid.py

python3 $PackPath $*