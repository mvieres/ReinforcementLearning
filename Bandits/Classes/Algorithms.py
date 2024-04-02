import numpy as np

from Bandits.Classes.GaussianBanditEnv import GaussianBanditEnv


class play_etc_gaussian_bandit:

    def __int__(self, mean_param, max_steps, num_actions):
        self.mean_param = mean_param
        self.max_steps = max_steps
        pass

    def _etc(self, m):
        counter = 0
        q_value = np.zeros(len(self.mean_param))

        while counter <= m:
            for i in range(len(self.actions)):
                reward = GaussianBanditEnv.step(action_index=i)
                q_value[i] = GaussianBanditEnv.update_q_value(q_old=q_value[i], reward_observation=reward, n=counter)
