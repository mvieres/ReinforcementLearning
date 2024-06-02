from enum import Enum


class Player:
    def __init__(self, number: int):
        self.__playerNumber = number
        self.__policy = {}
        self.__fields = []  # List of tuples, i.e. [(1, 1), (1, 2), ...]
        pass

    def getFields(self):
        return self.__fields

    def addToFields(self, field: tuple):
        self.__fields.append(field)

    def setPolicy(self, policy):
        self.__policy = policy

    def getPolicy(self):
        return self.__policy

    def updatePolicy(self, state):
        pass


class Direction(Enum):
    Left = 2, "Left"
    Right = 5, "Right"
    LeftUp = 3, "LeftUp"
    LeftDown = 1, "LeftDown"
    RightUp = 4, "RightUp"
    RightDown = 6, "RightDown"

    def getInt(self):
        return self.value[0]


class Hex:
    """
    Hex is a game where two players try to connect two sides of a hexagonal board.
    The board is modeled as a hexagonal grid with a size of n x n. Player one plays from top to bottom and player two
    from left to right.
    """
    def __init__(self, size: int):
        self.__size = size
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.takenFields = []

    def setBoardSize(self, size):
        self.__size = size
