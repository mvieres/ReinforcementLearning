from behave import *
from GeneralGames.Environments import Environments

use_step_matcher("re")


@given("Gridworld is initialized with dimensions <(3, 1)> and goal <(3, 1)>")
def step_impl(context, arg0, arg1):
    """
    :type arg0: str
    :type arg1: str
    :type context: behave.runner.Context
    """
    context.gridworld = Environments.Gridworld(arg0, arg1, (arg0, arg1))


@step("agent starts at <(0, 0)>")
def step_impl(context, arg0, arg1):
    """
    :type context: behave.runner.Context
    """
    context.gridworld.setStartingPoint((arg0, arg1))


@step("player is moved according to right right right up manually")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.gridworld.moveRestricted(Environments.DirectionsGridWorld.RIGHT)
    context.gridworld.moveRestricted(Environments.DirectionsGridWorld.RIGHT)
    context.gridworld.moveRestricted(Environments.DirectionsGridWorld.RIGHT)
    context.gridworld.moveRestricted(Environments.DirectionsGridWorld.UP)


@then("player is at <(arg0, arg1)> and is in terminal state")
def step_impl(context, arg0, arg1):
    """
    :param arg0:
    :type context: behave.runner.Context
    """
    assert context.gridworld.getPosition() == (arg0, arg1), f"Player is not in terminal state (at goal)"
    assert context.gridworld.isTerminal(), "Player is not in terminal state (goal should always be labeled as terminal)"


@given("Gridworld is initialized with dimensions 1x3 and tolerance 0\.01")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given Gridworld is initialized with dimensions 1x3 and tolerance 0.01')


@step("Policy is given by right right right up \(within a dictonary\)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And Policy is given by right right right up (within a dictonary)')


@step("Policy is valid")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And Policy is valid')


@step("player is moved by executing the policy")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And player is moved by executing the policy')
