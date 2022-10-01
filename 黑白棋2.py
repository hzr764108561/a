import math

import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)
bad = [(0, 0), (0, 7), (7, 7), (7, 0)]
worse = [(0, 2), (0, 3), (0, 4), (0, 5), (7, 2), (7, 3),
         (7, 4), (7, 5), (2, 0), (3, 0), (4, 0), (5, 0),
         (2, 7), (3, 7), (4, 7), (5, 7)]
good = [(1, 2), (1, 3), (1, 4), (1, 5), (6, 2), (6, 3),
        (6, 4), (6, 5), (2, 1), (3, 1), (4, 1), (5, 1),
        (2, 6), (3, 6), (4, 6), (5, 6)]
best = [(0, 1), (1, 1), (1, 0), (0, 6), (1, 6), (1, 7), (6, 1), (7, 1), (6, 0), (6, 6), (7, 6), (6, 7)]


# don't change the class name
class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        self.candidate_list = []

    def find_end(self, color, other_color, node, direction, chessboard):
        num = 0
        turn = []
        while 8 > node[0] > -1 and 8 > node[1] > -1 \
                and chessboard[(node[0], node[1])] == color:
            turn.append((node[0], node[1]))
            node[0] += direction[0]
            node[1] += direction[1]
            num += 1
        if 8 > node[0] > -1 and 8 > node[1] > -1 and chessboard[(node[0], node[1])] == other_color:
            return turn, num
        else:
            return None, 0

    def judge(self, chessboard):
        num = 0
        for i in bad:
            if chessboard[(i[0], i[1])] == self.color:
                num += 10000
            elif chessboard[(i[0], i[1])] != COLOR_NONE:
                num -= 10000
        for i in worse:
            if chessboard[(i[0], i[1])] == self.color:
                num += 50
            elif chessboard[(i[0], i[1])] != COLOR_NONE:
                num -= 50
        for i in good:
            if chessboard[(i[0], i[1])] == self.color:
                num -= 50
            elif chessboard[(i[0], i[1])] != COLOR_NONE:
                num += 50
        for i in best:
            if chessboard[(i[0], i[1])] == self.color:
                num -= 100
            elif chessboard[(i[0], i[1])] != COLOR_NONE:
                num += 100
        return num

    def find(self, color, chessboard, depth, whole_depth, self_num, end_sign):
        step = []
        score = []
        is_self = False
        if self.color == COLOR_BLACK:
            if self.color == color:
                other_color = COLOR_WHITE
                is_self = True
            else:
                other_color = COLOR_BLACK
        else:
            if self.color == color:
                other_color = COLOR_BLACK
                is_self = True
            else:
                other_color = COLOR_WHITE
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        for i in range(len(idx)):
            num = 0
            turn = []
            var = idx[i]
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if j == k == 0:
                        continue
                    if 8 > var[0] + j > -1 and 8 > var[1] + k > -1 and \
                            chessboard[(var[0] + j, var[1] + k)] == other_color:
                        a = var[0] + j
                        b = var[1] + k
                        z, n = self.find_end(other_color, color, [a, b], (j, k), chessboard)
                        if z is not None:
                            num += n
                            turn += z
            if turn:
                if is_self:
                    num += self_num
                else:
                    num = self_num - num
                chessboard[var] = color
                for j in range(len(turn)):
                    chessboard[turn[j]] = color
                turn.append(var)
                step.append(var)
                if depth == whole_depth:
                    self.candidate_list.append(var)
                if depth > 1:
                    m = self.find(other_color, chessboard, depth - 1, whole_depth, num, end_sign)
                    if m is not None:
                        score.append(m)
                else:
                    if end_sign == 0:
                        z = self.judge(chessboard)
                        score.append(z + num * 5)
                    else:
                        score.append(num)
                for j in range(len(turn)):
                    chessboard[turn[j]] = other_color
                chessboard[var] = COLOR_NONE
        if score:
            if is_self:
                var1 = score.index(min(score))
            else:
                var1 = score.index(max(score))
            if depth == whole_depth:
                if self.candidate_list:
                    self.candidate_list.append(self.candidate_list.pop(var1))
            return score[var1]

    # The input is the current chessboard. Chessboard is a numpy array.
    def go(self, chessboard):
        # Clear candidate_list, must do this step
        self.candidate_list.clear()
        # ==================================================================
        # Write your algorithm here
        # Here is the simplest sample:Random decision
        idx = np.where(chessboard == self.color)
        idx = list(zip(idx[0], idx[1]))
        idx2 = np.where(chessboard == COLOR_NONE)
        idx2 = list(zip(idx2[0], idx2[1]))
        if len(idx2) <= 15:
            self.find(self.color, chessboard, len(idx2), len(idx2), len(idx), 1)
        else:
            self.find(self.color, chessboard, 1, 1, len(idx), 0)


# ==============Find new pos========================================
# Make sure that the position of your decision on the chess board is empty.
# If not, the system will return error.
# Add your decision into candidate_list, Records the chessboard
# You need to add all the positions which are valid
# candidate_list example: [(3,3),(4,4)]
# You need append your decision at the end of the candidate_list,
# candidate_list example: [(3,3),(4,4),(4,4)]
# we will pick the last element of the candidate_list as the position you choose.
# In above example, we will pick (4,4) as your decision.
# If there is no valid position, you must return an empty list.