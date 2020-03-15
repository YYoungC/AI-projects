import argparse
import random
import time
import heapq

V = 0
E = 0
threshold_list = []
graph_list = []
dest_graph_list = []
active_list = []


def IC(activity_set):
    new_active_list = active_list.copy()
    count = len(activity_set)
    while activity_set:
        new_activity_set = []
        for seed in activity_set:
            # traverse neighbors
            for neighbor in graph_list[seed]:
                # not activated
                if new_active_list[neighbor[0]] == False:
                    lucky = random.random()
                    # try to activate based on probability
                    if neighbor[1] >= lucky:
                        new_active_list[neighbor[0]] = True
                        new_activity_set.append(neighbor[0])
        count += len(new_activity_set)
        activity_set = new_activity_set
    return count


def LT(activity_set):
    new_active_list = active_list.copy()
    # initialize threshold
    for i in range(1, len(threshold_list)):
        threshold_list[i] = random.random()
        # if threshold_list[i] == 0:
        #     activity_set.append(i)
        #     new_active_list[i] = True
    count = len(activity_set)
    while activity_set:
        new_activity_set = []
        for seed in activity_set:
            # traverse neighbors
            for neighbor in graph_list[seed]:
                # not activated
                if new_active_list[neighbor[0]] == False:
                    w_total = 0
                    # traverse neighbors pointing to it
                    for neighbor_neighbor in dest_graph_list[neighbor[0]]:
                        # activated
                        if new_active_list[neighbor_neighbor[0]] == True:
                            w_total += neighbor_neighbor[1]
                    if w_total >= threshold_list[neighbor[0]]:
                        new_active_list[neighbor[0]] = True
                        new_activity_set.append((neighbor[0]))
        count += len(new_activity_set)
        activity_set = new_activity_set
    return count


def model_iterate(m, activity_set):
    if m == "IC":
        result = 0
        for i in range(0, 50):
            result += IC(activity_set)
        return result / 50
    else:
        result = 0
        for i in range(0, 50):
            result += LT(activity_set)
        return result / 50


if __name__ == "__main__":
    # read parameters from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='network.txt')
    parser.add_argument('-k', '--seed_size', type=int, default='5')
    parser.add_argument('-m', '--model', type=str, default='IC')
    parser.add_argument('-t', '--time_limit', type=int, default=60)
    args = parser.parse_args()
    file_name = args.file_name
    seed_size = args.seed_size
    model = args.model
    time_limit = args.time_limit

    time1 = time.time()

    # read and store graph
    f = open(file_name, 'r')
    data1 = f.read().splitlines()
    f.close()
    temp = data1[0].split(" ")
    V, E = int(temp[0]), int(temp[1])
    for i in range(0, V+1):
        threshold_list.append(0)
        graph_list.append([])
        dest_graph_list.append([])
        active_list.append(False)
    for i in range(1, len(data1)):
        temp = data1[i].split(" ")
        src, dest, weight = int(temp[0]), int(temp[1]), float(temp[2])
        graph_list[src].append((dest, weight))
        dest_graph_list[dest].append((src, weight))

    # CELF
    gains = []
    for node in range(1, V+1):
        active_list[node] = True
        spread = model_iterate(model, [node])
        heapq.heappush(gains, (-spread, node))
        active_list[node] = False

    spread, node = heapq.heappop(gains)
    solution = [node]
    spread = -spread
    spreads = [spread]
    active_list[node] = True

    time2 = time.time()
    time_limit -= (time2 - time1)

    for _ in range(seed_size-1):
        matched = False

        while not matched:
            # calculate marginal gain
            _, current_node = heapq.heappop(gains)
            active_list[current_node] = True
            spread_gain = model_iterate(model, solution + [current_node]) - spread
            heapq.heappush(gains, (-spread_gain, current_node))
            active_list[current_node] = False
            matched = gains[0][1] == current_node

        spread_gain, node = heapq.heappop(gains)
        spread -= spread_gain
        solution.append(node)
        active_list[node] = True
        spreads.append(spread)

    for i in range(seed_size):
        print(solution[i])
