Feature: Verfiy movement of player in grid
  """
  Grid of dimesnion means we have one row and three colums
  -> first number indicates x axis
  -> second number indicates y axis
  Implementation count starts at 0

  Choose width = 3 and height = 1. Goal is at (3, 1). Agent starts at (0,0)
  """
  Scenario: Asymmetric grid and player is moved by hand
    Given Gridworld is initialized with dimensions
    And agent starts at origin
    And player is moved according to right right right up manually
    Then player is at goal and in terminal state
    