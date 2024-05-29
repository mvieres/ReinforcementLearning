Feature: Checking functionality and interaction between gridworld and policy evaluation / improvement within firstvisitmontecarlo class

  Scenario: One-step policy evaluation and improvement of policy

  Scenario: Iteration of only valid policy
    """
      Idea: When improving a policy based on Q-values, the policy should be valid at the end of the iteration step.
      This validation check has to be done within FirstVisitMonteCarlo Class because Policy Iteration class
      has no information about the environment.
      Possible scenarios can occure: Valid action has the highest Q-value -> no problem with plain policy iteration. -> covered by unit test
        Non-valid action has highest Q-value -> firstvisitmontecarlo should not chose this action and instead go with second best solution
      Choose smalles grid, i.e. 1x1
    """
    Given Q-values with problematic actions
    And firstvisitmontecarlo instance
    When greedy policy iteration is performed
    Then valid policy is obtained
