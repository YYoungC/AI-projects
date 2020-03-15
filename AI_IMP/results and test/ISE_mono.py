import argparse
import random


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


if __name__ == '__main__':
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
    nodes, status, Aset = create_graph()

    N = 10000
    sum = 0

    if model == 'IC':
        for i in range(0, N):
            sum += IC(status.copy(), Aset.copy())
        print(sum/N)
    elif model == 'LT':
        for b in range(0, N):
            threshold = []
            Aset_copy = Aset.copy()
            status_copy = status.copy()
            for n in range(0, len(status)):
                threshold.append([random.random(), 0])
                if threshold[n][0] == 0.0 and not status_copy[n]:
                    status_copy[n] = True
                    Aset_copy.append(n)
            for a in Aset_copy:
                for n in nodes[a]:
                    if not status_copy[n[0]]:
                        threshold[n[0]][1] += n[1]
            sum += LT(status_copy, Aset_copy, threshold)
        print(sum/N)



