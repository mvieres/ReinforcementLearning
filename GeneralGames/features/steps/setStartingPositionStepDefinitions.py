from GeneralGames.Algorithms import FirstVisitMonteCarlo as algo
from behave import given, when, then


@given(u'Env and FirstVisitMonteCarlo Algorithm is initialized')
def initTestSetup(context):
    context.mcpe = algo.MonteCarloPolicyEvaluation(0.1, 0.1, 3, 3, [3, 3])


@when(u'Gridworld is initialized')
def startingPoint(context):
    context.mcpe.setStartingPoint([1, 1])


@when(u'Sample path is generated')
def generateSamplePath(context):
    context.mcpe.generateSamplePaths()


@then(u'startingpoisiton is not changed')
def checkPosition(context):
    assert context.mcpe.env.startingPoint == [1, 1]
