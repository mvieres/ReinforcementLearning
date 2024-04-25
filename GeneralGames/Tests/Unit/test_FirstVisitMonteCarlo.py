import unittest
from GeneralGames.Algorithms.FirstVisitMonteCarlo import MonteCarloPolicyEvaluation


class MyTestCase(unittest.TestCase):

    def testAddToDict(self):
        mcpe = MonteCarloPolicyEvaluation(0.1, 0.1, 3, 3, [3, 3])
        mcpe.setStartingPoint([2, 2])
        mcpe.addSamplePathToMetricDicts()
        mcpe.countUp([2, 2])
        self.assertEqual(1, mcpe.visitations[(2, 2)])
        mcpe.countUp([2, 2])
        self.assertEqual(2, mcpe.visitations[(2, 2)])

    def testGeneratePath(self):
        mcpe = MonteCarloPolicyEvaluation(0.1, 0.1, 3, 3, [3, 3])
        mcpe.setStartingPoint([0, 0])
        mcpe.setMaxIterations(10000)
        mcpe.generateSamplePaths()
        if len(mcpe.pathUntilTermination) == mcpe.maxIteration:
            self.skipTest("Max Iteration was reached")
        else:
            self.assertEqual((3, 3), mcpe.pathUntilTermination[-1])

    def testFirstVisitMonteCarloValueApprox(self):
        mcpe = MonteCarloPolicyEvaluation(0.01, 0.1, 3, 3, [3, 3])
        mcpe.setStartingPoint([0, 0])
        mcpe.setMaxIterations(1000)
        mcpe.env.setRewards({(3, 3): 10, (2, 2): -10})
        mcpe.env.setCliff([2, 2])
        mcpe.firstVisitPolicyEvalV()
        self.assertTrue(10-0.01 <= mcpe.valueApproximation[(3, 3)] <= 10+0.01)

if __name__ == '__main__':
    unittest.main()
