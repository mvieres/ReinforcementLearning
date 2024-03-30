import unittest

from Bandits.Classes.GaussianBanditEnv import GaussianBanditEnv


class GaussianEnvTest(unittest.TestCase):

    def test_step(self):
        action = [1, 2, 3, 4]
        mean_param = [0.3, 0.4, 0.5, 0.6]
        for i in range(len(action)):
            reward = GaussianBanditEnv(mean_param=mean_param, max_steps=1).step(i)
            self.assertIsInstance(reward, float)


if __name__ == '__main__':
    unittest.main()
