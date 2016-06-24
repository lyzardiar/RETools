#coding=utf-8  

from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime

import multiprocessing
import concurrent.futures
import os, queue
from queue import Queue
import subprocess
import sys
import traceback

from util import Log
    
def queueThread(taskQueue, errorQueue, tcnt=4):
    print('threads : ' + str(tcnt))
    with ThreadPoolExecutor(tcnt) as pool :
        for i in range(1, tcnt + 1) :
            pool.submit(runThread, i, taskQueue, errorQueue)

def runThread(tid, taskQueue, errorQueue):
    try:
        while True:
            func, *args = taskQueue.get_nowait()
            if not func(tid, *args) :
                errorQueue.put((func, *args))
    except queue.Empty:
        pass
    except :
        t, v, tb = sys.exc_info()
        print(t, v)
        traceback.print_tb(tb)
        Log.printDetailln('线程异常,' + str(sys.exc_info()))
    finally :
        Log.printDetailln('线程结束, tid : ' + str(tid))

def queueProcess(taskQueue, errorQueue, tcnt=4):
    print('proces : ', tcnt)
    pools = []

    for i in range(1, tcnt+1):
        pool = multiprocessing.Process(target=runProcess, args=(i, taskQueue, errorQueue))
        # pool.daemon = True
        pools.append(pool)

    for pool in pools:
        pool.start()
    for pool in pools:
        pool.join()
  
def runProcess(tid, taskQueue, errorQueue):
    try:
        while taskQueue.qsize() > 0:
            func, *args = taskQueue.get()
            if not func(tid, *args) :
                errorQueue.put((func, *args))
    except :
        t, v, tb = sys.exc_info()
        print(t, v)
        traceback.print_tb(tb)
        Log.printDetailln('线程异常,' + str(sys.exc_info()))
    finally :
        Log.printDetailln('线程结束, tid : ' + str(tid))

def execCmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #Log.printDetailln(cmd)
    return p.wait()
