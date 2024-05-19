Feature: Test Policy evaluation and iteration
  Scenario: Without cliff
    Given Gird <[3,3]>, pararameters <parameters> and <greedy> policy are set
    When Policy evaluation and iteration is performed
    Then I should get a policy that solves the gridworld game

  Scenario: With cliff
    Given Gird <gird>, pararameters <parameters> and <policy> policy are set
    And Cliff is added to the grid
    When Policy evaluation and iteration is performed
    Then I should get a policy that solves the gridworld game