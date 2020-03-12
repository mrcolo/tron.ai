import gym 
import torch
from tron import TronEnv
from PPO import PPO, Memory
import numpy as np
import time
def adv_training():
    ############## Hyperparameters ##############
    # creating environment
    env = TronEnv()
    state_dim = env.observation_space.shape[0]
    action_dim = 4
    render = True
    solved_reward = 230         # stop training if avg_reward > solved_reward
    log_interval = 20           # print avg reward in the interval
    max_episodes = 10        # max training episodes
    max_timesteps = 300         # max timesteps in one episode
    n_latent_var = 64           # number of variables in hidden layer
    update_timestep = 2000      # update policy every n timesteps
    lr = 0.002
    betas = (0.9, 0.999)
    gamma = 0.99                # discount factor
    K_epochs = 4                # update policy for K epochs
    eps_clip = 0.2              # clip parameter for PPO
    random_seed = None
    #############################################
    
    if random_seed:
        torch.manual_seed(random_seed)
        env.seed(random_seed)
    
    h_memory = Memory()
    a_memory = Memory()
    
    hero = PPO(state_dim, action_dim, n_latent_var, lr, betas, gamma, K_epochs, eps_clip)
    hero.load()

    adv = PPO(state_dim, action_dim, n_latent_var, lr, betas, gamma, K_epochs, eps_clip)
    adv.load()

    timestep = 0
    
    # training loop
    for _ in range(1, max_episodes+1):
        p_state, e_state = env.reset()
        for t in range(max_timesteps):
            timestep += 1
            
            # Running policy_old:
            p_action = hero.policy_old.act(np.array(p_state), h_memory)
            e_action = adv.policy_old.act(np.array(e_state), a_memory)
            
            p_state, _, _, h_done, _ = env.step(p_action, 0)
            e_state, _, _, a_done, _ = env.step(e_action, 1)

            # if render:
            #     env.render()
            if h_done or a_done:
                env.render()
                break

if __name__ == "__main__":
    adv_training()