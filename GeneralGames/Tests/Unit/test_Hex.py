import unittest

from GeneralGames.Environments import Hex


class TestHexEnum(unittest.TestCase):

    def testEnum(self):
        self.assertEqual(Hex.Direction.Right.getInt(), 5)
        self.assertEqual(Hex.Direction.Left.getInt(), 2)
        self.assertEqual(Hex.Direction.LeftUp.getInt(), 3)
        self.assertEqual(Hex.Direction.LeftDown.getInt(), 1)
        self.assertEqual(Hex.Direction.RightUp.getInt(), 4)
        self.assertEqual(Hex.Direction.RightDown.getInt(), 6)


class TestHex(unittest.TestCase):

    def test(self):
        pass