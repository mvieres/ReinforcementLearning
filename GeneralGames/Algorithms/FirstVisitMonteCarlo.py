import numpy as np

from ..Environments import Environments
from ..Algorithms import PolicyIteration
import numpy.random as rnd


class MonteCarloPolicyEvaluation:

    def __init__(self, tol, gamma, width, height, goal, initialDistribution=None, maxIteration=10000):

        self.__percentage = 90
        self.__currentPolicy = None
        self.width = width
        self.height = height
        self.maxIteration = maxIteration
        self.__policyType = None
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
        self.__watchPolicy = False

    def getValueApproximation(self) -> dict:
        return self.valueApproximation

    def getQApproximation(self) -> dict:
        return self.qApproximation

    def setPercentageForConvergenceCriterion(self, percentage: float) -> None:
        """
        Default is: 90% of state-action pairs have to be below the tolerance value.
        :param percentage: float 1 - 100
        :return: None
        """
        self.__percentage = percentage

    def setWatchPolicyDuringIteration(self, watch: bool) -> None:
        """
        Set boolean flag if policy should be validated during iteration. (for debugging purpose)
        :param watch:
        :return:
        """
        self.__watchPolicy = watch

    def setMaxIterations(self, maxIterations: int) -> None:
        self.maxIteration = maxIterations

    def setPolicy(self, policy: str, epsilon=0.1) -> None:
        """
        Choose policy type to be used within policy evaluation.
        :param policy: String, either "greedy" or "epsilonGreedy"
        :param epsilon: Optinal, float, epsilon value for epsilon greedy policy
        :return: None
        """
        self.__policyType = policy
        self.__epsilon = epsilon

    def __policyWrapper(self):
        """
        Wrapper to use policy specified by setPolicy() method.
        :return:
        """
        policy_methods = {
            None: lambda: rnd.choice([1, 2, 3, 4]),
            "greedy": lambda: self.policyIteration.greedy(self.qApproximation),
            "epsilonGreedy": lambda: self.policyIteration.epsilonGreedy(self.qApproximation, self.__epsilon)
        }

        try:
            return policy_methods[self.__policyType]()
        except KeyError:
            raise Exception(f"Policy {self.__policyType} not known")

    def __addStateToSamplePath(self):
        self.pathUntilTermination.append(tuple(self.env.getPosition()))
        pass

    def __addActionsToSamplePath(self) -> None:
        self.actionsUntilTermination.append(self.actionPlayed)
        pass

    def compute_V_value(self):

        pass

    def evalConverged(self, old, new) -> bool:
        """
        Convergence criterium for Q / V Evaluation: When x% of state-action pairs are below tolerance value qApproximation
        is converged.
        :param old: dict qApproximation of state-action-pairs before iteration
        :param new: dict qApproximation of state-action-pairs after iteration
        :return: bool
        """
        result = []
        keys = list(old.keys())
        for key in keys:
            if key not in new:
                result.append(False)
            elif np.abs(old[key] - new[key]) > self.tol:
                result.append(False)
            else:
                result.append(True)
        return self.__checkPercentageOfTrue(result)

    def __checkPercentageOfTrue(self, result) -> bool:
        true_count = sum(result)
        total_count = len(result)
        if total_count == 0:
            return False
        true_percentage = (true_count / total_count) * 100
        return true_percentage >= self.__percentage

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
                actions.remove(action) if not self.env.moveTest(action) else None
            if self.__currentPolicy is None:
                action_played = rnd.choice(actions) if actions else None  # Uniform Sampling
            else:
                assert isinstance(self.__currentPolicy, dict)  # self.policy has to be a dict here!
                try:
                    action_played = self.__currentPolicy[
                        tuple(self.env.getPosition())] if actions else None  # TODO: Check this
                except:
                    action_played = rnd.choice(actions) if actions else None  # Fallback for
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
        self.numberIterations = 0
        v_old = {}
        v_new = {}
        while not self.evalConverged(v_old, v_new):
            v_old = self.valueApproximation.copy()
            self.generateSamplePaths()
            self.addSamplePathToMetricDicts()
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
            v_new = self.valueApproximation.copy()  # ?

    def firstVisitPolicyEvalQ(self) -> None:
        """
        Perform first visit monte carlo evaluation of given policy for action value function.
        :return: None
        """
        q_old = {}
        q_new = {}
        while not self.evalConverged(q_old, q_new):
            q_old = self.qApproximation.copy()
            self.generateSamplePaths()
            self.addSamplePathToMetricDicts()
            for t in range(len(self.stateActionPairs)):
                sap = self.stateActionPairs[t]
                if sap not in self.stateActionPairs[0:t]:
                    q = self.env.rolloutReward(sap[0]) + self.rolloutRewardtoSampleV(t)
                    self.qApproximation[sap] = (q / (self.visitationsForQ[sap] + 1)) + \
                                               (self.visitationsForQ[sap] / (self.visitationsForQ[sap] + 1)) * \
                                               self.qApproximation[sap]
                    self.countUpStateActionPair(sap[0], sap[1])
            q_new = self.qApproximation.copy()

    def firstVisitMonteCarloIteration(self) -> None:
        """
        Perform first visit monte carlo iteration for Q value.
        :return: None
        """
        self.numberIterations = 0
        while not self.policyConverged(self.numberIterations):
            while self.validatePolicy():  # Check if policy is valid throughout iteration
                self.firstVisitPolicyEvalQ()
                self.performPolicyIterationStep()
                self.numberIterations += 1

    def getCurrentPolicy(self) -> dict:
        return self.__currentPolicy

    def performPolicyIterationStep(self) -> None:
        """
        Perform one step of policy iteration.
        :return: None
        """
        self.__currentPolicy = self.__policyWrapper().copy()
        pass

    def validatePolicy(self) -> bool:
        """
        Check for valid policy for each state.
        :return: If policy is valid for each state return True, if one state has invalid action, return False.
        """
        if self.qApproximation == {}:
            return True
        stateActionPairs = list(self.qApproximation.keys())
        for sap in stateActionPairs:
            if sap[1] is not None:
                if not self.env.moveTest(sap[1]):
                    return False
        return True

    def vEvalConverged(self, numberIterations):
        if numberIterations < self.maxIteration:
            return False
        else:
            return True
        pass
