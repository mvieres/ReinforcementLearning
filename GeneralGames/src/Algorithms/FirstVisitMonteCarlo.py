import numpy as np
import numpy.random as rnd

from ..Environments import Gridworld
from ..Algorithms import PolicyIteration


class MonteCarloPolicyEvaluation:

    def __init__(self, tol, gamma, width, height, goal, initialDistribution=None, maxIteration=10000):
        #super().__init__()
        self.percentage = 90
        self.__currentPolicy = {}
        self.width = width
        self.height = height
        self.__maxIteration = maxIteration
        self.__policyType = None
        self.initialDistribution = initialDistribution
        self.pathUntilTermination = []
        self.tol = tol
        self.__visitationsForV = {}
        self.__visitationsForQ = {}
        self.env = Gridworld.Gridworld(width, height, goal)
        self.__gamma = gamma
        self.valueApproximation = {}
        self.numberIterations = 0
        self.qApproximation = {}  # intended layout: {(state, action): q_value} with state = (x, y) and action
        self.actionsUntilTermination = []
        self.__actionPlayed = None
        self.__stateActionPairs = None
        self.__epsilon = None
        self.policyIteration = PolicyIteration.PolicyIteration()
        self.__watchPolicy = False
        self.__numberOfIterations = 0

    def getVisitationsForV(self) -> dict:
        return self.__visitationsForV

    def getVisitationsForQ(self) -> dict:
        return self.__visitationsForQ

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
        self.percentage = percentage

    def setWatchPolicyDuringIteration(self, watch: bool) -> None:
        """
        Set boolean flag if policy should be validated during iteration. (for debugging purpose)
        :param watch:
        :return:
        """
        self.__watchPolicy = watch

    def setMaxIterations(self, maxIterations: int) -> None:
        self.__maxIteration = maxIterations

    def setPolicy(self, policy: str, epsilon=0.1) -> None:
        """
        Choose policy type to be used within policy evaluation.
        :param policy: String, either "greedy" or "epsilonGreedy"
        :param epsilon: Optinal, float, epsilon value for epsilon greedy policy
        :return: None
        """
        self.__policyType = policy
        self.__epsilon = epsilon

    def resetIterationCounter(self) -> None:
        self.__numberOfIterations = 0

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
        self.actionsUntilTermination.append(self.__actionPlayed)
        pass

    def __evalConverged(self, old, new) -> bool:
        """
        Convergence criterium for Q / V Evaluation: When x% of state-action pairs are below tolerance value qApproximation
        is converged.
        :param old: dict qApproximation of state-action-pairs before iteration
        :param new: dict qApproximation of state-action-pairs after iteration
        :return: bool
        """
        # TODO: Convergence does not work -> endless loop. Check this
        result = []
        keys = list(old.keys())
        if self.__numberOfIterations == self.__maxIteration:
            return True
        for key in keys:
            if key not in new:
                result.append(False)
            elif np.abs(old[key] - new[key]) > self.tol:
                result.append(False)
            else:
                result.append(True)
        self.__numberOfIterations += 1  # TODO: is this right?
        return self.__checkPercentageOfTrue(result)

    def getConverged(self, old: dict, new: dict) -> bool:
        return self.__evalConverged(old, new)

    def __checkPercentageOfTrue(self, result) -> bool:
        true_count = sum(result)
        total_count = len(result)
        if total_count == 0:
            return False
        true_percentage = (true_count / total_count) * 100
        return true_percentage >= self.percentage

    def policyConverged(self, count) -> bool:
        """
        CONVERGENCE Criterium?
        :param old:
        :param new:
        :return:
        """
        # TODO: implement right convergence criterium
        if count < self.__maxIteration:
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
                self.__visitationsForV.setdefault(player_as_tuple, 0)

            state_action_pairs = [(tuple(self.pathUntilTermination[i]), self.actionsUntilTermination[i])
                                  for i in range(len(self.pathUntilTermination) - 1)]
            state_action_pairs.append((tuple(self.pathUntilTermination[-1]), None))  # Add last state with no action
            self.__stateActionPairs = state_action_pairs
            for sap in state_action_pairs:  # Add state action pairs to qApproximation and visitationsForQ for Q Approx
                self.qApproximation.setdefault(sap, 0)
                self.__visitationsForQ.setdefault(sap, 0)

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
            self.__visitationsForV[tuple(state)] += 1
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
            self.__visitationsForQ[(tuple(state), action)] += 1
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
                actions.remove(action) if not self.env.moveTest(action, None) else None
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
            self.__actionPlayed = action_played
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
            reward += self.__gamma ** (t - timeIndex) * self.env.rolloutReward(state)
        return reward

    def rolloutRewardToSampleQ(self, timeIndex: int) -> float:
        """
        Roll out reward for given time index from given timepoint using discount factor gamma.
        Attention: reward does not depend on action, hence rollout does not consider action played
        :param timeIndex: int
        :return: float
        """
        reward = 0
        for t in range(timeIndex + 1, len(self.__stateActionPairs)):
            state = self.__stateActionPairs[t][0]
            reward += self.__gamma ** (t - timeIndex) * self.env.rolloutReward(state)
        return reward

    def policyEvaluationForV(self) -> None:
        """
        Perform first visit monte carlo evaluation of given policy for value function.
        :return: None
        """
        self.numberIterations = 0
        v_old = {}
        v_new = {}
        while not self.__evalConverged(v_old, v_new):
            v_old = self.valueApproximation.copy()
            self.generateSamplePaths()
            self.addSamplePathToMetricDicts()
            for t in range(len(self.pathUntilTermination)):
                state = self.pathUntilTermination[t]
                if state not in self.pathUntilTermination[0:t]:
                    # Roll out rewards:
                    state_as_tuple = tuple(state)
                    v = self.env.rolloutReward(state) + self.rolloutRewardtoSampleV(t)
                    self.valueApproximation[state_as_tuple] = (v / (self.__visitationsForV[state_as_tuple] + 1)) + \
                                                              (self.__visitationsForV[state_as_tuple] / (
                                                                      self.__visitationsForV[state_as_tuple] + 1)) * \
                                                              self.valueApproximation[state_as_tuple]
                    self.countUpState(state)
            v_new = self.valueApproximation.copy()  # ?

    def policyEvaluationOfQ(self) -> None:
        """
        Perform first visit monte carlo evaluation of given policy for action value function.
        :return: None
        """
        q_old = {}
        q_new = {}
        while not self.__evalConverged(q_old, q_new):
            q_old = self.qApproximation.copy()
            self.generateSamplePaths()
            self.addSamplePathToMetricDicts()
            for t in range(len(self.__stateActionPairs)):
                sap = self.__stateActionPairs[t]
                if sap not in self.__stateActionPairs[0:t]:
                    q = self.env.rolloutReward(sap[0]) + self.rolloutRewardtoSampleV(t)
                    self.qApproximation[sap] = (q / (self.__visitationsForQ[sap] + 1)) + \
                                               (self.__visitationsForQ[sap] / (self.__visitationsForQ[sap] + 1)) * \
                                               self.qApproximation[sap]
                    self.countUpStateActionPair(sap[0], sap[1])
            q_new = self.qApproximation.copy()

    def EvaluationAndIteration(self) -> None:
        """
        Perform first visit monte carlo iteration for Q value.
        :return: None
        """
        self.numberIterations = 0

        while not self.policyConverged(self.numberIterations):
            if self.validatePolicy():
                self.policyEvaluationOfQ()
                self.performPolicyIterationStep()
                self.numberIterations += 1
            else:
                raise Exception("Policy is not valid for all states")

    def getCurrentPolicy(self) -> dict:
        return self.__currentPolicy

    def setCurrentPolicy(self, policy: dict) -> None:
        self.__currentPolicy = policy

    def performPolicyIterationStep(self) -> None:
        """
        Perform one step of policy iteration.
        :return: None
        """
        # TODO: testing for this method
        self.__currentPolicy = self.__policyWrapper().copy()
        pass

    def validatePolicy(self) -> bool:
        """
        Check for current policy for each state action pair if action is valid.
        :return: If policy is valid for each state return True, if one state has invalid action, return False.
        """
        if self.__currentPolicy == {}:
            return True
        states = list(self.__currentPolicy.keys())
        for state in states:
            action = self.__currentPolicy[state]
            if action is not None:
                if not self.env.moveTest(action, state):
                    return False
        return True

    def vEvalConverged(self, numberIterations):
        if numberIterations < self.__maxIteration:
            return False
        else:
            return True
        pass

    def visualizeGrid(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.env.getPosition() == [x, y]:
                    print('P', end='')  # P represents the player
                elif self.env.goal == [x, y]:
                    print('G', end='')  # G represents the goal
                elif [x, y] in self.env.cliff:
                    print('C', end='')  # C represents the cliff
                else:
                    print('.', end='')  # . represents an empty space
            print()  # print a newline at the end of each row

    def visualizeQApproximation(self):
        for y in range(self.height):
            for x in range(self.width):
                state = (x, y)
                for action in [1, 2, 3, 4]:  # assuming actions are represented by these numbers
                    state_action = (state, action)
                    if state_action in self.qApproximation:
                        print(f'Q[{state}, {action}]: {self.qApproximation[state_action]} {self.env.moveTest(action, None)}')
                    else:
                        print(f'Q[{state}, {action}]: No value {self.env.moveTest(action, None)}')
