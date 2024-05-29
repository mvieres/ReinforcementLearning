from behave import *

from GeneralGames.Environments import Environments
from GeneralGames.Algorithms import PolicyIteration
from GeneralGames.Algorithms import FirstVisitMonteCarlo

use_step_matcher("re")


@given("Q-values with problematic actions")
def someArbitraryPolicy(self):
    self.qValues = {
        ((0, 0), 1): 4,
        ((0, 0), 2): 3,
        ((0, 0), 3): 2,
        ((0, 0), 4): 4,
        ((0, 1), 1): 1,
        ((0, 1), 2): 4,
        ((0, 1), 3): 3,
        ((0, 1), 4): 2,
        ((1, 0), 1): 4,
        ((1, 0), 2): 3,
        ((1, 0), 3): 2,
        ((1, 0), 4): 1
    }


@given("firstvisitmontecarlo instance")
def initFirstVisitMonteCarlo(context):
    context.mcpe = FirstVisitMonteCarlo.MonteCarloPolicyEvaluation(0.1, 0.1, 1, 1, (1, 1))


@when("greedy policy iteration is performed")
def performPolicyImprovementInGridworld(context):
    context.mcpe.setPolicy("greedy")
    context.mcpe.performPolicyIterationStep()
    pass

@then("valid policy is obtained")
def testifplolicyisvalid(context):
    assert context.mcpe.validatePolicy()
