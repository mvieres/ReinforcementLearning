from behave import given, when, then
from GeneralGames.Algorithms import FirstVisitMonteCarlo as algo


@given('Env and FirstVisitMonteCarlo Algorithm is initialized')
def step_given_env_and_algo_initialized(context):
    context.mcpe = algo.MonteCarloPolicyEvaluation(0.1, 0.1, 3, 3, [3, 3])


@when('setStartingPosition is assigned')
def step_when_set_starting_position(context):
    context.mcpe.setStartingPoint([1, 1])


@when('one samplepath is created')
def step_when_sample_path_created(context):
    context.mcpe.generateSamplePaths()


@then('startingpoisiton is not changed')
def step_then_check_starting_position(context):
    assert context.mcpe.env.__startingPoint == [1, 1]
