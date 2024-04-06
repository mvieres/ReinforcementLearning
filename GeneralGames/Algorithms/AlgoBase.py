import random as rand

import numpy as np


class AlgoBase:

    def __int__(self):
        pass

    @staticmethod
    def argmaxDict(d):
        max_key = None
        max_value = float('-inf')  # Initializing with negative infinity to handle negative values
        for key, value in d.items():
            if value > max_value:
                max_key = key
                max_value = value
        return max_key

    def greedy(self, q_values: dict):
        return self.argmaxDict(q_values)

    def epsilonGreedy(self, q_values: dict, epsilon: float):
        if rand.uniform(0, 1) > epsilon:
            return self.argmaxDict(q_values)
        else:
            return


