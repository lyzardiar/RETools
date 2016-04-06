'''
Created on 2015年12月19日

@author: Administrator
'''
# print(u'asdf\nasdfasdf');
# 
# a,b,c,d=20,5.5,True,4+3j;
# print(type(a),type(b),type(c),type(d))
# 
# name = 'hello'
# print(len(name))
# print(name[0:2])
# 
# ary = ['a',3,4,'adsfadsf']
# ary.clear()
# print(ary)
# 
# 3*4
# b = 0;
# while b <10:
#     print(b)
#     b=b+1
# from builtins import range
# 
# # age = input("yourage")
# # print("yourage is : ", age)
# def hello(adf):
#     for i in range(0,adf,3):
#         print(i)
# hello(14) 
# import sys
# import main.PackTool
# print('命令行参数如下:')
# for i in sys.argv:
#     print(i)
# 
# print('/n/nThe PYTHONPATH is', sys.path, '/n')
# 
# main.PackTool.hello()
# import pickle
# 
# # fileName = r'E:\runehero\code\tools\workspace_pack\PackTool\src\main\PackTool.py'
# # f = open(fileName, 'r')
# # for line in f.readlines():
# #     print(line, end="")
# 
# config = {'a':r'adf', 'b':r'asdf'}
# f = open('config', 'wb')
# pickle.dump(config, f)
# from concurrent.futures.thread import ThreadPoolExecutor
# from time import sleep
import os
import re
import shutil
from datetime import datetime
from distutils import dir_util


# class Config:
#     name = 'configName'
#     def show(self):
#         print(self.name)
# 
# c = Config()
# print(c.name)
# c.show()
# def taska():
#     print('start')
#     sleep(3)
#     print('stop')
# pool = ThreadPoolExecutor(3)
# 
# def exec1():
#     for i in range(1, 4) :
#         pool.submit(taska)
#     #会等待
#     print('over')
#     
# exec1()
# with ThreadPoolExecutor(3) as pool :
#     for i in range(1, 4) :
#         f = pool.submit(taska, i)
#         print(f)
# #会等待
# print('over')
# for r, d, f in os.walk(r'E:\runehero\code\tools\workspace_pack\PackTool') :
#     print(r, d, f)
# target = r'E:\temptest\root.ini'
# os.makedirs(os.path.dirname(target), exist_ok=True)
# shutil.copyfile(r'E:\runehero\code\tools\workspace_pack\PackTool\packroot\root.ini', target)
# print('start')
# ary = []
# for r, d, fl in os.walk(r'E:\runehero\code\client\trunk\runehero\res') :
#     for f in fl :
#         abs = os.path.join(r, f);
# #         if re.match(FILE_POWER_OF_TWO_MAPRES_INCLUDE[0],abs) :
#         regex = r'.*data[\\/]((mapres)|(innercity)|(battlebg))[\\/](?!((mapblock)|(mapimage))).*\.((jpg)|(png)|(jpeg))$'
#         if re.match(regex, abs) :
#             ary.append(abs)
#             print(abs)
# print(len(ary))

# data = ['123','11','132','1','0','2','231','120','200']
# data.sort(key=lambda x:int(x))
# print(data)
# dt = datetime.now()
# print(dt)
# print(datetime.now().strftime('%Y%m%d%H%M%S'))

# dir_util.copy_tree('f:/cptest/f1','f:/cptest/f2')

# def n(x):
#     v = 1
#     for i in range(x) :
#         v = (i+1) * v
#     return v
# 
# print(n(4))

print(str(b'\xcf\xb5\xcd\xb3\xd5\xd2\xb2\xbb\xb5\xbd\xd6\xb8\xb6\xa8\xb5\xc4\xc7\xfd\xb6\xaf\xc6\xf7\xa1\xa3\r\n',encoding='gbk'))