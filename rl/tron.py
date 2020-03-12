import gym
from gym import spaces
from gym.utils import seeding
import random
import numpy as np
from stable_baselines import PPO2
from game import TronGame
dic = {0: "left", 1: "up", 2: "right", 3: "down" }

N = 40
BOARD = np.zeros((N, N), dtype=int)

class TronEnv(gym.Env):
    def __init__(self):
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=N, shape = (N * N + 4,), dtype=np.int32)
        self.curr_board = None
        self.p_pos = None
        self.e_pos = None
        self.e_prev = None
        self.p_prev = None
        self.game = TronGame(N, 8)

    def step(self, action, p=0):
        assert self.action_space.contains(action)
        #e_action = self.game.bot_turn()
        if p == 1:
            if (action + 2 == self.e_prev) or (action - 2 == self.e_prev):
                action = self.e_prev

            curr_board, e_pos, reward, e_done = self.game.move(action, self.e_pos)
            self.e_pos = e_pos
            self.curr_board = curr_board
            
            curr_board = self.curr_board.flatten()
            p_pos = np.array([self.p_pos]).flatten()
            e_pos = np.array([self.e_pos]).flatten()
            state = np.concatenate((curr_board,e_pos, p_pos), axis=0).tolist()
            self.e_prev = action

            if e_done:
                return state, 1, -1, e_done, {}
            else:
                return state, 0, 0, e_done, {}

        else:
            if (action + 2 == self.p_prev) or (action - 2 == self.p_prev):
                action = self.p_prev

            curr_board, p_pos, reward, p_done = self.game.move(action, self.p_pos)
            self.p_pos = p_pos
            self.curr_board = curr_board

            curr_board = self.curr_board.flatten()
            p_pos = np.array([self.p_pos]).flatten()
            e_pos = np.array([self.e_pos]).flatten()
        
            state = np.concatenate((curr_board,p_pos, e_pos), axis=0).tolist()
            self.p_prev = action

            if p_done:
                return state, -1, 1, p_done, {}
            else:
                return state, 0, 0, p_done, {}

    def reset(self):
        curr_board, p_pos, e_pos = self.game.start_game()
        
        self.p_pos = p_pos
        self.e_pos = e_pos
        self.curr_board = curr_board            
        
        curr_board = curr_board.flatten()
        p_pos = np.array([p_pos]).flatten()
        e_pos = np.array([e_pos]).flatten()

        p_state = np.concatenate((curr_board,p_pos, e_pos), axis=0).tolist()
        e_state = np.concatenate((curr_board,e_pos, p_pos), axis=0).tolist()

        return p_state, e_state
    def render(self):
        self.game.print_board()