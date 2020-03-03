import gym
from gym import spaces
from gym.utils import seeding
import random
import numpy as np
from stable_baselines import PPO2
from game import TronGame
dic = {0: "left", 1: "up", 2: "right", 3: "down" }

N = 20
BOARD = np.zeros((N, N), dtype=int)

class TronEnv(gym.Env):
    def __init__(self):
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=N, shape = (N * N + 4,), dtype=np.int32)
        self.curr_board = None
        self.p_pos = None
        self.e_pos = None
        self.game = TronGame(20, 2)
        #self.teacher = PPO2.load("tron_20x20_1000000")
        self.temp_state = None
        self.prev_action = None

    def step(self, action):
        assert self.action_space.contains(action)

        if (action + 2 == self.prev_action) or (action - 2 == self.prev_action):
            action = self.prev_action


        e_action = self.game.bot_turn()
        _, p_pos, reward, p_done = self.game.move(action, self.p_pos)
        curr_board, e_pos, _, e_done = self.game.move(e_action, self.e_pos)
        reward = 0
        if p_done:
            reward -= 1
        if e_done:
            reward += 1
        self.curr_board = curr_board
        self.p_pos = p_pos
        self.e_pos = e_pos
        curr_board = curr_board.flatten()
        p_pos = np.array([p_pos]).flatten()
        e_pos = np.array([e_pos]).flatten()
        state = np.concatenate((curr_board,p_pos, e_pos), axis=0).tolist()
        self.temp_state = state
        self.prev_action = action

        return state, reward, p_done or e_done, {}

    def reset(self):
        curr_board, p_pos, e_pos = self.game.start_game()
        self.p_pos = p_pos
        self.e_pos = e_pos
        self.curr_board = curr_board            
        curr_board = curr_board.flatten()
        p_pos = np.array([p_pos]).flatten()
        e_pos = np.array([e_pos]).flatten()

        state = np.concatenate((curr_board,p_pos, e_pos), axis=0).tolist()
        self.temp_state = state
        
        return state
    def render(self):
        self.game.print_board()