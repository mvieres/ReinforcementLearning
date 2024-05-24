import unittest

from GeneralGames.Algorithms.FirstVisitMonteCarlo import MonteCarloPolicyEvaluation
from GeneralGames.Algorithms.PolicyIteration import PolicyIteration


class MyTestCase(unittest.TestCase):

    @unittest.skip("Skip this test")
    def testAddToDict(self):
        mcpe = MonteCarloPolicyEvaluation(0.1, 0.1, 3, 3, [3, 3])
        mcpe.setStartingPoint([1, 1])
        mcpe.pathUntilTermination = [(1, 1), (1, 2), (2, 2), (3, 2)]
        mcpe.actionsUntilTermination = [3, 4, 4]
        mcpe.addSamplePathToMetricDicts()
        target_dict_q_approx = {((1, 1), 3): 0, ((1, 2), 4): 0, ((2, 2), 4): 0, ((3, 2), None): 0}
        self.assertEqual(target_dict_q_approx, mcpe.qApproximation)

    @unittest.skip("Skip this test")
    def testCountVisits(self):
        mcpe = MonteCarloPolicyEvaluation(0.1, 0.1, 3, 3, [3, 3])
        mcpe.setStartingPoint([1, 1])
        mcpe.pathUntilTermination = [(1, 1), (1, 2), (2, 2), (3, 2)]
        mcpe.actionsUntilTermination = [3, 4, 4]
        mcpe.addSamplePathToMetricDicts()
        mcpe.countUpStateActionPair([1, 1], 3)
        self.assertEqual(1, mcpe.getVisitationsForQ()[((1, 1), 3)])
        mcpe.countUpState([1, 2])
        self.assertEqual(1, mcpe.getVisitationsForV()[(1, 2)])

    @unittest.skip("Skip this test")
    def testGeneratePath(self):
        mcpe = MonteCarloPolicyEvaluation(0.1, 0.1, 3, 3, [3, 3])
        mcpe.setStartingPoint([0, 0])
        mcpe.setMaxIterations(1000)
        mcpe.generateSamplePaths()
        if len(mcpe.pathUntilTermination) == 1000:
            self.skipTest("Max Iteration was reached")
        else:
            self.assertEqual((3, 3), mcpe.pathUntilTermination[-1])
            self.assertTrue(len(mcpe.pathUntilTermination) > 5, "Samplepath is too short")
            self.assertEqual(len(mcpe.pathUntilTermination) - 1, len(mcpe.actionsUntilTermination))
            mcpe.generateSamplePaths()  # Check if pathrollout is valide at the second time
            self.assertTrue(len(mcpe.pathUntilTermination) > 5, "Samplepath is too short")

    @unittest.skip("Skip this test")
    def testFirstVisitMonteCarloQApprox(self):
        mcpe = MonteCarloPolicyEvaluation(0.01, 0.1, 3, 3, [3, 3])
        mcpe.setMaxIterations(10000)
        mcpe.env.setCliff([(1, 1)])
        mcpe.setStartingPoint([0, 0])
        mcpe.env.setRewards({(3, 3): 10, (1, 1): -10})
        mcpe.policyEvaluationOfQ()
        self.assertEqual(1, 1)
        a = PolicyIteration().greedy(mcpe.qApproximation)
        self.assertEqual(1, 1)

    def testPolicyIteration(self):
        mcpe = MonteCarloPolicyEvaluation(0.01, 0.1, 3, 3, [3, 3])
        mcpe.setMaxIterations(10000)
        mcpe.setPolicy("greedy")
        mcpe.env.setCliff([(1, 1)])
        mcpe.setStartingPoint([0, 0])
        mcpe.env.setRewards({(3, 3): 10, (1, 1): -10})
        mcpe.policyEvaluationOfQ()
        mcpe.performPolicyIterationStep()
        new_policy = mcpe.getCurrentPolicy()
        self.assertIsInstance(new_policy, dict)

    # Put all functional tests here
    def testFirstVisitMonteCarloImprovement(self):
        mcpe = MonteCarloPolicyEvaluation(0.01, 0.1, 3, 3, [3, 3])
        mcpe.setPercentageForConvergenceCriterion(0)  # TODO: Addition with convergence Criterion is not working
        mcpe.setStartingPoint([0, 0])
        mcpe.env.setRewards({(3, 3): 10})
        mcpe.setPolicy("greedy")
        mcpe.EvaluationAndIteration()
        optimal_policy = mcpe.getCurrentPolicy()
        self.assertEqual(optimal_policy[(3, 2)], 3)

    def testFirstVisitMonteCarloImprovementBestPolicy(self):
        mcpe = MonteCarloPolicyEvaluation(0.01, 0.1, 3, 3, [3, 3], maxIteration=100)
        mcpe.setStartingPoint([0, 0])
        mcpe.env.setRewards({(3, 3): 10})
        mcpe.setPolicy("greedy")
        mcpe.EvaluationAndIteration()
        self.assertEqual(mcpe.getCurrentPolicy()[(3, 2)], 3)  # Okay

    def testIteratedPolicyForValidActions(self):
        # TODO: This test is outdated and should be rewritten to a cucumber test
        mcpe = MonteCarloPolicyEvaluation(0.5, 0.1, 1, 1, [1, 1], maxIteration=1000)
        mcpe.setStartingPoint([0, 0])
        mcpe.env.setRewards({(1, 1): 10})
        mcpe.setPolicy("greedy")
        mcpe.EvaluationAndIteration()
        self.assertTrue(mcpe.validatePolicy())  # TODO: Observed wrong policy, check state - action pairs sampling

    def testqApproxVisualization(self):
        mcpe = MonteCarloPolicyEvaluation(0.5, 0.1, 1, 1, [1, 1], maxIteration=1000)
        mcpe.setStartingPoint([0, 0])
        mcpe.env.setRewards({(1, 1): 10})
        mcpe.setPolicy("greedy")
        mcpe.policyEvaluationOfQ()
        mcpe.visualizeQApproximation()

    def testEvalConverged(self):
        mcpe = MonteCarloPolicyEvaluation(0.01, 0.1, 3, 3, [3, 3], maxIteration=1000)
        old  = {
            ((1, 1,), 1): 10,
            ((1, 2), 2): 10,
            ((2, 2), 3): 9.5
        }
        new = {
            ((1, 1,), 1): 10.005,
            ((1, 2), 2): 10.4,
            ((2, 2), 3): 9.501
        }
        mcpe.setPercentageForConvergenceCriterion(50)
        self.assertTrue(mcpe.getConverged(old, new))
        mcpe.setPercentageForConvergenceCriterion(80)
        self.assertFalse(mcpe.getConverged(old, new))

    def testPerformPolicyIterationStep(self):
        mcpe = MonteCarloPolicyEvaluation(0.1, 0.1, 1, 1, [1, 1], maxIteration=1000)
        mcpe.setStartingPoint([0, 0])
        mcpe.env.setRewards({(1, 1): 10})
        mcpe.setPolicy("greedy")
        mcpe.policyEvaluationOfQ()
        mcpe.performPolicyIterationStep()
        self.assertTrue(mcpe.validatePolicy())


if __name__ == '__main__':
    unittest.main()
