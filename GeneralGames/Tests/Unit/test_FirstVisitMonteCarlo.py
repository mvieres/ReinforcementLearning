import unittest
from GeneralGames.Algorithms.FirstVisitMonteCarlo import MonteCarloPolicyEvaluation


class MyTestCase(unittest.TestCase):

    def testAddToDict(self):
        mcpe = MonteCarloPolicyEvaluation(0.1, 0.1, 3, 3, [3, 3])
        mcpe.setStartingPoint([1, 1])
        mcpe.pathUntilTermination = [(1, 1), (1, 2), (2, 2), (3, 2)]
        mcpe.actionsUntilTermination = [3, 4, 4]
        mcpe.addSamplePathToMetricDicts()
        target_dict_q_approx = {((1, 1), 3): 0, ((1, 2), 4): 0, ((2, 2), 4): 0, ((3, 2), None): 0}
        self.assertEqual(target_dict_q_approx, mcpe.qApproximation)

    def testCountVisits(self):
        mcpe = MonteCarloPolicyEvaluation(0.1, 0.1, 3, 3, [3, 3])
        mcpe.setStartingPoint([1, 1])
        mcpe.pathUntilTermination = [(1, 1), (1, 2), (2, 2), (3, 2)]
        mcpe.actionsUntilTermination = [3, 4, 4]
        mcpe.addSamplePathToMetricDicts()
        mcpe.countUpStateActionPair([1, 1], 3)
        self.assertEqual(1, mcpe.visitationsForQ[((1, 1), 3)])
        mcpe.countUpState([1, 2])
        self.assertEqual(1, mcpe.visitationsForV[(1, 2)])

    def testGeneratePath(self):
        mcpe = MonteCarloPolicyEvaluation(0.1, 0.1, 3, 3, [3, 3])
        mcpe.setStartingPoint([0, 0])
        mcpe.setMaxIterations(1000)
        mcpe.generateSamplePaths()
        if len(mcpe.pathUntilTermination) == mcpe.maxIteration:
            self.skipTest("Max Iteration was reached")
        else:
            self.assertEqual((3, 3), mcpe.pathUntilTermination[-1])
            self.assertTrue(len(mcpe.pathUntilTermination) > 5, "Samplepath is too short")
            self.assertEqual(len(mcpe.pathUntilTermination)-1, len(mcpe.actionsUntilTermination))
            mcpe.generateSamplePaths()  # Check if pathrollout is valide at the second time
            self.assertTrue(len(mcpe.pathUntilTermination) > 5, "Samplepath is too short")

    def testFirstVisitMonteCarloValueApprox(self):
        mcpe = MonteCarloPolicyEvaluation(0.01, 0.1, 3, 3, [3, 3])
        mcpe.env.setCliff([(1, 1)])
        mcpe.setStartingPoint([0, 0])
        mcpe.setMaxIterations(1000)
        mcpe.env.setRewards({(3, 3): 10, (2, 2): -10})
        mcpe.firstVisitPolicyEvalV()
        self.assertTrue(10-0.01 <= mcpe.valueApproximation[(3, 3)] <= 10+0.01)
        #self.assertTrue(-10-0.01 <= mcpe.valueApproximation[(1, 1)] <= -10+0.01) # TODO: Check this test if cliff point should have value approx of -10

    def testFirstVisitMonteCarloQApprox(self):
        mcpe = MonteCarloPolicyEvaluation(0.01, 0.1, 3, 3, [3, 3])
        mcpe.env.setCliff([(1, 1)])
        mcpe.setStartingPoint([0, 0])
        mcpe.setMaxIterations(1000)
        mcpe.env.setRewards({(3, 3): 10, (2, 2): -10})
        mcpe.firstVisitPolicyEvalQ()
        self.assertTrue(10 - 0.01 <= mcpe.qApproximation[(3, 3)] <= 10 + 0.01)


if __name__ == '__main__':
    unittest.main()
