import multiprocessing as mp
import sys
import ISE
import argparse
# import time
import signal


class Worker(mp.Process):
    def __init__(self, inQ, outQ, task_num):
        super(Worker, self).__init__(target=self.start)
        self.inQ = inQ
        self.outQ = outQ
        self.task_num = task_num

    def run(self):
        while True:
            task = self.inQ.get()
            q = []
            for i in range(self.task_num):
                current = tempo[task*self.task_num + i]
                if len(graph.nodes[current]) != 0:
                    q.append([current, cal_ise([current]), -1])
            self.outQ.put(q)


def create_worker(num, task_num):
    for i in range(num):
        worker.append(Worker(mp.Queue(), mp.Queue(), task_num))
        worker[i].start()


def finish_worker ():
    for w in worker:
        w.terminate()


def cal_ise(seeds):
    # return influence spread of the 'seeds'
    return ISE.run(seeds, N)


def degree_discount(k):
    candidates = []
    # contains sequence of nodes selected
    degree = []
    # out-degree of nodes
    ct = []
    # a debuff. If parent node is selected, importance of child node decrease.
    for i in range(graph.node_num):
        degree.append(len(graph.nodes[i]))
        ct.append(0)
        # initialize lists
    for i in range(k):
        u = degree.index(max(degree))
        degree[u] = -1
        # select node with biggest out-degree
        candidates.append(u)
        for child, w in graph.nodes[u].items():
            # add debuff the children of selected node
            if child not in candidates:
                ct[child] += 1
                degree[child] = degree[child] - 2 * ct[child] - (len(graph.nodes[child]) - ct[child]) * ct[child] * w
    return candidates


def celf():
    pq = []
    # contains sequence, influence spread and a mark of nodes
    if graph.node_num < 200:
        # if graph is small, skip the heuristic algorithm
        for i in tempo:
            if len(graph.nodes[i]) == 0:
                pq.append([i, 0, -1])
            else:
                pq.append([i, cal_ise([i]), -1])
    else:
        create_worker(worker_num, int(len(tempo) / worker_num))
        Task = [i for i in range(worker_num)]
        for i, t in enumerate(Task):
            worker[i % worker_num].inQ.put(t)
        for w in worker:
            pq += w.outQ.get()
        finish_worker()
        # use multi-processor to calculate influence spread of each node
    pq = sorted(pq, key=lambda x: x[1], reverse=True)
    # sort the nodes according to the influence spread
    result = [pq[0][0]]
    # contains selected nodes
    max = pq[0][1]
    # influence spread of selected nodes
    del pq[0]
    cycle = 2
    # the number of loops
    while len(result) < size:
        pq = sorted(pq, key=lambda x: x[1], reverse=True)
        if cycle - pq[0][2] <= 1 + k * int(cycle / co):
            result.append(pq[0][0])
            max += pq[0][1]
            del pq[0]
            # pick the node with biggest influence spread. If it is picked in last loop, add it into results
        else:
            pq[0][1] = cal_ise(result + [pq[0][0]]) - max
            pq[0][2] = cycle
            # else recalculate influence spread and update its mark
        cycle += 1
    return result


def timeout(signum, frame):
    raise TimeoutError


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='network.txt')
    parser.add_argument('-k', '--size', type=str, default=5)
    parser.add_argument('-m', '--model', type=str, default='IC')
    parser.add_argument('-t', '--time_limit', type=int, default=120)

    args = parser.parse_args()
    file_name = args.file_name
    size = int(args.size)
    model = args.model
    time_limit = int(args.time_limit)

    signal.signal(signal.SIGALRM, timeout)
    signal.setitimer(signal.ITIMER_REAL, time_limit-10)

    try:
        worker = []
        worker_num = 8
        graph = ISE.create_graph(file_name)
        ISE.init(graph, model)

        k = 0
        step = 3200
        co = 100
        if graph.node_num < 200:
            if model == 'IC':
                N = 5000
            else:
                N = 1000
        elif size < 30:
            if model == 'IC':
                N = 1000
            else:
                N = 400
                k = 1
        elif model == 'IC':
            step = 1000
            N = 800
            k = 1
            # co = 50
        else:
            step = 400
            N = 400
            k = 1
            co = 50

        if graph.node_num < 100:
            tempo = range(0, graph.node_num)
        else:
            tempo = degree_discount(step)
        result = celf()
        signal.setitimer(signal.ITIMER_REAL, 0)
    except TimeoutError:
        result = degree_discount(size)

    for i in result:
        i += 1
        print(i)
    sys.stdout.flush()
