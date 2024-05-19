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
        self.__boundaries = [width, height]
        self.__player = [None, None]
        self.goal = [goal[0], goal[1]]
        self.cliff = []
        self.__startingPoint = None

    def getPosition(self) -> list:
        return self.__player

    def setPosition(self, pos) -> None:
        self.__player = pos

    def setBoundaries(self, boundary) -> None:
        self.__boundaries = boundary

    def setStartingPoint(self, start: list) -> None:
        self.__startingPoint = [start[0], start[1]]
        self.__player = self.__startingPoint.copy()

    def getBoundaries(self) -> list:
        return self.__boundaries

    def setCliff(self, cliff: list) -> None:
        for cliff_vector in cliff:
            self.cliff.append(cliff_vector)

    def getCliff(self) -> list:
        return self.cliff

    def setRewards(self, rewards: dict) -> None:
        self.__rewards = rewards

    def getRewards(self) -> dict:
        return self.__rewards

    def resetPlayerToStart(self) -> None:
        self.__player = self.__startingPoint.copy()

    def isInBoundaries(self) -> bool:
        if self.__player is not None:
            return (0 <= self.__player[0] <= self.__boundaries[0]) and (0 <= self.__player[1] <= self.__boundaries[1])
        else:
            return False

    def isPositiveTerminal(self) -> bool:
        return self.__player == self.goal

    def isNegativeTerminal(self) -> bool:
        return any(all(item in sublist for item in self.__player) for sublist in self.cliff)

    def isTerminal(self):
        return self.isPositiveTerminal() or self.isNegativeTerminal()

    def __up(self):
        self.__player[1] += 1
        if self.isInBoundaries():
            pass
        else:
            self.__player[1] -= 1
            raise Exception

    def __down(self):
        self.__player[1] -= 1
        if self.isInBoundaries():
            pass
        else:
            self.__player[1] += 1
            raise Exception

    def __left(self):
        self.__player[0] -= 1
        if self.isInBoundaries():
            pass
        else:
            self.__player[0] += 1
            raise Exception

    def __right(self):
        self.__player[0] += 1
        if self.isInBoundaries():
            pass
        else:
            self.__player[0] -= 1
            raise Exception

    def moveRestricted(self, direction) -> None:

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
        self.__player[1] += 1
        return

    def __downUnres(self):
        self.__player[1] -= 1
        return

    def __leftUnres(self):
        self.__player[0] -= 1
        return

    def __rightUnres(self):
        self.__player[0] += 1
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

    def __upTest(self) -> bool:
        self.__player[1] += 1
        if self.isInBoundaries():
            self.__player[1] -= 1
            return True
        else:
            self.__player[1] -= 1
            return False

    def __downTest(self) -> bool:
        self.__player[1] -= 1
        if self.isInBoundaries():
            self.__player[1] += 1
            return True
        else:
            self.__player[1] += 1
            return False

    def __leftTest(self) -> bool:
        self.__player[0] -= 1
        if self.isInBoundaries():
            self.__player[0] += 1
            return True
        else:
            self.__player[0] += 1
            return False

    def __rightTest(self) -> bool:
        self.__player[0] += 1
        if self.isInBoundaries():
            self.__player[0] -= 1
            return True
        else:
            self.__player[0] -= 1
            return False

    def moveTest(self, direction) -> bool:
        """
        Testing a move direction without actully moving the player
        :param direction:
        :return:
        """
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
            return self.__rewards[tuple(state)]  # TODO: eliminate try except
        except:
            return 0
