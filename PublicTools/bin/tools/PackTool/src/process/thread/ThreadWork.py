
import threading
import queue
import time
try:
    from util import Log
except:
    class Log:
        def printDetailln(*args):
            print(*args, flush="True")

class Task():
    """
        Task
    """

    def __init__(self, target=None, args=(), empty=False):
        self.target = target
        self.param = args
        self.empty = empty

    def isEmpty(self):
        return self.empty

    def apply(self, tid):
        p, *args = self.param
        return self.target(tid, p, *args)

class TaskQueue():
    """
        Thread.TaskQueue
    """

    def __init__(self, name="TaskQueue"):
        self.list = queue.Queue()
        self.name = name
        self.lock = threading.Lock()
        pass

    def get(self):
        return self.list.get()

    def put(self, task):
        self.list.put(task)
    
    def empty(self):
        return self.list.empty()
    
    def size(self):
        return self.list.qsize()

    def print(self):
        if self.empty():
            return
        Log.printDetailln("%s.print:" % (self.name))
        while not self.empty():
            task = self.get()
            ret, *args = task.param
            Log.printDetailln('\t', ret, *args)

class Work():
    """
        ThreadWork
    """
    def __init__(self, count = 1):
        self.tasks  = TaskQueue(name="Tasks")
        self.errs   = TaskQueue(name="Errors")
        self.count  = count
        self.elapse = 0

        if self.tasks is None:
            raise Exception("Error, must init with tasks...")

        self.threads = []
        self.__isInited = False

    # private staticmethod
    def __run(tid, tasks, errs):        
        while not tasks.empty():
            task = tasks.get()

            if task.isEmpty():
                break

            if not task.apply(tid):
                errs.put(task)

    def __initProcess(self):
        if self.__isInited:
            return True

        self.__isInited = True

        for i in range(1, self.count + 1):
            self.tasks.put(Task(empty=True))
            thread = threading.Thread(target=Work.__run, args=(i, self.tasks, self.errs))
            self.threads.append(thread)
        
        return True

    def putTask(self, task):
        self.tasks.put(task)

    def getTask(self):
        return self.tasks.get()

    def getTaskSize(self):
        return self.tasks.size()

    def start(self):
        self.__initProcess()

        for thread in self.threads:
            thread.start()

    def join(self):    
        self.__initProcess()
                
        tstart = time.clock()
                
        for thread in self.threads:
            thread.join()
        
        tend = time.clock()

        self.elapse = tend - tstart


if __name__ == '__main__':

    work = Work(count=4)

    def runable(tid, *args):
        Log.printDetailln('线程:' + str(tid), *args)
        return True

    for i in range(0, 50):
        work.putTask(Task(target=runable, args=('41', '2', '3', )))

    work.start()
    work.join()

    Log.printDetailln("Completed in %.3fs" % (work.elapse))

    work.tasks.print()
    work.errs.print()

    pass
