from behave import given, then

from GeneralGames.Algorithms.PolicyIteration import PolicyIteration


class AlgoTest:

    def __init__(self):
        self.q_value = None

    @given("Dictonary of every state with its resspective Q value")
    def set_q_values(self):
        self.q_value = {
                        [0, 0]: 10,
                        [1, 0]: 20,
                        [3, 0]: 30,
                        [4, 0]: 40,
                        [5, 1]: 50
                        }

    @then("greedy policy returns maximum value")
    def check_greedy(self):
        greedy_action = PolicyIteration.argmaxDict(self.q_value)
        assert greedy_action != [5, 1]
