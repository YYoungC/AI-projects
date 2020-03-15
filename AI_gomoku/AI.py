import numpy as np
import time
import random
COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)


class AI(object):
    def _init_(self, chessboard_size, color, time_out):
        self.chessboard_size = 15
        self.color = -1
        self.time_out = time_out
        self.candidate_list = []


    def go(self, chessboard):

        self.candidate_list.clear()
        # points = [15][15]
        # for i in range(0, 14):
        #     for j in range(0, 14):
        #         points[i][j] = 0
        points = np.zeros((15, 15), dtype=np.int)
        scores1 = [35, 800, 15000, 800000]
        scores2 = [15, 400, 1800, 100000]
        if AI.color == 1:
            scores1, scores2 = scores2, scores1

        def cal(*args):
            b = w = s = 0
            for i in range(0, 4):
                if args[i] == -1:
                    b += 1
                elif args[i] == 0:
                    s += 1
                else:
                    w += 1
            if s == 5:
                return 7
            elif b != 0 & w != 0:
                return 0
            elif b != 0:
                return {
                    1: scores1[0],
                    2: scores1[1],
                    3: scores1[2],
                    4: scores1[3],
                }.get(b)
            elif w != 0:
                return {
                    1: scores2[0],
                    2: scores2[1],
                    3: scores2[2],
                    4: scores2[3],
                }.get(w)

        x = y = 0
        for y in range(0, 15):
            for x in range(0, 11):
                if chessboard[y][x] != 0 | chessboard[y][x + 4] != 0:
                    score = cal(chessboard[y][x], chessboard[y][x + 1], chessboard[y][x + 2], chessboard[y][x + 3], chessboard[y][x + 4])
                    if chessboard[y][x] != 0:
                        points[y][x] += score
                    if chessboard[y][x + 4] != 0:
                        points[y][x + 4] += score
                x += 1
            x = 0
            y += 1
        y = 0
        for x in range(0, 15):
            for y in range(0, 11):
                if chessboard[y][x] != 0 | chessboard[y + 4][x] != 0:
                    score = cal(chessboard[y][x], chessboard[y + 1][x], chessboard[y + 2][x], chessboard[y + 3][x], chessboard[y + 4][x])
                    if chessboard[y][x] != 0:
                        points[y][x] += score
                    if chessboard[y + 4][x] != 0:
                        points[y + 4][x] += score
                y += 1
            x += 1
            y = 0
        x = 0
        for y in range(0, 11):
            for x in range(0, 11):
                if chessboard[y][x] != 0 | chessboard[y + 4][x + 4] != 0:
                    score = cal(chessboard[y][x], chessboard[y + 1][x + 1], chessboard[y + 2][x + 2], chessboard[y + 3][x + 3],
                                chessboard[y + 4][x + 4])
                    if chessboard[y][x] != 0:
                        points[y][x] += score
                    if chessboard[y + 4][x + 4] != 0:
                        points[y + 4][x + 4] += score
                x += 1
            y += 1
            x = 0
        y = 4
        for y in range(4, 15):
            for x in range(0, 11):
                if chessboard[y][x] != 0 | chessboard[y - 4][x + 4] != 0:
                    score = cal(chessboard[y][x], chessboard[y - 1][x + 1], chessboard[y - 2][x + 2], chessboard[y - 3][x + 3],
                                chessboard[y - 4][x + 4])
                    if chessboard[y][x] != 0:
                        points[y][x] += score
                    if chessboard[y - 4][x + 4] != 0:
                        points[y - 4][x + 4] += score
                x += 1
            y += 1
            x = 0

        y = m = x1 = y1 = 0
        for y in range(0, 15):
            for x in range(0, 15):
                if points[y][x] > max:
                    m = points[y][x]
                    x1 = x
                    y1 = y

        new_pos = [x1, y1]
        # assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        # self.candidate_list.append(new_pos)
        print(x1, y1)

    go()
