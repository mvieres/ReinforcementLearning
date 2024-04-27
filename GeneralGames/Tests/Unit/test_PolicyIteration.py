import unittest

from GeneralGames.Algorithms.PolicyIteration import PolicyIteration


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
        greedy_action = PolicyIteration.argmaxDict(q_value)
        self.assertEqual((5, 1), greedy_action)

    def test_listq(self):
        q_dict = {
            ((1, 1), 1): 10,
            ((2, 2), 1): 10
        }
        keys = list(q_dict.keys())
        print(keys[0][0])



if __name__ == '__main__':
    unittest.main()
