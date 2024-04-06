from enum import Enum


class DirectionsGridWorld(Enum):
    UP = 3, "UP"
    DOWN = 1, "DOWN"
    LEFT = 2, "LEFT"
    RIGHT = 4, "RIGHT"


class Gridworld:

    def __init__(self, width, height, goal):
        self.rewards = {}
        self.width = width
        self.height = height
        self.boundaries = [width, height]
        self.player = [1, 1]
        self.goal = [goal[0], goal[1]]
        self.cliff = []

    def getPosition(self):
        return self.player

    def setBoundaries(self, boundary):
        self.boundaries = boundary

    def setStartingPoint(self, start):
        self.player = [start[0], start[1]]

    def getBoundaries(self):
        return self.boundaries

    def setCliff(self, obsitcal):
        self.cliff.append(obsitcal)

    def setRewards(self, rewardList):
        assert len(rewardList)>0
        assert rewardList[1] < 0
        self.rewards = rewardList

    def isInBoundaries(self):
        return (0 <= self.player[0] <= self.boundaries[0]) and (0 <= self.player[1] <= self.boundaries[1])

    def isPositiveTerminal(self):
        return self.player == self.goal

    def isNegativeTerminal(self):
        return any(all(item in sublist for item in self.player) for sublist in self.cliff)

    def isTerminal(self):
        return self.isPositiveTerminal() or self.isNegativeTerminal()

    def __up(self):
        self.player[1] += 1
        if self.isInBoundaries():
            return
        else:
            self.player[1] -= 1
            return

    def __down(self):
        self.player[1] -= 1
        if self.isInBoundaries():

            return
        else:
            self.player[1] += 1
            return

    def __left(self):
        self.player[0] -= 1
        if self.isInBoundaries():
            return
        else:
            self.player[0] += 1
            return

    def __right(self):
        self.player[0] += 1
        if self.isInBoundaries():
            return
        else:
            self.player[0] -= 1
            return

    def move(self, direction):
        if self.isTerminal():
            return [], False, "No valid step"

        moves = {
            1: self.__down,
            2: self.__left,
            3: self.__up,
            4: self.__right
        }
        x_old = self.player
        if direction not in moves:
            raise AssertionError("Step rollout failed")
        return moves[direction]()

    def rolloutReward(self):
        # Rollout strictly for Gridworld with reward profiles
        if self.isPositiveTerminal():
            return self.rewards[0]

        if self.isNegativeTerminal():
            return self.rewards[1]
