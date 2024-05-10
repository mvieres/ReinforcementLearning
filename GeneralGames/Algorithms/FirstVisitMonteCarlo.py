import numpy as np

from ..Environments import Environments
from ..Algorithms import PolicyIteration
import numpy.random as rnd


class MonteCarloPolicyEvaluation:

    def __init__(self, tol, gamma, width, height, goal, initialDistribution=None, maxIteration=10000):

        self.width = width
        self.height = height
        self.maxIteration = maxIteration
        self.policy = None
        self.initialDistribution = initialDistribution
        self.pathUntilTermination = []
        self.tol = tol
        self.visitationsForV = {}
        self.visitationsForQ = {}
        self.env = Environments.Gridworld(width, height, goal)
        self.gamma = gamma
        self.valueApproximation = {}
        self.numberIterations = 0
        self.qApproximation = {}  # intended layout: {(state, action): q_value} with state = (x, y) and action
        self.actionsUntilTermination = []
        self.actionPlayed = None
        self.stateActionPairs = None
        self.__epsilon = None
        self.policyIteration = PolicyIteration.PolicyIteration()

    def getValueApproximation(self) -> dict:
        return self.valueApproximation

    def getQApproximation(self) -> dict:
        return self.qApproximation

    def setMaxIterations(self, maxIterations: int) -> None:
        self.maxIteration = maxIterations

    def setPolicy(self, policy: str, epsilon = 0.1) -> None:
        self.policy = policy
        self.__epsilon = epsilon

    def __improvePolicy(self):
        policy_methods = {
            None: lambda: rnd.choice([1, 2, 3, 4]),
            "greedy": lambda: self.policyIteration.greedy(self.qApproximation),
            "epsilonGreedy": lambda: self.policyIteration.epsilonGreedy(self.qApproximation, self.__epsilon)
        }

        try:
            return policy_methods[self.policy]()
        except KeyError:
            raise Exception(f"Policy {self.policy} not known")

    def __addStateToSamplePath(self):
        self.pathUntilTermination.append(tuple(self.env.getPosition()))
        pass

    def __addActionsToSamplePath(self) -> None:
        self.actionsUntilTermination.append(self.actionPlayed)
        pass

    def compute_V_value(self):

        pass

    def pathConverged(self, count) -> bool:
        """
        CONVERGENCE Criterium?
        :param old:
        :param new:
        :return:
        """
        # TODO: change to use of q / v approximations
        if count < self.maxIteration:
            return False
        else:
            return True

    def policyConverged(self, count) -> bool:
        """
        CONVERGENCE Criterium?
        :param old:
        :param new:
        :return:
        """
        # TODO: implement right convergence criterium
        if count < self.maxIteration:
            return False
        else:
            return True

    def addSamplePathToMetricDicts(self) -> None:
        """
        Adds the generated sample path to the metric dictionaries, e.g., V approx and visitation count.
        :return: None
        """
        try:
            for state in self.pathUntilTermination:  # Add states for Valueapprox
                player_as_tuple = tuple(state)
                self.valueApproximation.setdefault(player_as_tuple, 0)
                self.visitationsForV.setdefault(player_as_tuple, 0)

            state_action_pairs = [(tuple(self.pathUntilTermination[i]), self.actionsUntilTermination[i])
                                  for i in range(len(self.pathUntilTermination) - 1)]
            state_action_pairs.append((tuple(self.pathUntilTermination[-1]), None))  # Add last state with no action
            self.stateActionPairs = state_action_pairs
            for sap in state_action_pairs:  # Add state action pairs to qApproximation and visitationsForQ for Q Approx
                self.qApproximation.setdefault(sap, 0)
                self.visitationsForQ.setdefault(sap, 0)

        except Exception as e:
            print(f"Unknown error in addSamplePathToMetricDicts: {e}")
            raise

    def countUpState(self, state: list) -> None:
        """
        Counts up the visitation count for a given state.
        :param state: list
        :return: None
        """
        try:
            self.visitationsForV[tuple(state)] += 1
        except Exception as e:
            print(f"state as tuple key not in dict in countUpState: {e}")
            raise
        pass

    def countUpStateActionPair(self, state: list, action: int) -> None:
        """
        Counts up the visitation count for a given state action pair.
        :param state: list
        :param action: int
        :return: None
        """
        try:
            self.visitationsForQ[(tuple(state), action)] += 1
        except Exception as e:
            print(f"state action as key not in dict in countUpStateActionPair: {e}")
            raise
        pass

    def generateSamplePaths(self) -> None:  # Roll out one sample path
        """
        Generate one sample path until termination (or until max iterations are reached).

        IDEA: Use this function for q and v
        :return: None
        """
        self.__resetSamplePath()
        self.env.resetPlayerToStart()
        self.__addStateToSamplePath()
        while not self.env.isTerminal():  # Sample path
            actions = [1, 2, 3, 4]
            for action in [1, 2, 3, 4]:  # check for valid actions
                try:
                    self.env.moveTest(action)
                except:
                    actions.remove(action)

            if self.policy is None:
                action_played = rnd.choice(actions) if actions else None  # Uniform Sampling
            else:
                assert isinstance(self.policy, dict)  # self.policy has to be a dict here!
                action_played = self.policy[tuple(self.env.getPosition())] if actions else None  # TODO: Check this line
            self.env.moveRestricted(action_played)
            self.actionPlayed = action_played
            self.__addActionsToSamplePath()
            self.__addStateToSamplePath()

    def __resetSamplePath(self):
        self.pathUntilTermination = []
        self.actionsUntilTermination = []

    def setStartingPoint(self, startingPoint: list) -> None:
        self.env.setStartingPoint(startingPoint)

    def rolloutRewardtoSampleV(self, timeIndex: int) -> float:
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

    def rolloutRewardToSampleQ(self, timeIndex: int) -> float:
        """
        Roll out reward for given time index from given timepoint using discount factor gamma.
        Attention: reward does not depend on action, hence rollout does not consider action played
        :param timeIndex: int
        :return: float
        """
        reward = 0
        for t in range(timeIndex + 1, len(self.stateActionPairs)):
            state = self.stateActionPairs[t][0]
            reward += self.gamma ** (t - timeIndex) * self.env.rolloutReward(state)
        return reward

    def firstVisitPolicyEvalV(self) -> None:
        """
        Perform first visit monte carlo evaluation of given policy for value function.
        :return: None
        """
        # Marked for removal
        self.numberIterations = 0
        v_old = {}
        v_new = {}  # ?
        while not self.pathConverged(self.numberIterations):
            self.generateSamplePaths()
            self.addSamplePathToMetricDicts()
            v_old = self.valueApproximation  # ?
            for t in range(len(self.pathUntilTermination)):
                state = self.pathUntilTermination[t]
                if state not in self.pathUntilTermination[0:t]:
                    # Roll out rewards:
                    state_as_tuple = tuple(state)
                    v = self.env.rolloutReward(state) + self.rolloutRewardtoSampleV(t)
                    self.valueApproximation[state_as_tuple] = (v / (self.visitationsForV[state_as_tuple] + 1)) + \
                                                              (self.visitationsForV[state_as_tuple] / (
                                                                      self.visitationsForV[state_as_tuple] + 1)) * \
                                                              self.valueApproximation[state_as_tuple]
                    self.countUpState(state)
            v_new = self.valueApproximation  # ?
            self.numberIterations += 1

    def firstVisitPolicyEvalQ(self, policy = None) -> None:
        """
        Perform first visit monte carlo evaluation of given policy for action value function.
        :return: None
        """
        self.numberIterations = 0
        while not self.pathConverged(self.numberIterations):
            self.generateSamplePaths()
            self.addSamplePathToMetricDicts()
            q_old = 0
            for t in range(len(self.stateActionPairs)):
                sap = self.stateActionPairs[t]
                if sap not in self.stateActionPairs[0:t]:
                    q = self.env.rolloutReward(sap[0]) + self.rolloutRewardtoSampleV(t)
                    self.qApproximation[sap] = (q / (self.visitationsForQ[sap] + 1)) + \
                                               (self.visitationsForQ[sap] / (self.visitationsForQ[sap] + 1)) * \
                                               self.qApproximation[sap]
                    self.countUpStateActionPair(sap[0], sap[1])
            self.numberIterations += 1

    def firstVisitMonteCarloIteration(self) -> None:
        """
        Perform first visit monte carlo iteration for Q value.
        :return: None
        """
        self.numberIterations = 0
        while not self.policyConverged(self.numberIterations):
            self.firstVisitPolicyEvalQ()
            self.policy = self.__improvePolicy()
            self.numberIterations += 1

    def getOptimalPolicy(self) -> dict:
        return self.policy
