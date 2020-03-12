import gym
from tron import TronEnv
from stable_baselines.common.vec_env import DummyVecEnv
#from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines.common.policies import MlpPolicy
from stable_baselines import PPO2
import optuna
from test import run_test    
n_steps_per_eval = 15000000
optuna_study = optuna.create_study(
           study_name="{}_study".format("test"), 
           storage="sqlite:///params.db", 
           load_if_exists=True,
           pruner=optuna.pruners.MedianPruner())

# OPTIMIZE FUNCTIONS
def optimize_agent_params(trial):
    return {
        'n_steps': int(trial.suggest_loguniform('n_steps', 512, 2048)),
        'gamma': trial.suggest_loguniform('gamma', 0.9, 0.9999),
        'learning_rate': trial.suggest_loguniform('learning_rate', 1e-5, 1.),
        'ent_coef': trial.suggest_loguniform('ent_coef', 1e-8, 1e-1),
        'cliprange': trial.suggest_uniform('cliprange', 0.1, 0.4),
        'noptepochs': int(trial.suggest_loguniform('noptepochs', 1, 48)),
        'lam': trial.suggest_uniform('lam', 0.8, 1.)
    }
def optimize_params(trial, n_prune_evals_per_trial: int = 2, n_tests_per_eval: int = 1):
    model_params = optimize_agent_params(trial)
    train_env = DummyVecEnv([TronEnv])
    model = PPO2(MlpPolicy, 
                train_env, 
                verbose=0, 
                tensorboard_log="./logs/", 
                nminibatches=1,
                **model_params)
    # TODO fix this
    for eval_idx in range(n_prune_evals_per_trial):
        try:
            model.learn(n_steps_per_eval)
        except AssertionError:
            raise
 
        last_reward = run_test(model)

        trial.report(-1 * last_reward, eval_idx)
        
        if trial.should_prune(eval_idx):
            raise optuna.structs.TrialPruned()
    return -1 * last_reward
def get_model_params():
    params = optuna_study.best_trial.params
    print('Loaded best parameters as: {}'.format(params))

    return {
        'n_steps': int(params['n_steps']),
        'gamma': params['gamma'],
        'learning_rate': params['learning_rate'],
        'ent_coef': params['ent_coef'],
        'cliprange': params['cliprange'],
        'noptepochs': int(params['noptepochs']),
        'lam': params['lam'],
    } 
def run_optimization(n_trials: int = 10):
    try:
      optuna_study.optimize(optimize_params, n_trials=n_trials, n_jobs=1)
    except KeyboardInterrupt:
      pass
    print('Finished trials: {}'.format(len(optuna_study.trials)))
    print('Best trial: {}'.format(optuna_study.best_trial.value))
    return optuna_study.trials_dataframe()


if __name__ == "__main__":
    env = DummyVecEnv([TronEnv])
    params = {'cliprange': 0.33665282227943044, 
              'ent_coef': 3.344529418417107e-06, 
              'gamma': 0.966674189931648, 
              'lam': 0.9390867393163336, 
              'learning_rate': 0.00015, 
              'n_steps': 1000, 
              'noptepochs': 2}
    model = PPO2(MlpPolicy, env, verbose=1, tensorboard_log="./logs/", **params)
    model.learn(total_timesteps=5000000)
    #df = run_optimization()
    #print(df)
    model.save("tron_student_{}x{}_{}".format(40,40,50000000))

