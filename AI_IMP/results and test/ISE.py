# -*- coding: utf-8 -*-
# written by mark zeng 2018-11-14
# modified by Yao Zhao 2019-10-30

import multiprocessing as mp
import signal
import sys
import argparse
# import os
import random
# import numpy as np


class Worker(mp.Process):
    def __init__ (self, inQ, outQ):
        super(Worker, self).__init__(target=self.start)
        self.inQ = inQ
        self.outQ = outQ
        # np.random.seed(random_seed)  #  如果子进程的任务是有随机性的，一定要给每个子进程不同的随机数种子，否则就在重复相同的结果了
    
    def run (self):
        while True:
            task = self.inQ.get()  # 取出任务， 如果队列为空， 这一步会阻塞直到队列有元素
            x, y = task     # 解析任务
            # sum, product = sum_and_product(x, y)   # 执行任务
            self.outQ.put(sample(x, y))  # 返回结果


def create_worker (num):
    '''
    创建子进程备用
    :param num: 多线程数量
    '''
    for i in range(num):
        worker.append(Worker(mp.Queue(), mp.Queue()))
        worker[i].start()


def finish_worker ():
    '''
    关闭所有子线程
    '''
    for w in worker:
        w.terminate()


# def sum_and_product(x, y):
#     '''
#     计算两个数的和与积
#     '''
#     return x + y, x * y


def create_graph():
    with open(file_name) as file:
        node_num, line_num = file.readline().split(" ")
        node_num = int(node_num)
        line_num = int(line_num)
        nodes = []
        status = []

        for i in range(0, node_num):
            nodes.append([])
            status.append(False)

        for i in range(0, line_num):
            node_seq, neighbor_seq, weight = file.readline().split(" ")
            node_seq = int(node_seq) - 1
            neighbor_seq = int(neighbor_seq) - 1
            weight = float(weight)
            nodes[node_seq].append((neighbor_seq, weight))

    Aset = []

    with open(seed) as s:
        for line in s:
            seed_seq = line
            seed_seq = int(seed_seq) - 1
            status[seed_seq] = True
            Aset.append(seed_seq)
    return nodes, status, Aset


def IC(status, Aset):
    count = len(Aset)
    while len(Aset) != 0:
        newAset = []
        for a in Aset:
            for n in nodes[a]:
                if not status[n[0]] and random.random() < n[1]:
                    status[n[0]] = True
                    newAset.append(n[0])
        count += len(newAset)
        Aset = newAset
    del Aset
    del status
    return count


def LT(status, Aset, threshold):
    count = len(Aset)
    while len(Aset) != 0:
        newAset = []
        for a in Aset:
            for n in nodes[a]:
                if not status[n[0]] and threshold[n[0]][1] >= threshold[n[0]][0]:
                    status[n[0]] = True
                    newAset.append(n[0])
                    for j in nodes[n[0]]:
                        threshold[j[0]][1] += j[1]
        count += len(newAset)
        Aset = newAset
    del Aset
    del status
    del threshold
    return count


def sample(status, Aset):
    if model == 'IC':
        return IC(status.copy(), Aset.copy())
    elif model == 'LT':
        threshold = []
        # Aset_copy = Aset.copy()
        # status_copy = status.copy()
        for n in range(0, len(status)):
            threshold.append([random.random(), 0])
            if threshold[n][0] == 0.0 and not status[n]:
                status[n] = True
                Aset.append(n)
        for a in Aset:
            for n in nodes[a]:
                if not status[n[0]]:
                    threshold[n[0]][1] += n[1]
        return LT(status, Aset, threshold)


def timeout(signum, frame):
    # this function raise a TimeoutError
    raise TimeoutError


if __name__ == '__main__':
    '''
    从命令行读参数示例
    '''
    # print("从命令行读参数示例")
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='network.txt')
    parser.add_argument('-s', '--seed', type=str, default='seeds.txt')
    parser.add_argument('-m', '--model', type=str, default='IC')
    parser.add_argument('-t', '--time_limit', type=int, default=60)

    args = parser.parse_args()
    file_name = args.file_name
    seed = args.seed
    model = args.model
    time_limit = args.time_limit

    signal.signal(signal.SIGALRM, timeout)
    signal.setitimer(signal.ITIMER_REAL, time_limit-10)
    try:
        nodes, status, Aset = create_graph()

        N = 10000
        sum = 0

        '''
        多进程示例
        '''
        # print("多进程示例")
        # np.random.seed(0)
        check = False
        worker = []
        worker_num = 8
        create_worker(worker_num)
        Task = [(status, Aset) for i in range(N)]  # 生成16个随机任务， 每个任务是2个整数， 需要计算两数之和与积
        # print('Task', Task)
        for i, t in enumerate(Task):
            worker[i % worker_num].inQ.put(t)  # 根据编号取模， 将任务平均分配到子进程上
        result = []
        for i, t in enumerate(Task):
            result.append(worker[i % worker_num].outQ.get())  # 用同样的规则取回结果， 如果任务尚未完成，此处会阻塞等待子进程完成任务
        # print('result', result)
        finish_worker()
        signal.setitimer(signal.ITIMER_REAL, 0)
    except TimeoutError:
        finish_worker()

    for i in range(len(result)):
        sum += result[i]
    print(sum/len(result))
    '''
    程序结束后强制退出，跳过垃圾回收时间, 如果没有这个操作会额外需要几秒程序才能完全退出
    '''
    sys.stdout.flush()
