import numpy as np
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
        self.directions = {
            DirectionsGridWorld.UP: self.__up,
            DirectionsGridWorld.DOWN: self.__down,
            DirectionsGridWorld.LEFT: self.__left,
            DirectionsGridWorld.RIGHT: self.__right,
        }

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
        # Wrong Boundaries
        return (pos[0] <= self.boundaries[0]) and (pos[1] <= self.boundaries[1])

    def hasHitGoal(self, pos):
        return (pos[0] == self.goal[0]) and (pos[1] == self.goal[1])

    def __up(self):
        self.player[1] += 1
        if self.isInBoundaries(self.player):

            return
        else:
            self.player[1] -= 1
            AssertionError("No valid Direction")  # Make this different

    def __down(self):
        self.player[1] -= 1
        if self.isInBoundaries(self.player):

            return
        else:
            self.player[1] += 1
            AssertionError("No valid Direction")  # Make this different

    def __left(self):
        self.player[0] -= 1
        if self.isInBoundaries(self.player):

            return
        else:
            self.player[0] += 1
            AssertionError("No valid Direction")  # Make this different

    def __right(self):
        self.player[0] += 1
        if self.isInBoundaries(self.player):

            return
        else:
            self.player[0] -= 1
            AssertionError("No valid Direction")  # Make this different

    def move(self, direction):
        if not self.hasHitGoal(self.player):
            if direction in self.directions: #That does not work
                return self.directions[direction]
            else:
                AssertionError("Step rollout failed")
        else:
            info_flag = "Game already finished, no step needed"
            return info_flag
