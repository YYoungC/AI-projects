FUNCTION celf():
    pq <- []
    # contains sequence, influence spread AND a mark of nodes
    IF graph.node_num < 200:
        # IF graph is small, skip the heuristic algorithm
          ENDIF
        for i in tempo:
            IF len(graph.nodes[i]) = 0:
                pq.append([i, 0, -1])
            ELSE:
                pq.append([i, cal_ise([i]), -1])
            ENDIF
        ENDFOR
    ELSE:
        create_worker(worker_num, int(len(tempo) / worker_num))
        Task <- [i for i in range(worker_num)]
                  ENDFOR
        for i, t in enumerate(Task):
            worker[i % worker_num].inQ.put(t)
        ENDFOR
        for w in worker:
            pq += w.outQ.get()
        ENDFOR
        finish_worker()
        # use multi-processor to calculate influence spread of each node
    ENDIF
    pq <- sorted(pq, key=lambda x: x[1], reverse=True)
    # sort the nodes according to the influence spread
    result <- [pq[0][0]]
    # contains selected nodes
    max <- pq[0][1]
    # influence spread of selected nodes
    del pq[0]
    cycle <- 2
    # the number of loops
    while len(result) < size:
        pq <- sorted(pq, key=lambda x: x[1], reverse=True)
        IF cycle - pq[0][2] <= 1 + k * int(cycle / co):
            result.append(pq[0][0])
            max += pq[0][1]
            del pq[0]
            # pick the node with biggest influence spread. If it is picked in last loop, add it into results
        ELSE:
            pq[0][1] <- cal_ise(result + [pq[0][0]]) - max
            pq[0][2] <- cycle
            # else recalculate influence spread AND update its mark
        ENDIF
        cycle += 1
    ENDWHILE
    RETURN result
