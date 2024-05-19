Feature: Testing setStartingPosition for Env / FirstVisitMonteCarlo Algorithm: Finding is that move method updates startingposition

  Scenario: 1
    Given Env and FirstVisitMonteCarlo Algorithm is initialized
    When setStartingPosition is assigned
    And one samplepath is created
    Then startingpoisiton is not changed