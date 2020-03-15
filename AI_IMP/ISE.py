import multiprocessing as mp
import random


graph = None
seeds = []
model = 'IC'


class Worker(mp.Process):
    def __init__(self, outQ, count):
        super(Worker, self).__init__(target=self.start)
        self.outQ = outQ
        self.count = count
        self.sum = 0

    def run(self):
        while self.count > 0:
            res = ise()
            self.sum += res
            self.count -= 1
            if self.count == 0:
                self.outQ.put(self.sum)


def create_worker(num, task_num, worker):
    for i in range(num):
        worker.append(Worker(mp.Queue(), task_num))
        worker[i].start()


def finish_worker(worker):
    for w in worker:
        w.terminate()


class Graph:
    def __init__(self, node_num):
        self.node_num = node_num
        self.nodes = dict()
        for i in range(self.node_num):
            self.add_node(i)

    def add_node(self, node):
        self.nodes[node] = dict()

    def add_edge(self, s, e, w):
        self.nodes[s][e] = w


def create_graph(file_name):
    # read the given file and create a graph containing nodes in the file
    with open(file_name) as file:
        node_num, line_num = file.readline().split(" ")
        node_num = int(node_num)
        line_num = int(line_num)
        graph = Graph(node_num)
        # read the first line to get the number of nodes and edges
        for i in range(0, line_num):
            node_seq, neighbor_seq, weight = file.readline().split(" ")
            node_seq = int(node_seq) - 1
            neighbor_seq = int(neighbor_seq) - 1
            weight = float(weight)
            graph.add_edge(node_seq, neighbor_seq, weight)
            # read the next lines and add edges into the graph
    return graph


def IC():
    global graph, seeds
    Aset = set(seeds)
    # set of nodes activated in last loop
    total_Aset = set(seeds)
    # set of all the nodes activated
    while len(Aset) != 0:
        newAset = set()
        # set of nodes activated in this loop
        for a in Aset:
            for n, w in graph.nodes[a].items():
                if n not in total_Aset and random.random() < w:
                    # if not activated and lucky, it is activated
                    newAset.add(n)
                    total_Aset.add(n)
        Aset = newAset
    return len(total_Aset)


def LT():
    global graph, seeds
    Aset = set(seeds)
    # set of nodes activated in last loop
    total_Aset = set(seeds)
    # set of all the nodes activated
    threshold = {}
    # a dict of threshold of nodes
    w_total = {}
    # a dict of total weight of nodes
    while len(Aset) != 0:
        newAset = set()
        # set of nodes activated in this loop
        for a in Aset:
            for n, w in graph.nodes[a].items():
                if n not in total_Aset:
                    # if not activated
                    if n not in threshold:
                        # initialize the threshold
                        threshold[n] = random.random()
                        w_total[n] = 0
                    w_total[n] += w
                    if w_total[n] >= threshold[n] or threshold[n] == 0.0:
                        # if total weight greater than threshold, activated
                        newAset.add(n)
                        total_Aset.add(n)
        Aset = newAset
    return len(total_Aset)


def ise():
    global model
    if model == 'IC':
        return IC()
    elif model == 'LT':
        return LT()


def init(g, m):
    global model, graph
    graph = g
    model = m


def run(s, N):
    global seeds
    seeds = s
    worker = []
    worker_num = 8
    create_worker(worker_num, int(N / worker_num), worker)
    result = []
    for w in worker:
        result.append(w.outQ.get())
    finish_worker(worker)
    return sum(result) / N
