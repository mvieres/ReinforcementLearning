from ..Environments import Environments
import numpy.random as rnd
import numpy as np


class MonteCarloPolicyEvaluation:

    def __init__(self, tol, gamma, width, height, goal, initialDistribution=None, maxIteration=10000):
        self.rewardPath = {}
        self.maxIteration = maxIteration
        self.policy = None
        self.initialDistribution = initialDistribution
        self.pathUntilTermination = []
        self.tol = tol
        self.visitations = {}
        self.env = Environments.Gridworld(width, height, goal)
        self.gamma = gamma
        self.value = {}

    def getValue(self) -> dict:
        return self.value

    def setMaxIterations(self, maxIterations: int) -> None:
        self.maxIteration = maxIterations

    def setStartingPoint(self, start: list):
        self.env.player = start
        self.env.startingPoint = start

    def resetPath(self):
        self.env.resetPlayerToStart()
        self.rewardPath = {}
        self.visitations = {}
        self.pathUntilTermination = [self.env.startingPoint]

    def setPolicy(self):
        # TODO: Mapping to use epsilon greedy etc.
        return

    def __addToSamplePath(self):
        self.pathUntilTermination.append(tuple(self.env.player))
        return

    def compute_V_value(self):

        pass

    def converged(self) -> bool:
        # Placeholder
        return True

    def addToDict(self) -> None:
        # TODO: change setup
        player_as_tuple = tuple(self.env.player)
        if player_as_tuple not in self.rewardPath:
            self.rewardPath[player_as_tuple] = None
        if player_as_tuple not in self.visitations:
            self.visitations[player_as_tuple] = 0

    def countUp(self) -> None:
        # TODO: change setup
        self.visitations[tuple(self.env.player)] += 1
        pass

    def generateSamplePaths(self) -> None:  # Roll out one sample path
        self.__resetSamplePath()
        while not self.env.isTerminal():  # Sample path
            self.__addToSamplePath()
            actions = [1, 2, 3, 4]
            for action in [1, 2, 3, 4]:  # check for valid actions
                try:
                    self.env.moveTest(action)
                except:
                    actions.remove(action)

            if self.policy is None:
                action_played = rnd.choice(actions) if actions else None  # Uniform Sampling
            else:
                raise Exception("?")
            self.env.moveRestricted(action_played)
        self.__addToSamplePath()

    def __resetSamplePath(self):
        self.pathUntilTermination = []

    def firstVisitPolicyEvalV(self):
        while not self.converged():
            self.generateSamplePaths()
            for t in range(len(self.pathUntilTermination)):
                state = self.pathUntilTermination[t]
                if state not in self.pathUntilTermination[0:t]:
                    # Roll out rewards:



