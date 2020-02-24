from stable_baselines import PPO2
from tron import TronEnv
import numpy as np
a_dic = {0: "left", 1: "down", 2: "right", 3: "up" }
dic = {0: "Draw", 1: "Hero wins", -1: "Enemy wins"}

if __name__ == "__main__":
    n_episodes = 1
    env  = TronEnv()
    model = PPO2.load("tron_20x20_1000000")
    tot_rewards = []
    actions = []
    #episodes = 1
    for _ in range(0, n_episodes):
        obs = env.reset()
        env.render()
        done = False
        moves = 0
        while not done:
            moves += 1
            action, _states = model.predict(obs)
            actions.append(a_dic[action])
            obs, reward, done, info = env.step(action)
            env.render()
        tot_rewards.append(reward)
        print("GAME OVER: {} w/ {} moves, EPISODES -> [{}/{}] - MEAN -> [{}] ".format(dic[reward],moves, _ + 1, n_episodes,  np.array(tot_rewards).mean()))
        print(np.array(tot_rewards).mean())
    print(actions)
    