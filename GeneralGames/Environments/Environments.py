from enum import Enum


class DirectionsGridWorld(Enum):
    UP = 3, "UP"
    DOWN = 1, "DOWN"
    LEFT = 2, "LEFT"
    RIGHT = 4, "RIGHT"


class Gridworld:

    def __init__(self, width, height, goal):
        self.__rewards = {}
        self.width = width
        self.height = height
        self.boundaries = [width, height]
        self.player = [None, None]
        self.__goal = [goal[0], goal[1]]
        self.__cliff = []
        self.startingPoint = None

    def getPosition(self) -> list:
        return self.player

    def setPosition(self, pos) -> None:
        self.player = pos

    def setBoundaries(self, boundary) -> None:
        self.boundaries = boundary

    def setStartingPoint(self, start: list) -> None:
        self.startingPoint = [start[0], start[1]]
        self.player = self.startingPoint.copy()

    def getBoundaries(self) -> list:
        return self.boundaries

    def setCliff(self, cliff: list) -> None:
        for cliff_vector in cliff:
            self.__cliff.append(cliff_vector)

    def getCliff(self) -> list:
        return self.__cliff

    def setRewards(self, rewards: dict) -> None:
        self.__rewards = rewards

    def resetPlayerToStart(self) -> None:
        self.player = self.startingPoint.copy()

    def isInBoundaries(self) -> bool:
        return (0 <= self.player[0] <= self.boundaries[0]) and (0 <= self.player[1] <= self.boundaries[1])

    def isPositiveTerminal(self) -> bool:
        return self.player == self.__goal

    def isNegativeTerminal(self) -> bool:
        return any(all(item in sublist for item in self.player) for sublist in self.__cliff)

    def isTerminal(self):
        return self.isPositiveTerminal() or self.isNegativeTerminal()

    def __up(self):
        self.player[1] += 1
        if self.isInBoundaries():
            pass
        else:
            self.player[1] -= 1
            raise Exception

    def __down(self):
        self.player[1] -= 1
        if self.isInBoundaries():
            pass
        else:
            self.player[1] += 1
            raise Exception

    def __left(self):
        self.player[0] -= 1
        if self.isInBoundaries():
            pass
        else:
            self.player[0] += 1
            raise Exception

    def __right(self):
        self.player[0] += 1
        if self.isInBoundaries():
            pass
        else:
            self.player[0] -= 1
            raise Exception

    def moveRestricted(self, direction):

        moves = {
            1: self.__down,
            2: self.__left,
            3: self.__up,
            4: self.__right
        }

        if direction not in moves:
            raise AssertionError("Step rollout failed")
        moves[direction]()

    def __upUnres(self):
        self.player[1] += 1
        return

    def __downUnres(self):
        self.player[1] -= 1
        return

    def __leftUnres(self):
        self.player[0] -= 1
        return

    def __rightUnres(self):
        self.player[0] += 1
        return

    def move(self, direction) -> None:

        moves = {
            1: self.__downUnres,
            2: self.__leftUnres,
            3: self.__upUnres,
            4: self.__rightUnres
        }

        if direction not in moves:
            raise AssertionError("Step rollout failed")
        return moves[direction]()

    def __upTest(self):
        self.player[1] += 1
        if self.isInBoundaries():
            self.player[1] -= 1
            return
        else:
            self.player[1] -= 1
            raise Exception

    def __downTest(self):
        self.player[1] -= 1
        if self.isInBoundaries():
            self.player[1] += 1
            return
        else:
            self.player[1] += 1
            raise Exception

    def __leftTest(self):
        self.player[0] -= 1
        if self.isInBoundaries():
            self.player[0] += 1
            return
        else:
            self.player[0] += 1
            raise Exception

    def __rightTest(self):
        self.player[0] += 1
        if self.isInBoundaries():
            self.player[0] -= 1
            return
        else:
            self.player[0] -= 1
            raise Exception

    def moveTest(self, direction) -> None:

        moves = {
            1: self.__downTest,
            2: self.__leftTest,
            3: self.__upTest,
            4: self.__rightTest
        }

        if direction not in moves:
            raise AssertionError("Step rollout failed")
        return moves[direction]()

    def rolloutReward(self, state: list) -> float:
        # Rollout strictly for Gridworld reward profiles
        try:
            return self.__rewards[tuple(state)]
        except:
            return 0
