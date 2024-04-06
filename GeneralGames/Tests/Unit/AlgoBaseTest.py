import unittest

from GeneralGames.Algorithms.AlgoBase import AlgoBase


class MyTestCase(unittest.TestCase):

    def __int__(self):
        pass

    def test_greedy(self):
        q_value = {
            (0, 0): 10,
            (1, 0): 20,
            (3, 0): 30,
            (4, 0): 40,
            (5, 1): 50
        }
        greedy_action = AlgoBase.argmaxDict(q_value)
        self.assertEqual((5, 1), greedy_action)


if __name__ == '__main__':
    unittest.main()
