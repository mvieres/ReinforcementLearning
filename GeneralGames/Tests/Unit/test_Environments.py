import unittest

import numpy as np

from GeneralGames.Environments.Environments import Gridworld
from GeneralGames.Environments.Environments import DirectionsGridWorld as DGW


class TestGridworldDirections(unittest.TestCase):

    def test_Enum(self):
        self.assertEqual(DGW.RIGHT.value[0], 4)
        self.assertEqual(DGW.LEFT.value[0], 2)
        self.assertEqual(DGW.UP.value[0], 3)
        self.assertEqual(DGW.DOWN.value[0], 1)


class TestGridWorld(unittest.TestCase):

    def test_movement(self):
        gridworld = Gridworld(10, 10, [3, 3])
        gridworld.setStartingPoint([0, 0])
        gridworld.moveRestricted(4)
        self.assertEqual([1, 0], gridworld.getPosition())
        gridworld.moveRestricted(3)
        self.assertEqual([1, 1], gridworld.getPosition())
        gridworld.moveRestricted(2)
        self.assertEqual([0, 1], gridworld.getPosition())
        gridworld.moveRestricted(1)
        self.assertEqual([0, 0], gridworld.getPosition())

    def test_goal(self):
        gridworld = Gridworld(10, 10, [1, 1])
        gridworld.setStartingPoint([1, 1])
        result = gridworld.isPositiveTerminal()
        self.assertEqual(True, result)

    def test_setCliff(self):
        gridworld = Gridworld(10, 10, [1, 1])
        gridworld.setStartingPoint([1, 1])
        cliff = [[1, 1], [1, 2], [1, 3]]
        gridworld.setCliff(cliff)
        self.assertEqual(cliff, gridworld.getCliff())

    def test_isinboundaries(self):
        gridworld = Gridworld(10, 10, [3, 3])
        gridworld.setPosition([-1, 0])
        self.assertEqual(False, gridworld.isInBoundaries())

    def test_setObstical(self):
        gridworld = Gridworld(10, 10, [1, 1])
        gridworld.setCliff([1, 1])

    def test_terminal(self):
        gridworld = Gridworld(10, 10, [1, 1])
        gridworld.setPosition([1, 1])
        self.assertEqual(True, gridworld.isTerminal())

    def test_setRewads(self):
        gridworld = Gridworld(10, 10, [1, 1])
        gridworld.setRewards({(1, 1): 10})
        self.assertEqual(10, gridworld.getRewards()[(1, 1)])

    def test_rolloutReward(self):
        gridworld = Gridworld(10, 10, [1, 1])
        gridworld.setRewards({(1, 1): 10})
        self.assertEqual(10, gridworld.rolloutReward([1, 1]))
        self.assertEqual(0, gridworld.rolloutReward([1, 2]))

    def testDicts(self):
        dict = {((1, 1), 1): 10, ((2, 2), 1): 4}
        a = list(dict.keys())
        b = a[0]

    def testMoreDict(self):
        d ={
            (1, 1): [(2, 10), (1, 40)],
            (1, 2): [(1, 20)],
            (2, 2): [(3, 30), (2, 50), (4, 60)]
        }
        b = d[(1, 1)]
        a = [b[_][1] for _ in range(len(b))]
        c = b[np.argmax(a)][0]


if __name__ == '__main__':
    unittest.main()
