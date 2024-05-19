from behave import *

use_step_matcher("re")

# TODO: Implement the following steps
@when("Policy evaluation and iteration is performed")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When Policy evaluation and iteration is performed')


@given("Gird <\[3,3\]>, pararameters <parameters> and <greedy> policy are set")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given Gird <[3,3]>, pararameters <parameters> and <greedy> policy are set')


@then("I should get a policy that solves the gridworld game")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then I should get a policy that solves the gridworld game')


@step("Cliff is added to the grid")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And Cliff is added to the grid')