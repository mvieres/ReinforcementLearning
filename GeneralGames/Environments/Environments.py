from enum import Enum


class DirectionsGridWorld(Enum):
    UP = 3, "UP"
    DOWN = 1, "DOWN"
    LEFT = 2, "LEFT"
    RIGHT = 4, "RIGHT"


class Gridworld:

    def __init__(self, width, height, goal):
        self.width = width
        self.height = height
        self.boundaries = [width, height]
        self.player = [1, 1]
        self.goal = [goal[0], goal[1]]
        self.obstical = []

    def getPosition(self):
        return self.player

    def setBoundaries(self, boundary):
        self.boundaries = boundary

    def setStartingPoint(self, start):
        self.player = [start[0], start[1]]

    def getBoundaries(self):
        return self.boundaries

    def setObstical(self, obsticalList):
        self.obstical = self.obstical.append(obsticalList)

    def isInBoundaries(self, pos):
        return (0 <= pos[0] <= self.boundaries[0]) and (0 <= pos[1] <= self.boundaries[1])

    def isTerminal(self):
        return (self.player[0] == self.goal[0]) and (self.player[1] == self.goal[1])

    def __up(self):
        self.player[1] += 1
        if self.isInBoundaries(self.player):

            return
        else:
            self.player[1] -= 1
            raise AssertionError("No valid Direction")  # Make this different

    def __down(self):
        self.player[1] -= 1
        if self.isInBoundaries(self.player):

            return
        else:
            self.player[1] += 1
            raise AssertionError("No valid Direction")  # Make this different

    def __left(self):
        self.player[0] -= 1
        if self.isInBoundaries(self.player):

            return
        else:
            self.player[0] += 1
            raise AssertionError("No valid Direction")  # Make this different

    def __right(self):
        if not self.isTerminal():
            self.player[0] += 1

    def move(self, direction):
        if self.isTerminal():
            return [], False, "No valid step"

        moves = {
            1: self.__down,
            2: self.__left,
            3: self.__up,
            4: self.__right
        }

        if direction not in moves:
            raise AssertionError("Step rollout failed")

        return moves[direction]()
