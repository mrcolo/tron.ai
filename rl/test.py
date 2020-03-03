from stable_baselines import PPO2
from tron import TronEnv
import numpy as np
a_dic = {0: "left", 1: "down", 2: "right", 3: "up" }
dic = {0: "Draw", 1: "Hero wins", -2: "Enemy wins"}

def run_test(model):
    n_episodes = 100
    env  = TronEnv()
    tot_rewards = []
    actions = []
    for _ in range(0, n_episodes):
        obs = env.reset()
        #env.render()
        done = False
        moves = 0
        while not done:
            moves += 1
            action, _states = model.predict(obs)
            actions.append(a_dic[action])
            obs, reward, done, _ = env.step(action)
            # env.render()
        tot_rewards.append(reward)
        #print("GAME OVER: {} w/ {} moves, EPISODES -> [{}/{}] - MEAN -> [{}] ".format(dic[reward],moves, _ + 1, n_episodes,  np.array(tot_rewards).mean()))
    return np.array(tot_rewards).mean()
    
if __name__ == "__main__":
    model = PPO2.load("tron_student_20x20_3000000")
    reward_mean = run_test(model)
    print(reward_mean)