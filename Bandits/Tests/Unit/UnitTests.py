import unittest

from Bandits.Classes.Env import Env
from Bandits.Classes.GaussianBanditEnv import GaussianBanditEnv


class EnvTest(unittest.TestCase):

    def test_q_value(self):
        test_float = [4, 4, 4, 4, 4]
        self.assertEqual(Env().q_value(rewards=test_float, return_std=False), 4)


if __name__ == '__main__':
    unittest.main()
