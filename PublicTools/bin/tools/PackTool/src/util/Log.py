#coding=utf-8  
'''
Created on 2015年12月19日

@author: Administrator
'''
import traceback
import sys
from queue import Queue


infoQueue = Queue()
detailQueue = Queue()

def printInfo(*args):
    print(*args, end='', flush=True)
    # infoQueue.put(str(text))

def printInfoln(*args):
    print(*args, flush=True)
    # infoQueue.put(str(text) + '\n')

def printDetail(*args):
    print(*args, end='', flush=True)
    # detailQueue.put(str(text))
    
def printDetailln(*args):
    print(*args, flush=True)
    # detailQueue.put(str(text) + '\n')

def printError():
    t, v, tb = sys.exc_info()
    print(t, v, flush=True)
    traceback.print_tb(tb)
    printDetailln('线程异常,' + str(sys.exc_info()))
