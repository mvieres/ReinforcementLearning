import numpy as np
from enum import Enum


class DirectionsGridWorld(Enum):
    UP = 3
    DOWN = 1
    LEFT = 2
    RIGHT = 4


class Gridworld:

    def __init__(self, width, height, goal):
        self.width = width
        self.height = height
        self.boundaries = None
        self.player = [1, 1]
        self.goal = [goal[0], goal[1]]
        self.obstical = []
        self.directions = {
            "UP": self.__up,
            "DOWN": self.__down,
            "LEFT": self.__left,
            "RIGHT": self.__right,
        }

    def setBoundaries(self, boundary):
        self.boundaries = boundary

    def setStartingPoint(self, start):
        self.player = [start[0], start[1]]

    def getBoundaries(self):
        return self.boundaries

    def setObstical(self, obsticalList):
        self.boundaries = self.boundaries.append(obsticalList)

    def isInBoundaries(self, pos):
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

    def step(self, direction):
        if not self.hasHitGoal(self.player):
            if direction in self.directions:
                return self.directions[direction]
            else:
                AssertionError("Step rollout failed")
        else:
            info_flag = "Game already finished, no step needed"
            return info_flag
