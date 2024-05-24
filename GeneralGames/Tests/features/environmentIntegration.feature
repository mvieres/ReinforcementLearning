Feature: Verfiy movement of player in grid
  """
  Grid of dimesnion means we have one row and three colums
  -> first number indicates x axis
  -> second number indicates y axis
  Implementation count starts at 0
  """
  Scenario: Asymmetric grid and player is moved by hand
    Given Gridworld is initialized with dimensions <(3, 1)> and goal <(3, 1)>
    And agent starts at <(0, 0)>
    And player is moved according to right right right up manually
    Then player is at (1, 3) and is in terminal state
    