import numpy as np

from ..Environments import Environments
import numpy.random as rnd


class MonteCarloPolicyEvaluation:

    def __init__(self, tol, gamma, width, height, goal, initialDistribution=None, maxIteration=10000):
        self.rewardPath = {}
        self.width = width
        self.height = height
        self.maxIteration = maxIteration
        self.policy = None
        self.initialDistribution = initialDistribution
        self.pathUntilTermination = []
        self.tol = tol
        self.visitations = {}
        self.env = Environments.Gridworld(width, height, goal)
        self.gamma = gamma
        self.valueApproximation = {}
        self.numberIterations = 0

    def getValueApproximation(self) -> dict:
        return self.valueApproximation

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

    def converged(self, old: dict, new: dict) -> bool:
        """
        CONVERGENCE Criterium?
        :param old:
        :param new:
        :return:
        """
        if old is None:
            return False
        elif len(old) < self.width * self.height:
            return False
        else:
            for key in old.keys():
                if np.abs(old[key] - new[key]) < self.tol: # ??????
                    return True

    def addSamplePathToMetricDicts(self) -> None:
        """
        Adds the generated sample path to the metric dictionaries, e.g., V approx and visitation count.
        :return: None
        """
        try:
            for state in self.pathUntilTermination:
                player_as_tuple = tuple(state)
                if player_as_tuple not in self.valueApproximation:
                    self.valueApproximation[player_as_tuple] = 0
                if player_as_tuple not in self.visitations:
                    self.visitations[player_as_tuple] = 0
            pass
        except:
            Exception("pathUntilTermination is empty.")

    def countUp(self, state: list) -> None:
        """
        Counts up the visitation count for a given state.
        :param state: list
        :return: None
        """
        try:
            self.visitations[tuple(state)] += 1
        except:
            self.visitations[tuple(state)] = 1
        pass

    def generateSamplePaths(self) -> None:  # Roll out one sample path
        """
        Generate one sample path until termination (or until max iterations are reached).
        :return: None
        """
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

    def rolloutRewardtoSample(self, timeIndex: int) -> float:
        """
        Roll out reward for given time index from given timepoint using discount factor gamma.
        :param timeIndex: int
        :return: float
        """
        reward = 0
        for t in range(timeIndex + 1, len(self.pathUntilTermination)):
            state = self.pathUntilTermination[t]
            reward += self.gamma ** (t - timeIndex) * self.env.rolloutReward(state)
        return reward

    def firstVisitPolicyEvalV(self) -> None:
        """
        Perform first visit monte carlo evaluation of given policy for value function.
        :return: None
        """

        self.numberIterations = 0
        v_old = {}
        v_new = {} # ?
        while not self.converged(v_old, v_new):
            self.generateSamplePaths()
            self.addSamplePathToMetricDicts()
            v_old = self.valueApproximation # ?
            for t in range(len(self.pathUntilTermination)):
                state = self.pathUntilTermination[t]
                if state not in self.pathUntilTermination[0:t]:
                    # Roll out rewards:
                    state_as_tuple = tuple(state)
                    v = self.env.rolloutReward(state) + self.rolloutRewardtoSample(t)
                    self.valueApproximation[state_as_tuple] = (v / (self.visitations[state_as_tuple] + 1)) + \
                                                              (self.visitations[state_as_tuple] / (
                                                                      self.visitations[state_as_tuple] + 1)) * \
                                                              self.valueApproximation[state_as_tuple]
                    self.countUp(state)
            v_new = self.valueApproximation # ?
            self.numberIterations += 1
