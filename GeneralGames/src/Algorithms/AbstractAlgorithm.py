import numpy as np


class AbstractAlgorithm:

    def __init__(self, tol, maxIteration = 10000):
        self.tol: float = tol
        self.__maxIteration: int = maxIteration
        self.__numberOfIterations: int = 0
        self.percentage: float = 90.0
        pass

    def policyConverged(self, q_old: dict, q_new: dict) -> bool:
        """
        CONVERGENCE Criterium?
        :param q_new: new dict of qApproximation
        :param q_old: old dict of qApproximation
        :return:
        """
        if q_new is None:
            return False
        for key in q_old.keys():
            if np.abs(q_old[key] - q_new[key]) > self.tol:
                return False
        return True

    def evalConverged(self, old, new) -> bool:
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

    def __checkPercentageOfTrue(self, result) -> bool:
        true_count = sum(result)
        total_count = len(result)
        if total_count == 0:
            return False
        true_percentage = (true_count / total_count) * 100
        return true_percentage >= self.percentage

    def setPercentageForConvergenceCriterion(self, percentage: float) -> None:
        """
        Default is: 90% of state-action pairs have to be below the tolerance value.
        :param percentage: float 1 - 100
        :return: None
        """
        assert 0 <= percentage <= 100
        self.percentage = percentage