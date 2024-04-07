from ..Environments import Environments


class MonteCarloPolicyEvaluation(Environments.Gridworld):

    def __int__(self, initialDistribution=None, maxIteration=1000000):
        self.maxIteration = maxIteration
        self.base_policy = "uniform"
        self.policy = None
        self.initialDistribution = initialDistribution

    def setPolicy(self):
        # TODO: Mapping to use epsilon greedy etc.
        return

    def generateSamplePaths(self):
        n = 0
        while not self.isTerminal():
            # Sample action
            # set new position

            a = 1
        return

    def compute_V_value(self):

        pass
