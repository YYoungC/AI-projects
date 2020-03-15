import ISE
import time

start = time.time()
n1 = 'network.txt'
n2 = 'NetHEPT.txt'
graph = ISE.create_graph(n2)
Aset = []

with open('test.txt') as s:
    for line in s:
        seed_seq = line
        seed_seq = int(seed_seq) - 1
        # status[seed_seq] = True
        Aset.append(seed_seq)
seeds = [56, 58, 53, 62, 28]
seeds1 = [6025, 268, 38, 1242, 1435]
for i in range(0, len(seeds)):
    seeds[i] -= 1
# print(seeds)
# graph, seeds, model, time_limit, N
ISE.init(graph, 'LT')
ise = ISE.run(Aset, 10000)
print(ise)
print("time:{}".format(time.time() - start))
# a = [1, 2, 3]
# b = a[0]
# b += 9
# # b = a.append(5)
# print(int(5/2))

# print(a)

# while len(Aset) != 0:
#     newAset = set()
#     for a in Aset:
#         for n, w in graph.nodes[a].items():
#             if n not in total_Aset:
#                 if n not in threshold:
#                     threshold[n] = random.random()
#                     w_total[n] = 0
#                 w_total[n] += w
#                 if w_total[n] >= threshold[n] or threshold[n] == 0.0:
#                     newAset.add(n)
#                     total_Aset.add(n)
#                     for m, v in graph.nodes[n].items():
#                         if m not in total_Aset:
#                             if m not in threshold:
#                                 threshold[m] = random.random()
#                                 w_total[m] = 0
#                             w_total[m] += v