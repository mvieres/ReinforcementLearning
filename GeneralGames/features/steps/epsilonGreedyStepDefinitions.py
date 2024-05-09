from behave import given, then

from GeneralGames.Algorithms.PolicyIteration import PolicyIteration


@given("Dictonary of every state with its resspective Q value")
def set_q_values(context):
    pass

@then("greedy policy returns maximum value")
def check_greedy(context):
    greedy_action = PolicyIteration.__transformQValuesDict(context.q_value)
    assert greedy_action != [5, 1]
