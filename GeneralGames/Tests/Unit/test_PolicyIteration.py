import unittest

from GeneralGames.Algorithms.PolicyIteration import PolicyIteration


class MyTestCase(unittest.TestCase):

    def __int__(self):
        pass

    def test_greedy(self):
        d = {
            ((1, 1), 2): 10,
            ((1, 2), 1): 20,
            ((2, 2), 3): 30,
            ((1, 1), 1): 40,
            ((2, 2), 2): 50,
            ((2, 2), 4): 60,
        }
        supposed_output = {
            (1, 1): 1,
            (1, 2): 1,
            (2, 2): 4
        }
        self.assertEqual(PolicyIteration().greedy(d), supposed_output)

    def test_listq(self):
        q_dict = {
            ((1, 1), 1): 10,
            ((2, 2), 1): 10
        }
        keys = list(q_dict.keys())
        print(keys[0][0])

    def test_argMaxDict(self):
        d = {
            ((1, 1), 2): 10,
            ((1, 2), 1): 20,
            ((2, 2), 3): 30,
            ((1, 1), 1): 40,
            ((2, 2), 2): 50,
            ((2, 2), 4): 60,
        }
        supposed_output = {
            (1, 1): [(2, 10), (1, 40)],
            (1, 2): [(1, 20)],
            (2, 2): [(3, 30), (2, 50), (4, 60)]
        }
        self.assertEqual(supposed_output, PolicyIteration.transformQValuesDict(d))


if __name__ == '__main__':
    unittest.main()
