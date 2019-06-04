from statenode import StateNode
WALL = '#'
GOAL = 'G'
is_king = False

class GameState(StateNode):
    # A class-level variable (static) representing all the directions
    # the position can move.
    if (is_king):
        NEIGHBORING_STEPS = {(1, 1): "RF", (-1, 1):"LF", (1, -1): "RB", (-1, -1): "LB"}
    else:
        NEIGHBORING_STEPS = {(1, 1): "RF", (-1, 1):"LF"}
    # A class-level variable (static) representing the cost to move onto
    # different types of terrain.

    #PATH_COSTS = {FLOOR: 1, CARPET: 2, WALL: 0, GOAL: 1}

    """
    A 'static' method that reads mazes from text files and returns
    a RoombaRouteState which is an initial state.
    """
    def readFromFile(filename):
        with open(filename, 'r') as file:
            grid = []
            max_r, max_c = [int(x) for x in file.readline().split()]
            init_r, init_c = [int(x) for x in file.readline().split()]
            for i in range(max_r):
                row = list(file.readline().strip()) # or file.readline().split()
                assert (len(row) == max_c)
                grid.append(tuple(row)) # list -> tuple makes it immutable, needed for hashing
            grid = tuple(grid) # grid is a tuple of tuples - a 2d grid!
            return GameState(position = (init_r, init_c),
                                grid = grid,
                                last_action = None,
                                parent = None,
                                path_length = 0,
                                path_cost = 0)

    """
    Creates a RoombaRouteState node.
    Takes:
    position: 2-tuple of current coordinates
    grid: 2-d grid representing features of the maze.
    last_action: string describing the last action taken

    parent: the preceding StateNode along the path taken to reach the state
            (the initial state's parent should be None)
    path_length, the number of actions taken in the path to reach the state
    path_cost (optional), the cost of the entire path to reach the state
    """
    def __init__(self, position, grid, last_action, parent, path_length, path_cost = 0) :

        super().__init__(parent, path_length, path_cost)
        self.my_r, self.my_c = position[0], position[1]
        self.grid = grid
        self.last_action = last_action



    """
    Returns a full feature representation of the environment's current state.
    This should be an immutable type - only primitives, strings, and tuples.
    (no lists or objects).
    If two StateNode objects represent the same state,
    get_features() should return the same for both objects.
    Note, however, that two states with identical features
    may have different paths.
    """
    # Override
    def get_all_features(self) :
        return (self.get_position(), self.get_grid())

    """
    Returns True if a goal state.
    """
    # Override
    def is_goal_state(self) :
        return (self.grid[self.my_r][self.my_c] == 'G')

    """
    Return a string representation of the State
    This gets called when str() is used on an Object.
    """
    # Override
    def __str__(self):
        s = "\n".join(["".join(row) for row in self.grid])
        pos = self.my_r * (self.get_width()+1) + self.my_c
        return s[:pos] + 'X' + s[pos+1:] + "\n"


    """
    Returns a string describing the action taken from the parent StateNode
    that results in transitioning to this StateNode
    along the path taken to reach this state.
    (None if the initial state)
    """
    # Override
    def describe_previous_action(self) :
        return self.last_action

    """
    Generate and return an iterable (e.g. a list) of all possible neighbor
    states (StateNode objects).
    If avoid_backtrack is True, don't include the parent state in the iterable.
    """
    # Override
    def generate_next_states(self) :
        states = []
        for dr, dc in RoombaRouteState.NEIGHBORING_STEPS:
            new_r, new_c = self.my_r + dr, self.my_c + dc
            # Don't use any out-of-bounds moves
            if (new_r < 0) or (new_c < 0) or (new_r >= self.get_height()) or (new_c >= self.get_width()):
                continue
            terrain = self.grid[new_r][new_c]
            # Don't add moves that go into walls
            if terrain == WALL:
                continue

            step_cost = RoombaRouteState.PATH_COSTS[terrain]
            next_state = RoombaRouteState( position = (new_r, new_c),
                                    grid = self.grid,
                                    last_action = RoombaRouteState.NEIGHBORING_STEPS[(dr, dc)],
                                    parent = self,
                                    path_length = self.path_length + 1,
                                    path_cost = self.path_cost + step_cost)


            states.append(next_state)

        return states

    """ Additional accessor methods used the GUI """

    """
    Returns the width (number of cols) of the maze
    """
    def get_width(self):
        return len(self.grid[0])

    """
    Returns the height (number of rows) of the maze
    """
    def get_height(self):
        return len(self.grid)

    """
    Returns a 2d tuple grid of the maze.
    """
    def get_grid(self) :
        return self.grid
    """
    Returns a 2-tuple of the roomba's position (row, col) in the maze
    """
    def get_position(self):
        return self.my_r, self.my_c
