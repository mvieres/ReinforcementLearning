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

    def greedy(self, d: dict):
        transformed_dict = self.transformQValuesDict(d)
        res = {}
        for state in list(transformed_dict.keys()):
            b = transformed_dict[state]
            res[state] = b[np.argmax([b[_][1] for _ in range(len(b))])][0]
        return res
