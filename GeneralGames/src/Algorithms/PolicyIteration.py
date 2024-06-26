import random as rand
import numpy as np


class PolicyIteration:

    def __init__(self):
        pass

    def transformQValuesDict(self, d: dict) -> dict:
        """

        :param d:
        :return: dict with key: state, values: list with [(action1, rewards), (action2, reward),...]
        """
        keys = list(d.keys())
        return_dict = {}
        for i in range(len(keys)):
            state = keys[i][0]
            action = keys[i][1]
            if state not in list(return_dict.keys()):
                return_dict[state] = [(action, d[(state, action)])]
            else:
                return_dict[state].append((action, d[(state, action)]))
        return return_dict

    def greedy(self, d: dict) -> dict:
        """
        Performs greedy policy improvement based on the Q-Values
        :param d:
        :return:
        """
        transformed_dict = self.transformQValuesDict(d)
        res = {}
        for state in list(transformed_dict.keys()):
            actionRewardPair = transformed_dict[state]
            res[state] = actionRewardPair[np.argmax([actionRewardPair[_][1] for _ in range(len(actionRewardPair))])][0]
        return res

    def epsilonGreedy(self, d: dict, epsilon: float) -> dict:
        """
        Performs epsilon greedy policy improvement based on the "random" factor epsilon. A random action is chosen if
        uniform(0,1) < epsilon.
        :param d: dict with key: (state, action), values: rewards
        :param epsilon: Probability to choose a random action instead of the greedy one
        :return: dict with key: state, values: action
        """
        transformed_dict = self.transformQValuesDict(d)
        res = {}
        for state in list(transformed_dict.keys()):
            actionRewardPair = transformed_dict[state]
            if rand.random() < epsilon:
                res[state] = rand.choice([actionRewardPair[_][0] for _ in range(len(actionRewardPair))])
            else:
                res[state] = actionRewardPair[np.argmax([actionRewardPair[_][1] for _ in range(len(actionRewardPair))])][0]
        return res
