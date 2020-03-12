import numpy as np
import random

from math import inf as infinity
from random import choice
import platform
import time
from os import system
import sys
import copy
sys.setrecursionlimit(10000)
COMP = +1

class TronGame ():
    def __init__(self, N, depth):
        self.N = N
        self.board = None
        self.p_pos = []
        self.e_pos = []
        self.depth = depth

    # EVALS
    def is_done(self, pos):
        if self.board[pos[0]][pos[1]]:
            return True
        return False
    def evaluate(self,state, player):
        """
        Function to heuristic evaluation of state.
        :param state: the state of the current board
        :return: +1 if the computer wins; -1 if the human wins; 0 draw
        """
        me, you = None, None
        if player > 0:
            me = self.e_pos
            you = self.p_pos
        else:
            me = self.p_pos
            you = self.e_pos
        if self.is_done(you):
            score = +1
        elif self.is_done(me):
            score = -1
        else:
            score = 0
        return score
    def available_cells(self, state, pos):
        result = []
        l_x, l_y = pos[0], pos[1] - 1
        left = state[l_x][l_y]
        if not left:
            result.append([l_x,l_y])

        r_x, r_y = pos[0],pos[1] + 1
        right = state[r_x][r_y]
        
        if not right:
            result.append([r_x,r_y])
        
        u_x, u_y = pos[0] - 1,pos[1]
        up = state[u_x][u_y]
        if not up:
            result.append([u_x,u_y])
        
        d_x, d_y = pos[0] + 1, pos[1]
        down = state[d_x][d_y]
        if not down:
            result.append([d_x,d_y])
        return result
    def empty_cells(self,state):
        """
        Each empty cell will be added into cells' list
        :param state: the state of the current board
        :return: a list of empty cells
        """
        cells = []
        for i in range(self.N):
            for j in range(self.N):
                if state[i][j] == 0:
                    cells.append([i, j])
        return cells
    
    # """ AI """
    def minimax(self,start, state, depth, player):
        """
        Choose best move
        :param state: current state of the board
        :param depth: node index in the tree (0 <= depth <= 9),
        but never nine in this case (see iaturn() function)
        :param player: an human or a computer
        :return: a list with [the best row, best col, best score]
        """
        if depth == 0:
            score = self.evaluate(state, player)
            return [-1, -1, score]

        if player == COMP:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        empties =  self.available_cells(state, start)
        for cell in empties:
            x, y = cell[0], cell[1]
            state[x][y] = 1
            me = [x, y]     
            score = self.minimax(me, state, depth - 1, -player)
            state[x][y] = 0
            score[0], score[1] = x, y

            if player == COMP:
                if score[2] > best[2]:
                    best = score 
            else:
                if score[2] < best[2]:
                    best = score
        return best
    def bot_turn(self):
        """
        It calls the minimax function if the depth < 9,
        else it choices a random coordinate.
        :return:
        """
        x, y = None, None
        board = copy.deepcopy(self.board)
        move = self.minimax(self.e_pos, board, self.depth, COMP)
        x, y = move[0], move[1]
        randy = random.randrange(0,100)
        if [x,y] != [-1,-1] and randy % 5 != 0:
            return self.coor_to_action(x, y)
        else:
            moves = self.available_cells(self.board, self.e_pos)
            if len(moves) != 0:
                move = choice(moves)
                return self.coor_to_action(move[0], move[1])
            else:
                return 1
    
    # GAME LOGIC
    def move(self, action, curr_pos):
        # left
        if action == 0:
            curr_pos[1] = (curr_pos[1] - 1) if (curr_pos[1] - 1) >= 0 else curr_pos[1]
            done = self.is_done(curr_pos)
            if not done:
                self.board[curr_pos[0]][curr_pos[1]] = 1
            else:
                return self.board, curr_pos, -1, True
        # up
        if action == 1:
            curr_pos[0] = curr_pos[0] - 1 if curr_pos[0] - 1 >= 0 else curr_pos[0]
            done = self.is_done(curr_pos)
            if not done:
                self.board[curr_pos[0]][curr_pos[1]] = 1
            else:
                return self.board, curr_pos, -1, True

        # right
        if action == 2:
            curr_pos[1] = (curr_pos[1] + 1) if (curr_pos[1] + 1) < self.N else curr_pos[1]
            done = self.is_done(curr_pos)
            if not done:
                self.board[curr_pos[0]][curr_pos[1]] = 1
            else:
                return self.board, curr_pos, -1, True

        # down
        if action == 3:
            curr_pos[0] = curr_pos[0] + 1 if curr_pos[0] + 1 < self.N else curr_pos[0]
            done = self.is_done(curr_pos)
            if not done:
                self.board[curr_pos[0]][curr_pos[1]] = 1
            else:
                return self.board, curr_pos, -1, True
            
        return self.board, curr_pos, 0, False
    def start_game(self):
        """
        Simulates the board at the start of the game
        """
        self.board = np.zeros((self.N, self.N), dtype=int)
        # for i in range(self.N):
        #     self.board[0] = [1] * self.N
        #     self.board[self.N - 1] = [1] * self.N
        #     self.board[i][0] = 1
        #     self.board[i][self.N - 1] = 1

        self.p_pos = [self.N - self.N // 4, self.N // 2]
        self.e_pos = [self.N // 4, self.N // 2]
        # while self.p_pos[0] == self.e_pos[0] and  self.p_pos[1] == self.e_pos[1]: 
        #     self.e_pos = [random.randrange(1, self.N - 2), random.randrange(1, self.N - 2)]

        self.board[self.p_pos[0]][self.p_pos[1]] = 1
        self.board[self.e_pos[0]][self.e_pos[1]] = 1

        return self.board, self.p_pos, self.e_pos
    
    # UTILS
    def print_board(self):
        all_e = []
        all_p = []
        print("")
        start = 0
        end = self.N
        for i in range(0,self.N):
            if i >= 10:
                print(i, end=" ")
            else:
                print("{} ".format(i), end=" ")
            for j in range(0, self.N):
                if self.board[i][j] == 1:
                    if [i,j] == self.e_pos or [i,j] in all_e:
                        print("\033[1;37;41mx\033[0m", end=" ")
                        if [i, j] not in all_e:
                            all_e.append(self.e_pos)
                    elif [i,j] == self.p_pos or [i,j] in all_p:
                        print("\033[0;37;42mx\033[0m", end=" ")
                        if [i, j] not in all_p:
                            all_p.append(self.p_pos)
                    else:
                        print("x", end=" ")
                elif self.board[i][j] == 0:
                    print(" ", end =" ")
            print("")
            start += self.N
            end += self.N
    def print_a_board(self, board):
        print("")
        start = 0
        end = self.N
        for i in range(0,self.N):
            for j in range(0, self.N):
                if board[i][j] == 1:
                    print("x", end =" ")
                elif board[i][j] == 0:
                    print(" ", end =" ")
            print("")
            start += self.N
            end += self.N
    def possible_moves(self, pos): 
        moves = []
        # left up right down
        if (self.e_pos[1] - 1) >= 0:
            moves.append([pos[0], pos[1] - 1])
        if (pos[0] - 1) >= 0:
            moves.append([pos[0] - 1, pos[1]])
        if (pos[1] + 1) <= self.N:
            moves.append([pos[0], pos[1] + 1])
        if (pos[0] + 1) <= self.N:
            moves.append([pos[0] + 1, pos[1]])
        return moves
    def coor_to_action(self, x, y):
        moves = self.possible_moves(self.e_pos)
        return moves.index([x, y])