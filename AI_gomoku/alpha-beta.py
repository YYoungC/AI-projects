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
        global scores
        scores = [1000000, 40000, 1100, 5, 1000, 100, 2, 100, 10, 0, 10, 1, 0, 6000]

        # def reset():
        # 未考虑中间间隔

        def score(count, space, block, list):
            if count == 5:
                if space < 0:
                    list[0] += 1
                else:
                    list[13] += 1
            elif count == 4:
                if block == 0:
                    if space < 0:
                        list[1] += 1
                    else:
                        list[4] += 1
                elif block == 1:
                    list[2] += 1
                elif block == 2:
                    list[3] += 1
            elif count == 3:
                if block == 0:
                    list[4] += 1
                elif block == 1:
                    list[5] += 1
                elif block == 2:
                    list[6] += 1
            elif count == 2:
                if block == 0:
                    list[7] += 1
                elif block == 1:
                    list[8] += 1
                elif block == 2:
                    list[9] += 1
            elif count == 1:
                if block == 0:
                    list[10] += 1
                elif block == 1:
                    list[11] += 1
                elif block == 2:
                    list[12] += 1

        def calv(player, y, x, list):
            # reset()
            count = 1
            space = oppospace = -1
            oppocount = block = 0
            for i in range(1, 5):
                if y + i > 14:
                    block = 1
                    break
                elif chessboard[y + i, x] == 0:
                    if y + i + 1 > 14:
                        if space == -1:
                            space = -2
                            break
                        else:
                            break
                    elif chessboard[y + i + 1, x] == player and space == -1:
                        space = count
                        continue
                    elif space == -1:
                        space = -2
                        break
                    else:
                        break
                elif chessboard[y + i, x] == player:
                    count += 1
                    continue
                else:
                    block = 1
                    break
            for i in range(1, 5):
                if y - i < 0:
                    if block == 0:
                        block = 2
                    else:
                        block = 3
                    break
                # if x == 2 and y == 6 and player == 1 and chessboard[1, 2] == -1:
                #     print(chessboard[y - i, x])
                elif chessboard[y - i, x] == 0:
                    # if x == 2 and y == 6 and player == 1 and chessboard[1, 2] == -1:
                    #     print("===0")
                    if y - i - 1 < 0:
                        if oppospace == -1:
                            oppospace = -2
                            break
                        else:
                            break
                    elif chessboard[y - i - 1, x] == player and oppospace == -1:
                        # if x == 2 and y == 6 and player == 1 and chessboard[1, 2] == -1:
                        #     print("set")
                        oppospace = oppocount
                        continue
                    elif oppospace == -1:
                        oppospace = -2
                        break
                    else:
                        break
                elif chessboard[y - i, x] == player:
                    oppocount += 1
                    continue
                else:
                    if block == 0:
                        block = 2
                    else:
                        block = 3
                    break

            if space > 0:
                l = oppocount + space
            else:
                l = oppocount + count
            if oppospace >= 0:
                r = count + oppospace
            else:
                r = count + oppocount
            if space < 0 and oppospace < 0:
                count += oppocount
                if block in range(1, 3):
                    score(count, space, 1, list)
                elif block == 3:
                    score(count, space, 2, list)
                elif block == 0:
                    score(count, space, 0, list)
            elif space < 0:
                if block == 0:
                    score(l, oppospace, block, list)
                elif block == 1:
                    score(l, oppospace, 1, list)
                elif block == 2:
                    score(r, space, 0, list)
                elif block == 3:
                    score(l, oppospace, 2, list)
            elif oppospace < 0:
                if block == 0:
                    score(r, space, block, list)
                elif block == 1:
                    score(l, oppospace, 0, list)
                elif block == 2:
                    score(r, space, 1, list)
                elif block == 3:
                    score(r, space, 2, list)
            else:
                if block == 0:
                    if l >= r:
                        score(l, oppospace, block, list)
                    else:
                        score(r, space, block, list)
                elif block == 1:
                    score(l, oppospace, 0, list)
                elif block == 2:
                    score(r, space, 0, list)
                elif block == 3:
                    score(space + oppospace, -1, 0, list)
            # if x == 2 and y == 6 and player == 1 and chessboard[1, 2] == -1:
            #     print(count, oppocount, space, oppospace, block)

        def calh(player, y, x, list):
            # reset()
            count = 1
            space = oppospace = -1
            oppocount = block = 0
            for i in range(1, 5):
                if x + i > 14:
                    block = 1
                    break
                elif chessboard[y, x + i] == 0:
                    if x + i + 1 > 14:
                        if space == -1:
                            space = -2
                            break
                        else:
                            break
                    elif chessboard[y, x + i + 1] == player and space == -1:
                        space = count
                        continue
                    elif space == -1:
                        space = -2
                        break
                    else:
                        break
                elif chessboard[y, x + i] == player:
                    count += 1
                    continue
                else:
                    block = 1
                    break
            for i in range(1, 5):
                if x - i < 0:
                    if block == 0:
                        block = 2
                    else:
                        block = 3
                    break
                elif chessboard[y, x - i] == 0:
                    if x - i - 1 < 0:
                        if oppospace == -1:
                            oppospace = -2
                            break
                        else:
                            break
                    elif chessboard[y, x - i - 1] == player and oppospace == -1:
                        oppospace = oppocount
                        continue
                    elif oppospace == -1:
                        oppospace = -2
                        break
                    else:
                        break
                elif chessboard[y, x - i] == player:
                    oppocount += 1
                    continue
                else:
                    if block == 0:
                        block = 2
                    else:
                        block = 3
                    break

            if space > 0:
                l = oppocount + space
            else:
                l = oppocount + count
            if oppospace >= 0:
                r = count + oppospace
            else:
                r = count + oppocount
            # if x == 2 and y == 6 and player == 1:
            #     print(count)
            if space < 0 and oppospace < 0:
                count += oppocount
                if block in range(1, 3):
                    score(count, space, 1, list)
                elif block == 3:
                    score(count, space, 2, list)
                elif block == 0:
                    score(count, space, 0, list)
            elif space < 0:
                if block == 0:
                    score(l, oppospace, block, list)
                elif block == 1:
                    score(l, oppospace, 1, list)
                elif block == 2:
                    score(r, space, 0, list)
                elif block == 3:
                    score(l, oppospace, 2, list)
            elif oppospace < 0:
                if block == 0:
                    score(r, space, block, list)
                elif block == 1:
                    score(l, oppospace, 0, list)
                elif block == 2:
                    score(r, space, 1, list)
                elif block == 3:
                    score(r, space, 2, list)
            else:
                if block == 0:
                    if l >= r:
                        score(l, oppospace, block, list)
                    else:
                        score(r, space, block, list)
                elif block == 1:
                    score(l, oppospace, 0, list)
                elif block == 2:
                    score(r, space, 0, list)
                elif block == 3:
                    score(space + oppospace, -1, 0, list)
            # if player == 1 and x == y == 5:
            #     print(l, r)

        def calr(player, y, x, list):
            # reset()
            count = 1
            space = oppospace = -1
            oppocount = block = 0
            for i in range(1, 5):
                if x + i > 14 or y - i < 0:
                    block = 1
                    break
                elif chessboard[y - i, x + i] == 0:
                    if x + i + 1 > 14 or y - i - 1 < 0:
                        if space == -1:
                            space = -2
                            break
                        else:
                            break
                    elif chessboard[y - i - 1, x + i + 1] == player and space == -1:
                        space = count
                        continue
                    elif space == -1:
                        space = -2
                        break
                    else:
                        break
                elif chessboard[y - i, x + i] == player:
                    count += 1
                    continue
                else:
                    block = 1
                    break
            for i in range(1, 5):
                if x - i < 0 or y + i > 14:
                    if block == 0:
                        block = 2
                    else:
                        block = 3
                    break
                elif chessboard[y + i, x - i] == 0:
                    if x - i - 1 < 0 or y + i + 1 > 14:
                        if oppospace == -1:
                            oppospace = -2
                            break
                        else:
                            break
                    elif chessboard[y + i + 1, x - i - 1] == player and oppospace == -1:
                        oppospace = oppocount
                        continue
                    elif oppospace == -1:
                        oppospace = -2
                        break
                    else:
                        break
                elif chessboard[y + i, x - i] == player:
                    oppocount += 1
                    continue
                else:
                    if block == 0:
                        block = 2
                    else:
                        block = 3
                    break

            if space > 0:
                l = oppocount + space
            else:
                l = oppocount + count
            if oppospace >= 0:
                r = count + oppospace
            else:
                r = count + oppocount
            if space < 0 and oppospace < 0:
                count += oppocount
                if block in range(1, 3):
                    score(count, space, 1, list)
                elif block == 3:
                    score(count, space, 2, list)
                elif block == 0:
                    score(count, space, 0, list)
            elif space < 0:
                if block == 0:
                    score(l, oppospace, block, list)
                elif block == 1:
                    score(l, oppospace, 1, list)
                elif block == 2:
                    score(r, space, 0, list)
                elif block == 3:
                    score(l, oppospace, 2, list)
            elif oppospace < 0:
                if block == 0:
                    score(r, space, block, list)
                elif block == 1:
                    score(l, oppospace, 0, list)
                elif block == 2:
                    score(r, space, 1, list)
                elif block == 3:
                    score(r, space, 2, list)
            else:
                if block == 0:
                    if l >= r:
                        score(l, oppospace, block, list)
                    else:
                        score(r, space, block, list)
                elif block == 1:
                    score(l, oppospace, 0, list)
                elif block == 2:
                    score(r, space, 0, list)
                elif block == 3:
                    score(space + oppospace, -1, 0, list)

        def call(player, y, x, list):
            # reset()
            count = 1
            space = oppospace = -1
            oppocount = block = 0
            for i in range(1, 5):
                if x + i > 14 or y + i > 14:
                    block = 1
                    break
                elif chessboard[y + i, x + i] == 0:
                    if y + i + 1 > 14 or x + i + 1 > 14:
                        if space == -1:
                            space = -2
                            break
                        else:
                            break
                    elif chessboard[y + i + 1, x + i + 1] == player and space == -1:
                        space = count
                        continue
                    elif space == -1:
                        space = -2
                        break
                    else:
                        break
                elif chessboard[y + i, x + i] == player:
                    count += 1
                    continue
                else:
                    block = 1
                    break
            for i in range(1, 5):
                if x - i < 0 or y - i < 0:
                    if block == 0:
                        block = 2
                    else:
                        block = 3
                    break
                elif chessboard[y - i, x - i] == 0:
                    if y - i - 1 < 0:
                        if oppospace == -1:
                            oppospace = -2
                            break
                        else:
                            break
                    elif chessboard[y - i - 1, x - i - 1] == player and oppospace == -1:
                        oppospace = oppocount
                        continue
                    elif oppospace == -1:
                        oppospace = -2
                        break
                    else:
                        break
                elif chessboard[y - i, x - i] == player:
                    oppocount += 1
                    continue
                else:
                    if block == 0:
                        block = 2
                    else:
                        block = 3
                    break

            if space > 0:
                l = oppocount + space
            else:
                l = oppocount + count
            if oppospace >= 0:
                r = count + oppospace
            else:
                r = count + oppocount
            if space < 0 and oppospace < 0:
                count += oppocount
                if block in range(1, 3):
                    score(count, space, 1, list)
                elif block == 3:
                    score(count, space, 2, list)
                elif block == 0:
                    score(count, space, 0, list)
            elif space < 0:
                if block == 0:
                    score(l, oppospace, block, list)
                elif block == 1:
                    score(l, oppospace, 1, list)
                elif block == 2:
                    score(r, space, 0, list)
                elif block == 3:
                    score(l, oppospace, 2, list)
            elif oppospace < 0:
                if block == 0:
                    score(r, space, block, list)
                elif block == 1:
                    score(l, oppospace, 0, list)
                elif block == 2:
                    score(r, space, 1, list)
                elif block == 3:
                    score(r, space, 2, list)
            else:
                if block == 0:
                    if l >= r:
                        score(l, oppospace, block, list)
                    else:
                        score(r, space, block, list)
                elif block == 1:
                    score(l, oppospace, 0, list)
                elif block == 2:
                    score(r, space, 0, list)
                elif block == 3:
                    score(space + oppospace, -1, 0, list)

        def evaluate(player, y, x):
            list = [0] * 14
            calh(player, y, x, list)
            calv(player, y, x, list)
            calr(player, y, x, list)
            call(player, y, x, list)
            point = 0
            for i in range(0, 14):
                point += list[i] * scores[i]
            if list[1] != 0 and list[4] != 0:
                point += 10000
            if list[2] != 0 and list[4] != 0:
                point += 30000
            if list[4] >= 2:
                point += 15000
            if list[4] != 0 and list[5] != 0:
                point += 100
            if list[2] != 0 and list[7] != 0:
                point += 40
            if list[4] != 0 and list[7] != 0:
                point += 40
            if list[7] >= 2:
                point += 10
            # if player == 1 and y == 6 and x == 2:
            #     print(list)
            return point

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
                if right + 2 > 14:
                    right = 15
                else:
                    right += 2
            return up, bot, left, right

        def evaluateb():
            border = get_matrix()
            points = np.full((15, 15), -np.inf, dtype=np.float)
            # print(border1)
            for i in range(border[2], border[3]):
                for j in range(border[0], border[1]):
                    if chessboard[j, i] == 0:
                        # chessboard[j, i] = -self.color
                        points[j, i] = evaluate(self.color, j, i)
                        # chessboard[j, i] = 0
            return np.max(points)

        def max_value(alpha, beta, depth):
            if depth >= 2:
                return evaluateb()

            v = float("-inf")
            border = get_matrix()
            # print(border1)
            for i in range(border[2], border[3]):
                for j in range(border[0], border[1]):
                    if chessboard[j, i] == 0:
                        chessboard[j, i] = self.color
                        v = max(v, min_value(alpha, beta, depth+1))
                        chessboard[j, i] = 0
                        if v >= beta:
                            return v
                        alpha = max(alpha, v)
            return v

        def min_value(alpha, beta, depth):
            if depth >= 2:
                return evaluateb()

            v = float("inf")
            border = get_matrix()
            # print(border1)
            for i in range(border[2], border[3]):
                for j in range(border[0], border[1]):
                    if chessboard[j, i] == 0:
                        chessboard[j, i] = -self.color
                        v = min(v, max_value(alpha, beta, depth + 1))
                        chessboard[j, i] = 0
                        if v <= alpha:
                            return v
                        beta = min(beta, v)
            return v

        best_score = float("-inf")
        x1 = y1 = 0
        beta = float("inf")
        border = get_matrix()
        # print(border1)
        for i in range(border[2], border[3]):
            for j in range(border[0], border[1]):
                if chessboard[j, i] == 0:
                    chessboard[j, i] = self.color
                    v = min_value(best_score, beta, 1)
                    chessboard[j, i] = 0
                    if v >= best_score:
                        if v > best_score:
                            best_score = v
                            x1 = i
                            y1 = j
                        elif math.pow((i - 7), 2) + math.pow((j - 7), 2) < math.pow((x1 - 7), 2) + math.pow((y1 - 7),                                                                            2):
                                x1 = i
                                y1 = j
        new_pos = [y1, x1]
        # return best_action

        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, return error.
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        # Add your decision into candidate_list, Records the chess board
        self.candidate_list.append(new_pos)
