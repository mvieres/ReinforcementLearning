import unittest
from GeneralGames.Environments.Environments import Gridworld
from GeneralGames.Environments.Environments import DirectionsGridWorld as DGW


class TestGridworldDirections(unittest.TestCase):

    def test_Enum(self):
        self.assertEqual(DGW.RIGHT.value[0], 4)
        self.assertEqual(DGW.LEFT.value[0], 2)
        self.assertEqual(DGW.UP.value[0], 3)
        self.assertEqual(DGW.DOWN.value[0], 1)

    def test_something(self):

        self.assertEqual(True, False)  # add assertion here


class TestGridWorld(unittest.TestCase):

    def test_Momvement(self):
        gridworld = Gridworld(3, 3, [3, 3])
        gridworld.setStartingPoint([1, 1])
        gridworld.move(DGW.UP.value[0])
        self.assertEqual([1, 2], gridworld.getPosition())


if __name__ == '__main__':
    unittest.main()
