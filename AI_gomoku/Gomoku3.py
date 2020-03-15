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

        # global count, oppocount, space, oppospace, block, oppoblock, leap, oppoleap
        # global count, oppocount, space, block
        # global five, lfour, four, dfour, lthree, three, dthree, ltwo, two, dtwo, lone, one, done, spacefive\
        #     douthree, doufour, doutwo, lfour_three, four_three, three_two
        global scores
        scores = [10000000, 40000, 800, 50, 1000, 80, 20, 100, 8, 5, 10, 1, 0, 5000, 600, 800]

        # def reset():
        #未考虑中间间隔

        def score(count, space, block, list):
            if count >= 5:
                if space < 0:
                    list[0] += 1
                elif block > 0:
                    list[2] += 1
            elif count == 4:
                if block == 0:
                    if space < 0:
                        list[1] += 1
                    elif space == 3:
                        list[13] += 1
                    elif space == 2:
                        list[4] += 1
                elif block == 1:
                    if space < 0:
                        list[2] += 1
                    else:
                        list[14] += 1
                elif block == 2:
                    list[3] += 1
            elif count == 3:
                if block == 0:
                    if space<0:
                        list[4] += 1
                    else:
                        list[15] += 1
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
            for i in range(1, 6):
                if y+i > 14:
                    block = 1
                    break
                elif chessboard[y+i, x] == 0:
                    if y+i+1 > 14:
                        if space == -1:
                            space = -2
                            break
                        else:
                            break
                    elif chessboard[y+i+1, x] == player and space == -1:
                        space = count
                        continue
                    elif space == -1:
                        space = -2
                        break
                    else:
                        break
                elif chessboard[y+i, x] == player:
                    count += 1
                    continue
                else:
                    block = 1
                    break
            for i in range(1, 6):
                if y-i < 0:
                    if block == 0:
                        block = 2
                    else:
                        block = 3
                    break
                # if x == 2 and y == 1 and player == 1 and chessboard[6, 2] == -1:
                #     print(chessboard[y - i, x])
                elif chessboard[y-i, x] == 0:
                    # if x == 2 and y == 6 and player == 1 and chessboard[1, 2] == -1:
                    #     print("===0")
                    if y-i-1 < 0:
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
                elif chessboard[y-i, x] == player:
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
            # if x == 2 and y == 6 and player == 1 and chessboard[1, 2] == -1:
            #     print(count, oppocount, space, oppospace, block, l, r)
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
                    if l >= 5:
                        if r >= 5:
                            score(5, -1, 0, list)
                        elif r >= 4:
                            score(4, -1, 0, list)
                        elif r >= 3 or l-r >= 3:
                            score(4, 3, 0, list)
                    elif l == 4:
                        if r >= 3 or l-r >= 3:
                            score(4, 3, 0, list)
                        else:
                            score(4, 2, 0, list)
                    else:
                        score(l, oppospace, block, list)
                elif block == 1:
                    if r >= 5:
                        score(5, -1, 1, list)
                    elif l >= 5:
                        if r == 4:
                            score(4, -1, 1, list)
                        else:
                            score(4, 3, 1, list)
                    else:
                        score(l, oppospace, 1, list)    #五个四个同样对待，不管空同样对待
                elif block == 2:
                    if r >= 4:
                        if r >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif l-r >= 2:
                        score(l, oppospace, 1, list)
                    else:
                        score(r, space, 0, list)
                elif block == 3:
                    score(r, -1, 1, list)
            elif oppospace < 0:
                if block == 0:
                    if r >= 5:
                        if l >= 5:
                            score(5, -1, 0, list)
                        elif l >= 4:
                            score(4, -1, 0, list)
                        elif l >= 3 or r-l >= 3:
                            score(4, 3, 0, list)
                    elif r == 4:
                        if l >= 3 or r-l >= 3:
                            score(4, 3, 0, list)
                        else:
                            score(4, 2, 0, list)
                    else:
                        score(r, space, block, list)
                elif block == 1:
                    if l >= 4:
                        if l >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif r-l >= 2:
                        score(r, space, 1, list)
                    else:
                        score(l, space, 0, list)
                elif block == 2:
                    if l >= 5:
                        score(5, -1, 1, list)
                    elif r >= 5:
                        if l == 4:
                            score(4, -1, 1, list)
                        else:
                            score(4, 3, 1, list)
                    else:
                        score(r, space, 1, list)
                elif block == 3:
                    score(r, -1, 1, list)
            else:
                if block == 0:
                    if space+oppospace >= 4:
                        if oppospace+space >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif l >= r:
                        if l >= 4:
                            if l - space - oppospace >= 3 or space + oppospace >= 3:
                               score(4, 3, 0, list)
                            else:
                               score(4, 2, 0, list)
                        else:
                            score(l, oppospace, block, list)
                    else:
                        if r >= 4:
                            if r - space - oppospace >= 3 or space + oppospace >= 3:
                               score(4, 3, 0, list)
                            else:
                               score(4, 2, 0, list)
                        else:
                            score(r, space, block, list)
                elif block == 1:
                    if space+oppospace >= 4:
                        if oppospace+space >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif l >= 4:
                        if l - space - oppospace >= 3 or space + oppospace >= 3:
                            score(4, 3, 0, list)
                        else:
                            score(4, 2, 0, list)
                    elif r - l >= 2:
                        if r - space - oppospace == 4:
                            score(4, -1, 1, list)
                        else:
                            score(r, space, 1, list)
                    else:
                        score(l, oppospace, 0, list)
                elif block == 2:
                    if space + oppospace >= 4:
                        if oppospace + space >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif r >= 4:
                        if r - space - oppospace >= 3 or space + oppospace >= 3:
                            score(4, 3, 0, list)
                        else:
                            score(4, 2, 0, list)
                    elif l - r >= 2:
                        if l - space - oppospace == 4:
                            score(4, -1, 1, list)
                        else:
                            score(l, space, 1, list)
                    else:
                        score(r, oppospace, 0, list)
                elif block == 3:
                    if space+oppospace >= 3:
                        score(oppospace+space, -1, 0, list)
                    elif l >= r:
                        if l-2 >= oppospace+space:
                            score(l, oppospace, 1, list)
                        else:
                            score(space + oppospace, -1, 0, list)
                    else:
                        if r - 2 >= oppospace + space:
                            score(r, space, 1, list)
                        else:
                            score(space+oppospace, -1, 0, list)
            # if x == 2 and y == 6 and player == 1 and chessboard[1, 2] == -1:
            #     print(count, oppocount, space, oppospace, block)

        def calh(player, y, x, list):
            # reset()
            count = 1
            space = oppospace = -1
            oppocount = block = 0
            for i in range(1, 6):
                if x+i > 14:
                    block = 1
                    break
                elif chessboard[y, x+i] == 0:
                    if x+i+1 > 14:
                        if space == -1:
                            space = -2
                            break
                        else:
                            break
                    elif chessboard[y, x+i+1] == player and space == -1:
                        space = count
                        continue
                    elif space == -1:
                        space = -2
                        break
                    else:
                        break
                elif chessboard[y, x+i] == player:
                    count += 1
                    continue
                else:
                    block = 1
                    break
            for i in range(1, 6):
                if x-i < 0:
                    if block == 0:
                        block = 2
                    else:
                        block = 3
                    break
                elif chessboard[y, x-i] == 0:
                    if x-i-1 < 0:
                        if oppospace == -1:
                            oppospace = -2
                            break
                        else:
                            break
                    elif chessboard[y, x-i-1] == player and oppospace == -1:
                        oppospace = oppocount
                        continue
                    elif oppospace == -1:
                        oppospace = -2
                        break
                    else:
                        break
                elif chessboard[y, x-i] == player:
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
                    if l >= 5:
                        if r >= 5:
                            score(5, -1, 0, list)
                        elif r >= 4:
                            score(4, -1, 0, list)
                        elif r >= 3 or l - r >= 3:
                            score(4, 3, 0, list)
                    elif l == 4:
                        if r >= 3 or l - r >= 3:
                            score(4, 3, 0, list)
                        else:
                            score(4, 2, 0, list)
                    else:
                        score(l, oppospace, block, list)
                elif block == 1:
                    if r >= 5:
                        score(5, -1, 1, list)
                    elif l >= 5:
                        if r == 4:
                            score(4, -1, 1, list)
                        else:
                            score(4, 3, 1, list)
                    else:
                        score(l, oppospace, 1, list)  # 五个四个同样对待，不管空同样对待
                elif block == 2:
                    if r >= 4:
                        if r >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif l - r >= 2:
                        score(l, oppospace, 1, list)
                    else:
                        score(r, space, 0, list)
                elif block == 3:
                    score(r, -1, 1, list)
            elif oppospace < 0:
                if block == 0:
                    if r >= 5:
                        if l >= 5:
                            score(5, -1, 0, list)
                        elif l >= 4:
                            score(4, -1, 0, list)
                        elif l >= 3 or r - l >= 3:
                            score(4, 3, 0, list)
                    elif r == 4:
                        if l >= 3 or r - l >= 3:
                            score(4, 3, 0, list)
                        else:
                            score(4, 2, 0, list)
                    else:
                        score(r, space, block, list)
                elif block == 1:
                    if l >= 4:
                        if l >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif r - l >= 2:
                        score(r, space, 1, list)
                    else:
                        score(l, space, 0, list)
                elif block == 2:
                    if l >= 5:
                        score(5, -1, 1, list)
                    elif r >= 5:
                        if l == 4:
                            score(4, -1, 1, list)
                        else:
                            score(4, 3, 1, list)
                    else:
                        score(r, space, 1, list)
                elif block == 3:
                    score(r, -1, 1, list)
            else:
                if block == 0:
                    if space + oppospace >= 4:
                        if oppospace + space >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif l >= r:
                        if l >= 4:
                            if l - space - oppospace >= 3 or space + oppospace >= 3:
                                score(4, 3, 0, list)
                            else:
                                score(4, 2, 0, list)
                        else:
                            score(l, oppospace, block, list)
                    else:
                        if r >= 4:
                            if r - space - oppospace >= 3 or space + oppospace >= 3:
                                score(4, 3, 0, list)
                            else:
                                score(4, 2, 0, list)
                        else:
                            score(r, space, block, list)
                elif block == 1:
                    if space + oppospace >= 4:
                        if oppospace + space >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif l >= 4:
                        if l - space - oppospace >= 3 or space + oppospace >= 3:
                            score(4, 3, 0, list)
                        else:
                            score(4, 2, 0, list)
                    elif r - l >= 2:
                        if r - space - oppospace == 4:
                            score(4, -1, 1, list)
                        else:
                            score(r, space, 1, list)
                    else:
                        score(l, oppospace, 0, list)
                elif block == 2:
                    if space + oppospace >= 4:
                        if oppospace + space >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif r >= 4:
                        if r - space - oppospace >= 3 or space + oppospace >= 3:
                            score(4, 3, 0, list)
                        else:
                            score(4, 2, 0, list)
                    elif l - r >= 2:
                        if l - space - oppospace == 4:
                            score(4, -1, 1, list)
                        else:
                            score(l, space, 1, list)
                    else:
                        score(r, oppospace, 0, list)
                elif block == 3:
                    if space + oppospace >= 3:
                        score(oppospace + space, -1, 0, list)
                    elif l >= r:
                        if l - 2 >= oppospace + space:
                            score(l, oppospace, 1, list)
                        else:
                            score(space + oppospace, -1, 0, list)
                    else:
                        if r - 2 >= oppospace + space:
                            score(r, space, 1, list)
                        else:
                            score(space + oppospace, -1, 0, list)
            # if player == 1 and x == y == 5:
            #     print(l, r)

        def calr(player, y, x, list):
            # reset()
            count = 1
            space = oppospace = -1
            oppocount = block = 0
            for i in range(1, 6):
                if x+i > 14 or y-i < 0:
                    block = 1
                    break
                elif chessboard[y-i, x+i] == 0:
                    if x+i+1 > 14 or y-i-1 < 0:
                        if space == -1:
                            space = -2
                            break
                        else:
                            break
                    elif chessboard[y-i-1, x+i+1] == player and space == -1:
                        space = count
                        continue
                    elif space == -1:
                        space = -2
                        break
                    else:
                        break
                elif chessboard[y-i, x+i] == player:
                    count += 1
                    continue
                else:
                    block = 1
                    break
            for i in range(1, 6):
                if x-i < 0 or y+i > 14:
                    if block == 0:
                        block = 2
                    else:
                        block = 3
                    break
                elif chessboard[y+i, x-i] == 0:
                    if x-i-1 < 0 or y+i+1 > 14:
                        if oppospace == -1:
                            oppospace = -2
                            break
                        else:
                            break
                    elif chessboard[y + i + 1, x-i-1] == player and oppospace == -1:
                        oppospace = oppocount
                        continue
                    elif oppospace == -1:
                        oppospace = -2
                        break
                    else:
                        break
                elif chessboard[y+i, x-i] == player:
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
                    if l >= 5:
                        if r >= 5:
                            score(5, -1, 0, list)
                        elif r >= 4:
                            score(4, -1, 0, list)
                        elif r >= 3 or l - r >= 3:
                            score(4, 3, 0, list)
                    elif l == 4:
                        if r >= 3 or l - r >= 3:
                            score(4, 3, 0, list)
                        else:
                            score(4, 2, 0, list)
                    else:
                        score(l, oppospace, block, list)
                elif block == 1:
                    if r >= 5:
                        score(5, -1, 1, list)
                    elif l >= 5:
                        if r == 4:
                            score(4, -1, 1, list)
                        else:
                            score(4, 3, 1, list)
                    else:
                        score(l, oppospace, 1, list)  # 五个四个同样对待，不管空同样对待
                elif block == 2:
                    if r >= 4:
                        if r >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif l - r >= 2:
                        score(l, oppospace, 1, list)
                    else:
                        score(r, space, 0, list)
                elif block == 3:
                    score(r, -1, 1, list)
            elif oppospace < 0:
                if block == 0:
                    if r >= 5:
                        if l >= 5:
                            score(5, -1, 0, list)
                        elif l >= 4:
                            score(4, -1, 0, list)
                        elif l >= 3 or r - l >= 3:
                            score(4, 3, 0, list)
                    elif r == 4:
                        if l >= 3 or r - l >= 3:
                            score(4, 3, 0, list)
                        else:
                            score(4, 2, 0, list)
                    else:
                        score(r, space, block, list)
                elif block == 1:
                    if l >= 4:
                        if l >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif r - l >= 2:
                        score(r, space, 1, list)
                    else:
                        score(l, space, 0, list)
                elif block == 2:
                    if l >= 5:
                        score(5, -1, 1, list)
                    elif r >= 5:
                        if l == 4:
                            score(4, -1, 1, list)
                        else:
                            score(4, 3, 1, list)
                    else:
                        score(r, space, 1, list)
                elif block == 3:
                    score(r, -1, 1, list)
            else:
                if block == 0:
                    if space + oppospace >= 4:
                        if oppospace + space >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif l >= r:
                        if l >= 4:
                            if l - space - oppospace >= 3 or space + oppospace >= 3:
                                score(4, 3, 0, list)
                            else:
                                score(4, 2, 0, list)
                        else:
                            score(l, oppospace, block, list)
                    else:
                        if r >= 4:
                            if r - space - oppospace >= 3 or space + oppospace >= 3:
                                score(4, 3, 0, list)
                            else:
                                score(4, 2, 0, list)
                        else:
                            score(r, space, block, list)
                elif block == 1:
                    if space + oppospace >= 4:
                        if oppospace + space >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif l >= 4:
                        if l - space - oppospace >= 3 or space + oppospace >= 3:
                            score(4, 3, 0, list)
                        else:
                            score(4, 2, 0, list)
                    elif r - l >= 2:
                        if r - space - oppospace == 4:
                            score(4, -1, 1, list)
                        else:
                            score(r, space, 1, list)
                    else:
                        score(l, oppospace, 0, list)
                elif block == 2:
                    if space + oppospace >= 4:
                        if oppospace + space >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif r >= 4:
                        if r - space - oppospace >= 3 or space + oppospace >= 3:
                            score(4, 3, 0, list)
                        else:
                            score(4, 2, 0, list)
                    elif l - r >= 2:
                        if l - space - oppospace == 4:
                            score(4, -1, 1, list)
                        else:
                            score(l, space, 1, list)
                    else:
                        score(r, oppospace, 0, list)
                elif block == 3:
                    if space + oppospace >= 3:
                        score(oppospace + space, -1, 0, list)
                    elif l >= r:
                        if l - 2 >= oppospace + space:
                            score(l, oppospace, 1, list)
                        else:
                            score(space + oppospace, -1, 0, list)
                    else:
                        if r - 2 >= oppospace + space:
                            score(r, space, 1, list)
                        else:
                            score(space + oppospace, -1, 0, list)

        def call(player, y, x, list):
            # reset()
            count = 1
            space = oppospace = -1
            oppocount = block = 0
            for i in range(1, 6):
                if x+i > 14 or y+i > 14:
                    block = 1
                    break
                elif chessboard[y+i, x+i] == 0:
                    if y+i+1 > 14 or x+i+1 > 14:
                        if space == -1:
                            space = -2
                            break
                        else:
                            break
                    elif chessboard[y+i+1, x+i+1] == player and space == -1:
                        space = count
                        continue
                    elif space == -1:
                        space = -2
                        break
                    else:
                        break
                elif chessboard[y+i, x+i] == player:
                    count += 1
                    continue
                else:
                    block = 1
                    break
            for i in range(1, 6):
                if x-i < 0 or y-i < 0:
                    if block == 0:
                        block = 2
                    else:
                        block = 3
                    break
                elif chessboard[y-i, x-i] == 0:
                    if y-i-1 < 0:
                        if oppospace == -1:
                            oppospace = -2
                            break
                        else:
                            break
                    elif chessboard[y - i - 1, x-i-1] == player and oppospace == -1:
                        oppospace = oppocount
                        continue
                    elif oppospace == -1:
                        oppospace = -2
                        break
                    else:
                        break
                elif chessboard[y-i, x-i] == player:
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
                    if l >= 5:
                        if r >= 5:
                            score(5, -1, 0, list)
                        elif r >= 4:
                            score(4, -1, 0, list)
                        elif r >= 3 or l - r >= 3:
                            score(4, 3, 0, list)
                    elif l == 4:
                        if r >= 3 or l - r >= 3:
                            score(4, 3, 0, list)
                        else:
                            score(4, 2, 0, list)
                    else:
                        score(l, oppospace, block, list)
                elif block == 1:
                    if r >= 5:
                        score(5, -1, 1, list)
                    elif l >= 5:
                        if r == 4:
                            score(4, -1, 1, list)
                        else:
                            score(4, 3, 1, list)
                    else:
                        score(l, oppospace, 1, list)  # 五个四个同样对待，不管空同样对待
                elif block == 2:
                    if r >= 4:
                        if r >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif l - r >= 2:
                        score(l, oppospace, 1, list)
                    else:
                        score(r, space, 0, list)
                elif block == 3:
                    score(r, -1, 1, list)
            elif oppospace < 0:
                if block == 0:
                    if r >= 5:
                        if l >= 5:
                            score(5, -1, 0, list)
                        elif l >= 4:
                            score(4, -1, 0, list)
                        elif l >= 3 or r - l >= 3:
                            score(4, 3, 0, list)
                    elif r == 4:
                        if l >= 3 or r - l >= 3:
                            score(4, 3, 0, list)
                        else:
                            score(4, 2, 0, list)
                    else:
                        score(r, space, block, list)
                elif block == 1:
                    if l >= 4:
                        if l >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif r - l >= 2:
                        score(r, space, 1, list)
                    else:
                        score(l, space, 0, list)
                elif block == 2:
                    if l >= 5:
                        score(5, -1, 1, list)
                    elif r >= 5:
                        if l == 4:
                            score(4, -1, 1, list)
                        else:
                            score(4, 3, 1, list)
                    else:
                        score(r, space, 1, list)
                elif block == 3:
                    score(r, -1, 1, list)
            else:
                if block == 0:
                    if space + oppospace >= 4:
                        if oppospace + space >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif l >= r:
                        if l >= 4:
                            if l - space - oppospace >= 3 or space + oppospace >= 3:
                                score(4, 3, 0, list)
                            else:
                                score(4, 2, 0, list)
                        else:
                            score(l, oppospace, block, list)
                    else:
                        if r >= 4:
                            if r - space - oppospace >= 3 or space + oppospace >= 3:
                                score(4, 3, 0, list)
                            else:
                                score(4, 2, 0, list)
                        else:
                            score(r, space, block, list)
                elif block == 1:
                    if space + oppospace >= 4:
                        if oppospace + space >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif l >= 4:
                        if l - space - oppospace >= 3 or space + oppospace >= 3:
                            score(4, 3, 0, list)
                        else:
                            score(4, 2, 0, list)
                    elif r - l >= 2:
                        if r - space - oppospace == 4:
                            score(4, -1, 1, list)
                        else:
                            score(r, space, 1, list)
                    else:
                        score(l, oppospace, 0, list)
                elif block == 2:
                    if space + oppospace >= 4:
                        if oppospace + space >= 5:
                            score(5, -1, 0, list)
                        else:
                            score(4, -1, 0, list)
                    elif r >= 4:
                        if r - space - oppospace >= 3 or space + oppospace >= 3:
                            score(4, 3, 0, list)
                        else:
                            score(4, 2, 0, list)
                    elif l - r >= 2:
                        if l - space - oppospace == 4:
                            score(4, -1, 1, list)
                        else:
                            score(l, space, 1, list)
                    else:
                        score(r, oppospace, 0, list)
                elif block == 3:
                    if space + oppospace >= 3:
                        score(oppospace + space, -1, 0, list)
                    elif l >= r:
                        if l - 2 >= oppospace + space:
                            score(l, oppospace, 1, list)
                        else:
                            score(space + oppospace, -1, 0, list)
                    else:
                        if r - 2 >= oppospace + space:
                            score(r, space, 1, list)
                        else:
                            score(space + oppospace, -1, 0, list)

            # if space < 0 and oppospace < 0:
            #     count += oppocount
            #     if block in range(1, 3):
            #         score(count, space, 1, list)
            #     elif block == 3:
            #         score(count, space, 2, list)
            #     elif block == 0:
            #         score(count, space, 0, list)
            # elif space < 0:
            #     if block == 0:
            #         score(l, oppospace, block, list)
            #     elif block == 1:
            #         score(l, oppospace, 1, list)
            #     elif block == 2:
            #         score(r, space, 0, list)
            #     elif block == 3:
            #         score(l, oppospace, 2, list)
            # elif oppospace < 0:
            #     if block == 0:
            #         score(r, space, block, list)
            #     elif block == 1:
            #         score(l, oppospace, 0, list)
            #     elif block == 2:
            #         score(r, space, 1, list)
            #     elif block == 3:
            #         score(r, space, 2, list)
            # else:
            #     if block == 0:
            #         if l >= r:
            #             score(l, oppospace, block, list)
            #         else:
            #             score(r, space, block, list)
            #     elif block == 1:
            #         score(l, oppospace, 0, list)
            #     elif block == 2:
            #         score(r, space, 0, list)
            #     elif block == 3:
            #         score(space+oppospace, -1, 0, list)

        def evaluate(player, y, x):
            list = [0] * 16
            calh(player, y, x, list)
            calv(player, y, x, list)
            calr(player, y, x, list)
            call(player, y, x, list)
            point = 0
            # [1000000, 40000, 800, 20, 1000, 80, 2, 100, 8, 0, 10, 1, 0, 6000]
            # if list[1] != 0 and list[4] != 0:
            #     point += 10000
            # if list[2] != 0 and list[4] != 0:
            #     point += 30000
            # if list[4] >= 2:
            #     point += 15000
            # if list[4] != 0 and list[5] != 0:
            #     point += 70
            # if list[2] != 0 and list[7] != 0:
            #     point += 40
            # if list[5] != 0 and list[7] != 0:
            #     point += 20
            # if list[4] != 0 and list[7] != 0:
            #     point += 80
            # if list[7] >= 2:
            #     point += 30
            for i in range(0, 16):
                point += list[i] * scores[i]

            # [1000000, 40000, 800, 20, 1000(4), 80, 2, 100, 8, 0, 10, 1, 0(12), 5000, 600, 800]
            if list[13] != 0 and (list[2] != 0 or list[4] != 0 or list[15] != 0 or list[14] != 0):
                point += 35000
            if list[13] >= 2:
                point += 35000
            if list[1] != 0 and list[13] != 0:
                point += 30000
            if (list[2] != 0 or list[14] != 0) and (list[4] != 0 or list[15] != 0):
                point += 30000
            if list[2] + list[14] >= 2:
                point += 30000
            if list[1] != 0 and (list[2] != 0 or list[14] != 0):
                point += 20000
            if list[4] + list[15] >= 2:
                point += 15000
            if list[1] != 0 and (list[4] != 0 or list[15] != 0):
                point += 10000
            if (list[4] != 0 or list[15] != 0 or list[2] != 0 or list[14] != 0 or list[13] != 0) and (list[7] >= 2):
                point += 300
            if (list[4] != 0 or list[15] != 0 or list[2] != 0 or list[14] != 0 or list[13] != 0) and list[7] != 0:
                point += 80
            if (list[4] != 0 or list[15] != 0 or list[2] != 0 or list[14] != 0 or list[13] != 0) and list[5] != 0:
                point += 30
            if list[5] != 0 and list[7] != 0:
                point += 100
            if list[7] >= 2:
                point += 30
            if list[5] >= 2:
                point += 120
            if (list[4] != 0 or list[15] != 0 or list[2] != 0 or list[14] != 0 or list[13] != 0) and list[3] != 0:
                point += 30
            if list[3] != 0 and list[7] + list[5] >= 1:
                point += 20
            # if player == 1 and y == 2 and x == 3 and chessboard[5, 3] == -1:
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
                if up - 1 < 0:
                    up = 0
                else:
                    up -= 1
                if left - 1 < 0:
                    left = 0
                else:
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

        points = np.full((15, 15), -np.inf, dtype=np.float)
        border = get_matrix()
        # border1 = []
        # if border[0] > 0:
        #     border1[0] = border[0] - 1
        # if border[1] < 15:
        #     border1[1] += 1
        # if border[2] > 0:
        #     border1[2] -= 1
        # if border[3] < 15:
        #     border1 += 1
        # print(border)
        # points1 = np.full((15, 15), -np.inf, dtype=np.float)
        oppopoints = np.full((15, 15), -np.inf, dtype=np.float)
        for y in range(border[0], border[1]):
            for x in range(border[2], border[3]):
                if chessboard[y, x] == 0:
                    # print("hhh")
                    points1 = np.full((15, 15), -np.inf, dtype=np.float)
                    chessboard[y, x] = self.color
                    points[y, x] = evaluate(self.color, y, x)
                    # a = evaluate(self.color, y, x)
                    border1 = get_matrix()
                    # print(border1)
                    # b = 0
                    for i in range(border1[2], border1[3]):
                        for j in range(border1[0], border1[1]):
                            if chessboard[j, i] == 0:
                                chessboard[j, i] = -self.color
                                # b += evaluate(-self.color, j, i)
                                points1[j, i] = evaluate(-self.color, j, i)
                                chessboard[j, i] = 0
                    # b1 = b2 = b3 = float("-inf")
                    # for i in range(border1[2], border1[3]):
                    #     for j in range(border1[0], border1[1]):
                    #         if points1[j, i] >= b1:
                    #             b3 = b2
                    #             b2 = b1
                    #             b1 = points1[j, i]
                    #         elif points1[j, i] >= b2:
                    #             b3 = b2
                    #             b2 = points1[j, i]
                    #         elif points1[j, i] > b3:
                    #             b3 = points1[j, i]
                    oppopoints[y, x] = np.max(points1)

                    # if self.color == -1:
                    #     # b = np.max(points1)
                    #     points[y, x] = a - 0.75 * b
                    # else:
                    #     bm = 0.5 * b1 + 0.35 * b2 + 0.15 * b3
                    #     points[y, x] = a - 1.7 * bm
                        # b = 0.8 * b1 + 0.2 * b2
                        # print(np.argmax(points1))
                        # print(points1[5, 5])
                        # print(b)
                        # points1 = np.full((15, 15), -np.inf, dtype=np.float)

                    # else:
                    #     b = 0.5 * b1 + 0.25 * b2 + 0.25 * b3
                    #     points[y, x] = a - b
                    # points[y, x] = a - b
                    chessboard[y, x] = 0
        for y in range(border[0], border[1]):
            for x in range(border[2], border[3]):
                if chessboard[y, x] == 0:
                    if self.color == -1:
                        if points1[y, x] == np.max(oppopoints):
                            points[y, x] -= 0.6 * oppopoints[y, x]
                        else:
                            points[y, x] -= 0.8 * oppopoints[y, x]
                        # b = np.max(points1)
                        # points[y, x] = a - 0.75 * b
                    else:
                        if points1[y, x] == np.max(oppopoints):
                            points[y, x] -= 0.5 * oppopoints[y, x]
                        else:
                            points[y, x] -= 1 * oppopoints[y, x]
                        # bm = 0.5 * b1 + 0.35 * b2 + 0.15 * b3
                        # points[y, x] = a - 1.7 * bm
        # print("init")
        y1 = x1 = 0
        m = float("-inf")

        for y in range(border[0], border[1]):
            for x in range(border[2], border[3]):
                if points[y, x] >= m:
                    if points[y, x] > m:
                        m = points[y, x]
                        x1 = x
                        y1 = y
                    elif math.pow((x - 7), 2) + math.pow((y - 7), 2) < math.pow((x1 - 7), 2) + math.pow((y1 - 7), 2):
                        x1 = x
                        y1 = y
        if self.color == 1 and np.sum(chessboard == -1) == 1 and chessboard[8, 8] == 0:
            new_pos = [6, 8]
        else:
            new_pos = [y1, x1]
        # print(points[2, 3])
        # print(points[1, 9])
        # print(points[3, 11])
        # print(new_pos)
        # if self.color == -1 and np.sum(chessboard == 1) == 1:
        #     if chessboard[6, 6] == 1 or chessboard[8, 6] == 1:
        #         new_pos = [7, 6]
        #     elif chessboard[6, 8] == 1 or chessboard[8, 8] == 1:
        #         new_pos = [7, 8]
        #     elif chessboard[7, 6] == 1 or chessboard[6, 7] == 1:
        #         new_pos = [6, 6]
        #     elif chessboard[7, 8] == 1 or chessboard[8, 7] == 1:
        #         new_pos = [8, 8]
        if self.color == -1 and np.sum(chessboard == 1) == 1:
            if chessboard[6, 6] == 1 or chessboard[7, 6] == 1:
                new_pos = [6, 7]
            elif chessboard[8, 6] == 1 or chessboard[8, 7] == 1:
                new_pos = [7, 6]
            elif chessboard[8, 8] == 1 or chessboard[7, 8] == 1:
                new_pos = [8, 7]
            elif chessboard[6, 8] == 1 or chessboard[6, 7] == 1:
                new_pos = [7, 8]

        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, return error.
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        # Add your decision into candidate_list, Records the chess board
        self.candidate_list.append(new_pos)
