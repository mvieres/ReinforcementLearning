import unittest

from Bandits.Classes.Env import Env


class EnvTest(unittest.TestCase):
    def __int__(self):
        self.test_float = [4, 4, 4, 4, 4]
    def test_q_value(self):
        self.assertEqual(Env().q_value(rewards=self.test_float, return_std=False), 4)

    def test_update_q_value(self):
        self.assertEqual(Env().update_q_value(reward_observation=4, q_old=4, n=2), 4)

if __name__ == '__main__':
    unittest.main()
