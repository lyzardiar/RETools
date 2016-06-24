
import multiprocessing
import concurrent.futures


errorQueue = multiprocessing.Queue()  
taskQueue = multiprocessing.Queue()
# queueProcess(taskQueue, errorQueue, 1)# os.cpu_count())


def queueProcess2(taskQueue, errorQueue, tcnt=4):
    # print('threads : ' + str(tcnt))

    with concurrent.futures.ProcessPoolExecutor() as pool:
        for i in range(1, tcnt + 1) :
            pool.submit(runProcess2, i, taskQueue, errorQueue)

    # pools = []
    # for i in range(1, tcnt + 1) :
    #     pools.append(multiprocessing.Process(target=runProcess2, args=(i, taskQueue, errorQueue, )))

    # for pool in pools:
    #     pool.start()
    # for pool in pools:
    #     pool.join()

    return errorQueue

def runProcess2(tid, queue, errorQueue):
    print(tid)
    return

queueProcess2(taskQueue, errorQueue, 1)# os.cpu_count())