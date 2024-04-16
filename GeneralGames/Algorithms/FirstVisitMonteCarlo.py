from ..Environments import Environments
import numpy.random as rnd
import numpy as np


class MonteCarloPolicyEvaluation:

    def __init__(self, tol, gamma, width, height, goal, initialDistribution=None, maxIteration=10000):
        self.rewardPath = {}
        self.maxIteration = maxIteration
        self.policy = None
        self.initialDistribution = initialDistribution
        self.pathUntilTermination = np.array([])
        self.tol = tol
        self.visitations = {}
        self.env = Environments.Gridworld(width, height, goal)
        self.gamma = gamma

    def setStartingPoint(self, start):
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
        self.pathUntilTermination.append([self.env.player])
        return

    def compute_V_value(self):

        pass

    def converged(self):
        return np.abs(1 - 2) < self.tol  # TODO

    def addToDict(self):
        player_as_tuple = tuple(self.env.player)
        if player_as_tuple not in self.rewardPath:
            self.rewardPath[player_as_tuple] = None
        if player_as_tuple not in self.visitations:
            self.visitations[player_as_tuple] = 0
        return

    def countUp(self):
        self.visitations[tuple(self.env.player)] += 1
        return

    def setStartingPosition(self, pos):
        self.env.setPosition(pos)

    def generateSamplePaths(self):  # Roll out one sample path
        self.__resetSamplePath()
        while not self.env.isTerminal():  # Sample path
            actions = [1, 2, 3, 4]
            for action in [1, 2, 3, 4]:  # check for valid actions
                try:
                    self.env.moveTest(action)
                except:
                    actions.remove(action)

            if self.policy is None:
                action_played = rnd.choice(actions)  # Uniform Sampling
            else:
                raise Exception("?")
            self.env.moveRestricted(action_played)
            self.__addToSamplePath()
        return

    def updateRewards(self):
        for key in self.rewardPath.keys():
            self.rewardPath[key] = self.env.rolloutReward()

    def __resetSamplePath(self):
        self.pathUntilTermination = [self.env.startingPoint]

    def firstVisitPolicyEvalV(self):
        while not self.converged():
            self.generateSamplePaths()
            self.updateRewards()
