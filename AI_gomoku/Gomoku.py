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

        def calPoint(x, y, color):
            scores1 = [35, 800, 15000, 800000]
            scores2 = [15, 300, 3000, 300000]
            if color == 1:
                scores1, scores2 = scores2, scores1

            def cal(*args):
                b = w = s = 0
                for i in range(0, 5):
                    if args[i] == -1:
                        b += 1
                    elif args[i] == 0:
                        s += 1
                    elif args[i] == 1:
                        w += 1
                if s == 5:
                    return 2
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

            def calH0(y, x):
                if x < 0 or x + 4 > 14:
                    return 0
                else:
                    return cal(chessboard[y][x], chessboard[y][x + 1], chessboard[y][x + 2], chessboard[y][x + 3],
                                    chessboard[y][x + 4])

            def calV0(y, x):
                if y < 0 or y + 4 > 14:
                    return 0
                else:
                    return cal(chessboard[y][x], chessboard[y + 1][x], chessboard[y + 2][x], chessboard[y + 3][x],
                                    chessboard[y + 4][x])

            def calR0(y, x):
                if x < 0 or x + 4 > 14 or y - 4 < 0 or y > 14:
                    return 0
                else:
                    return cal(chessboard[y][x], chessboard[y - 1][x + 1], chessboard[y - 2][x + 2],
                                    chessboard[y - 3][x + 3],
                                    chessboard[y - 4][x + 4])

            def calL0(y, x):
                if x < 0 or x + 4 > 14 or y < 0 or y + 4 > 14:
                    return 0
                else:
                    return cal(chessboard[y][x], chessboard[y + 1][x + 1], chessboard[y + 2][x + 2],
                                     chessboard[y + 3][x + 3],
                                     chessboard[y + 4][x + 4])

            def calH(y, x):
                return calH0(y, x-4) + calH0(y, x-3) + calH0(y, x-2) + calH0(y, x-1) + calH0(y, x)

            def calV(y, x):
                return calV0(y-4, x) + calV0(y-3, x) + calV0(y-2, x) + calV0(y-1, x) + calV0(y, x)

            def calR(y, x):
                return calR0(y+4, x-4) + calR0(y+3, x-3) + calR0(y+2, x-2) + calR0(y+1, x-1) + calR0(y, x)

            def calL(y, x):
                return calL0(y-4, x-4) + calL0(y-3, x-3) + calL0(y-2, x-2) + calL0(y-1, x-1) + calL0(y, x)

            return calH(y, x) + calV(y, x) + calR(y, x) + calL(y, x)

        def getScore(color):
            matrix = np.zeros((15, 15), dtype=np.int)
            for y in range(up1, bot1):
                for x in range(left1, right1):
                    if chessboard[y, x] == 0:
                        matrix[y, x] = calPoint(x, y, color)
            return np.max(matrix)

        points = np.zeros((15, 15), dtype=np.float)
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
                    points[y, x] = float("-inf")
        if bot == -1:
            bot = right = 8
            up = left = 7
        else:
            if up-1 >= 0:
                up -= 1
            if left - 1 >= 0:
                left -= 1
            if bot + 2 > 14:
                bot = 15
            else:
                bot += 2
            if right + 2 > 14:
                right = 15
            else:
                right += 2
        x1 = y1 = 0
        for x in range(left, right):
            for y in range(up, bot):
                if chessboard[y, x] == 0:
                    if x == left and x - 1 >= 0:
                        left1 = left-1
                    else:
                        left1 = left
                    if x == right and x + 1 <= 15:
                        right1 = right + 1
                    else:
                        right1 = right
                    if y == up and y - 1 >= 0:
                        up1 = up-1
                    else:
                        up1 = up
                    if y == bot and y + 1 <= 15:
                        bot1 = bot + 1
                    else:
                        bot1 = bot
                    a = calPoint(x, y, self.color)
                    chessboard[y, x] = self.color
                    b = getScore(-self.color)
                    points[y, x] = a - 0.15 * b
                    chessboard[y, x] = 0
        m = float("-inf")
        # print("cal points")

        for x in range(0, 15):
            for y in range(0, 15):
                if points[y][x] >= m:
                    if points[y][x] > m:
                        m = points[y][x]
                        x1 = x
                        y1 = y
                    elif math.pow((x - 7), 2) + math.pow((y - 7), 2) < math.pow((x1 - 7), 2) + math.pow((y1 - 7), 2):
                        x1 = x
                        y1 = y
        # print(y1, x1)
        # print(points[3, 2])
        # print(points[1, 9])
        # print(-self.color)
        new_pos = [y1, x1]
        # print(new_pos)

        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, return error.
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        # Add your decision into candidate_list, Records the chess board
        self.candidate_list.append(new_pos)
