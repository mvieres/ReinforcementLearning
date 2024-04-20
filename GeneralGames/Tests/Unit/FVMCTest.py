import unittest
from GeneralGames.Algorithms.FirstVisitMonteCarlo import MonteCarloPolicyEvaluation
from GeneralGames.Environments.Environments import Gridworld


class MyTestCase(unittest.TestCase):

    def testAddToDict(self):
        mcpe = MonteCarloPolicyEvaluation(0.1, 0.1, 3, 3, [3, 3])
        mcpe.setStartingPoint([2, 2])
        mcpe.addToDict()
        mcpe.countUp()
        self.assertEqual(1, mcpe.visitations[(2, 2)])

    def testGeneratePath(self):
        mcpe = MonteCarloPolicyEvaluation(0.1, 0.1, 3, 3, [3, 3])
        mcpe.setStartingPoint([0, 0])
        mcpe.setMaxIterations(10000)
        mcpe.generateSamplePaths()
        if len(mcpe.pathUntilTermination) == mcpe.maxIteration:
            self.skipTest("Max Iteration was reached")
        else:
            self.assertEqual((3, 3), mcpe.pathUntilTermination[-1])


if __name__ == '__main__':
    unittest.main()
