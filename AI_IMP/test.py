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