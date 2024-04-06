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
        gridworld.move(4)
        self.assertEqual([1, 0], gridworld.getPosition())
        gridworld.move(3)
        self.assertEqual([1, 1], gridworld.getPosition())
        gridworld.move(2)
        self.assertEqual([0, 1], gridworld.getPosition())
        gridworld.move(1)
        self.assertEqual([0, 0], gridworld.getPosition())

    def test_Movement_boundary(self):
        gridworld = Gridworld(10, 10, [3, 3])
        gridworld.setStartingPoint([0, 0])
        gridworld.move(2)
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

    def test_isinboundaries(self):
        gridworld = Gridworld(10, 10, [1, 1])
        gridworld.player = [-1, 3]
        self.assertEqual(False, gridworld.isInBoundaries())

    def test_setObstical(self):
        gridworld = Gridworld(10, 10, [1, 1])
        gridworld.setCliff([1, 1])


if __name__ == '__main__':
    unittest.main()
