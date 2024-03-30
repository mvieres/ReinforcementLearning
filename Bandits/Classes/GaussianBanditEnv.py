import numpy as np

from Env import Env


class GaussianBanditEnv(Env):

    def __init__(self, mean_param, max_steps):
        """
        Create a multiarmed bandit with len(mean_param) arms
        :param mean_param:
        :param max_steps:
        """
        try:
            assert isinstance(mean_param, float)
        except:
            print("mean_param has to be float")
        self.steps = 1
        self.mean_param = mean_param
        self.max_steps = max_steps

        pass

    def step(self, action_index):
        """
        Roll out bandit given the played action
        :param action_index:
        :return: new state, reward, info
        """
        assert isinstance(action_index, int)
        # Sample Reward from distribution
        reward_sample = np.random.normal(self.mean_param[action_index], 1)
        return reward_sample

    def reset(self):
        self.mean_param = []
        pass

