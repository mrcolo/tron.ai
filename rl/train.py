import gym
from tron import TronEnv
from stable_baselines.common.vec_env import DummyVecEnv
#from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines.common.policies import MlpPolicy
from stable_baselines import PPO2
from stable_baselines import DQN

if __name__ == "__main__":
    env = DummyVecEnv([TronEnv])
    model = PPO2(MlpPolicy, env, verbose=1, tensorboard_log="./runs/")
    N = 20
    ts = 3000000
    model.learn(total_timesteps=ts)
    model.save("tron_student_{}x{}_{}".format(N,N,ts))

