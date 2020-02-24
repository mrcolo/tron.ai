
from tron import TronEnv
import random
import numpy as np

if __name__ == "__main__":
    env  = TronEnv()
    state = env.reset()
    
    done = False
    ratio = []
    for i in range(0, 10):
        state = env.reset()
        env.render()
        while not done:
            next_state, reward, done, _ = env.step(random.randrange(0, 4))
            env.render()
            state = next_state
        print(reward)
        ratio.append(reward)
    print(ratio)
   # print(np.array(ratio).mean())