from behave import *
from GeneralGames.src.Environments import Environments

use_step_matcher("re")


@given("Gridworld is initialized with dimensions")
def step_impl(context):
    """
    :type arg0: str
    :type arg1: str
    :type context: behave.runner.Context
    """
    context.gridworld = Environments.Gridworld(3, 1, (3, 1))


@step("agent starts at origin")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.gridworld.setStartingPoint((0, 0))


@step("player is moved according to right right right up manually")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.gridworld.moveRestricted(4)
    context.gridworld.moveRestricted(4)
    context.gridworld.moveRestricted(4)
    context.gridworld.moveRestricted(3)


@then("player is at goal and in terminal state")
def step_impl(context):
    """
    :param arg0:
    :type context: behave.runner.Context
    """
    assert context.gridworld.getPosition() == [3, 1], f"Player is not in terminal state (at goal)"
    assert context.gridworld.isTerminal(), "Player is not in terminal state (goal should always be labeled as terminal)"
