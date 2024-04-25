import unittest
from GeneralGames.Environments.Environments import Gridworld
from GeneralGames.Environments.Environments import DirectionsGridWorld as DGW


class TestGridworldDirections(unittest.TestCase):

    def test_Enum(self):
        self.assertEqual(DGW.RIGHT.value[0], 4)
        self.assertEqual(DGW.LEFT.value[0], 2)
        self.assertEqual(DGW.UP.value[0], 3)
        self.assertEqual(DGW.DOWN.value[0], 1)


class TestGridWorld(unittest.TestCase):

    def test_Momvement(self):
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

    def test_cliff(self):
        gridworld = Gridworld(10, 10, [1, 1])
        gridworld.setStartingPoint([1, 1])
        gridworld.setCliff([1, 1])
        self.assertEqual(True, gridworld.isNegativeTerminal())
        gridworld.setCliff([2, 2])
        gridworld.player = [2, 2]
        self.assertEqual(True, gridworld.isNegativeTerminal())

    def test_isinboundaries(self):
        gridworld = Gridworld(10, 10, [3, 3])
        gridworld.player = [-1, 0]
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
        self.assertEqual(10, gridworld.rewards[(1, 1)])

    def test_rolloutReward(self):
        gridworld = Gridworld(10, 10, [1, 1])
        gridworld.setRewards({(1, 1): 10})
        self.assertEqual(10, gridworld.rolloutReward([1, 1]))
        self.assertEqual(0, gridworld.rolloutReward([1, 2]))


if __name__ == '__main__':
    unittest.main()
