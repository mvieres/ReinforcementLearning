import numpy as np


class Env:

    def __int__(self):
        pass

    def q_value(self, rewards, return_std=False):
        q_value = np.mean(rewards)
        q_value_std = np.std(rewards)
        if return_std:
            return q_value, q_value_std
        else:
            return q_value

    def update_q_value(self, reward_observation, q_old, n):
        return ((n-1)/n)*q_old + (1/n)*reward_observation
