
from tron import TronEnv
import random
import numpy as np
import time
import keyboard
import os
import time

dic = {-1: "haha u lose", 0: "nice its a draw", 1:"you win wow ur so smart"}
if __name__ == "__main__":
    env  = TronEnv()
    state = env.reset()
    
    done = False
    ratio = []
    for i in range(0, 100):
        state = env.reset()
        env.render()
        done = False
        while not done:
            a = keyboard.read_key()
            if a == 'left':
                h_a = 0
                
            if a == 'up':
                h_a = 1
                
            if a == 'right':
                h_a = 2
                
            if a == 'down':
                h_a = 3
            next_state, reward, done, _ = env.step(h_a)
            env.render()
            state = next_state
        print(dic[reward])
   # print(np.array(ratio).mean())sadf