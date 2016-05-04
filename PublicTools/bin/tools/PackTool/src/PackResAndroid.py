# -*- coding: utf-8 -*-

'''
Created on 2016年4月8日

@author: yun.bo
'''

import sys
import PackRes

if len(sys.argv) > 1:
    print("start compile...")
    pack = PackRes.PackRes(sys.argv[1], 'android')
    pack.start()
else:
    print("use PackRes {dir} to compile...")