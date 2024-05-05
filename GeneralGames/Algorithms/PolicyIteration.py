import random as rand


class PolicyIteration:

    def __int__(self):
        pass

    @staticmethod
    def argmaxDict(d: dict) -> dict:
        """
        Return a dict with the best action for a given state
        :param d:
        :return:
        """
        for state in dict.keys():


        # TODO: Implement this
        pass

    def greedy(self, q_values: dict):
        return self.argmaxDict(q_values)

    def epsilonGreedy(self, q_values: dict, epsilon: float):
        if rand.uniform(0, 1) > epsilon:
            return self.argmaxDict(q_values)
        else:
            return


