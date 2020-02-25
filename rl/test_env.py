
from tron import TronEnv
import random
import numpy as np
import time
import keyboard
if __name__ == "__main__":
    env  = TronEnv()
    state = env.reset()
    
    done = False
    ratio = []
    for i in range(0, 1):
        state = env.reset()
        env.render()
        while not done:
            a = input()
            if a == 'a':
                h_a = 0
                
            if a == 'w':
                h_a = 1
                
            if a == 'd':
                h_a = 2
                
            if a == 's':
                h_a = 3
            next_state, reward, done, _ = env.step(h_a)
            env.render()
            state = next_state
        print(reward)
   # print(np.array(ratio).mean())sadf