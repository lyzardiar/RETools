#coding=utf-8  
'''
Created on 2015年12月19日

@author: Administrator
'''
from queue import Queue


infoQueue = Queue()
detailQueue = Queue()

def printInfo(text):
    print(text, end='', flush=True)
    infoQueue.put(str(text))

def printInfoln(text):
    print(text)
    infoQueue.put(str(text) + '\n')
    
def printDetailln(text):
    print(text)
    detailQueue.put(str(text) + '\n')

def printDetail(text):
    print(text, end='', flush=True)
    detailQueue.put(str(text))
