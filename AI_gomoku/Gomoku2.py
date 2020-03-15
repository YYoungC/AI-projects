import numpy as np
import random
import math
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)


# don't change the class name
class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []

    # The input is current chessboard.
    def go(self, chessboard):
        # Clear candidate_list
        self.candidate_list.clear()
        # ==================================================================
        # Write your algorithm here
        # Here is the simplest sample:Random decision

        def evaluate(player):
            scores1 = [35, 800, 15000, 800000]
            scores2 = [20, 400, 4000, 300000]
            result = 0

            def cal(*args):
                b = w = s = 0
                for i in range(0, 5):
                    if args[i] == player:
                        b += 1
                    elif args[i] == 0:
                        s += 1
                    else:
                        w += 1
                if s == 5:
                    return 7
                elif b != 0 and w != 0:
                    return 0
                elif b != 0:
                    if b == 1:
                        return scores1[0]
                    elif b == 2:
                        return scores1[1]
                    elif b == 3:
                        return scores1[2]
                    elif b == 4:
                        return scores1[3]
                elif w != 0:
                    if w == 1:
                        return scores2[0]
                    elif w == 2:
                        return scores2[1]
                    elif w == 3:
                        return scores2[2]
                    elif w == 4:
                        return scores2[3]
            # print("in")
            for y in range(0, 15):
                for x in range(0, 11):
                    result += cal(chessboard[y][x], chessboard[y][x + 1], chessboard[y][x + 2],
                                  chessboard[y][x + 3],
                                  chessboard[y][x + 4])
            for x in range(0, 15):
                for y in range(0, 11):
                    result += cal(chessboard[y][x], chessboard[y + 1][x], chessboard[y + 2][x],
                                  chessboard[y + 3][x],
                                  chessboard[y + 4][x])
            for y in range(4, 15):
                for x in range(0, 11):
                    result += cal(chessboard[y][x], chessboard[y - 1][x + 1], chessboard[y - 2][x + 2],
                                  chessboard[y - 3][x + 3],
                                  chessboard[y - 4][x + 4])
            for y in range(0, 11):
                for x in range(0, 11):
                    result += cal(chessboard[y][x], chessboard[y + 1][x + 1], chessboard[y + 2][x + 2],
                                  chessboard[y + 3][x + 3],
                                  chessboard[y + 4][x + 4])
            return result

        points = np.full((15, 15), -np.inf, dtype=np.float)
        # print(points[0, 0])

        def get_matrix():
            up = bot = left = right = -1
            for x in range(0, 15):
                for y in range(0, 15):
                    if chessboard[y, x] != 0:
                        if y > bot or bot == -1:
                            bot = y
                        if y < up or up == -1:
                            up = y
                        if x > right or right == -1:
                            right = x
                        if x < left or left == -1:
                            left = x
            if bot == -1:
                bot = right = 8
                up = left = 7
            else:
                if up - 1 >= 0:
                    up -= 1
                if left - 1 >= 0:
                    left -= 1
                if bot + 2 > 14:
                    bot = 15
                else:
                    bot += 2
                if bot + 2 > 14:
                    bot = 15
                else:
                    bot += 2
            return up, bot, left, right
        # print("init0")
        border = get_matrix()
        # print(border)
        # for x in range(border[2], border[3]):
        #     for y in range(border[0], border[1]):
        #         if chessboard[y, x] == 0:
        #             chessboard[y, x] = self.color
        #             # print("hhhh")
        for x in range(border[2], border[3]):
            for y in range(border[0], border[1]):
                if chessboard[y, x] == 0:
                    # print("hhh")
                    chessboard[y, x] = self.color
                    points[y, x] = evaluate(self.color)
                    chessboard[y, x] = 0
        # print("init")
        y1 = x1 = 0
        m = float("-inf")
        for x in range(border[2], border[3]):
            for y in range(border[0], border[1]):
                if points[y, x] >= m:
                    if points[y, x] > m:
                        m = points[y, x]
                        x1 = x
                        y1 = y
                    elif math.pow((x - 7), 2) + math.pow((y - 7), 2) < math.pow((x1 - 7), 2) + math.pow((y1 - 7), 2):
                        x1 = x
                        y1 = y
        new_pos = [y1, x1]
        # print(points[3, 11])
        # print(points[5, 5])
        # print(new_pos)
        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, return error.
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        # Add your decision into candidate_list, Records the chess board
        self.candidate_list.append(new_pos)
