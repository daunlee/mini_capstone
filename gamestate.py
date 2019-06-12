from statenode import StateNode
from copy import deepcopy
is_king = False


class GameState(StateNode):
    # A class-level variable (static) representing all the directions
    # the position can move.
    # "RF": right forward; "LF": left forward; "RB": right bottom; "LB": left bottom
    if (is_king):
        NEIGHBORING_STEPS = {(1, 1): "RF", (-1, 1):"LF", (1, -1): "RB", (-1, -1): "LB"}
    else:
        NEIGHBORING_STEPS = {(1, 1): "RF", (-1, 1):"LF"}


    num_rows = 8
    board_str = {'-': "BOARD", 'x': "BLACK", 'o': "WHITE", 'X': "KBLACK", 'O': "KWHITE"}
    positions_black = []
    positions_red = []
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
            # max_r, max_c = [int(x) for x in file.readline().split()]
            # init_r, init_c = [int(x) for x in file.readline().split()]
            first_player = int(file.readline())
            for i in range(GameState.num_rows):
                row = list(file.readline().strip()) # or file.readline().split()
                assert (len(row) == GameState.num_rows)
                grid.append(tuple(row)) # list -> tuple makes it immutable, needed for hashing

                for j in range(GameState.num_rows):
                    if row[j] == 'x' or row[j] == 'X':
                        GameState.positions_black.append([i, j])
                    elif row[j] == 'o' or row[j] == 'O':
                        GameState.positions_red.append([i, j])

            grid = tuple(grid) # grid is a tuple of tuples - a 2d grid!
            return GameState(GameState.positions_black, GameState.positions_red,
                                grid = grid,
                                last_action = None,
                                parent = None,
                                path_length = 0,
                                current_player = first_player)

    """
    Creates a CheckeState node.
    Takes:
    position: 2-tuple of current coordinates
    grid: 2-d grid representing features of the maze.
    last_action: string describing the last action taken

    parent: the preceding StateNode along the path taken to reach the state
            (the initial state's parent should be None)
    path_cost (optional), the cost of the entire path to reach the state
    """
    def __init__(self, positions_black, positions_red, grid, last_action, parent, path_length, current_player) :

        super().__init__(parent, path_length)
        self.positions_black = positions_black
        self.positions_red = positions_red
        self.grid = grid
        self.last_action = last_action
        self.current_player = current_player



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
        if (self.positions_black.length() == 0 or self.positions_red.length() == 0)
            return True

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

    def total_next_black_states(self):
        """ returns a list of possible moves for all black pieces"""
        next_black_states_list = []

        for black in self.positions_black:
            next_black_states_list.append(self.single_next_black_state(black))

        return next_black_states_list

    def total_next_red_states(self):
        """ returns a list of possible moves for all red pieces"""
        next_red_states_list = []

        for red in self.positions_red:
            next_red_states_list.append(self.single_next_red_state(red))

        return next_red_states_list

    def single_next_black_states(self, cur_piece_pos):
        """ returns a list of possible moves for a single black piece"""
        neighboring_states = [(1, -1), (-1,-1)]
        return self.generate_next_states(cur_piece_pos, neighboring_states)

    def single_next_red_states(self, cur_piece_pos):
        """ returns a list of possible moves for a single black piece"""
        neighboring_states = [(1, 1), (-1,1)]
        return self.generate_next_states(cur_piece_pos, neighboring_states)

    def generate_next_states(self, cur_piece_pos, possible_pos):
        BLACK = 1
        RED = 0
        for move_pos in possible_pos:
            # regular moving
            next_state_x = cur_piece_pos[0] + move_pos[0]
            next_state_y = cur_piece_pos[1] + move_pos[1]

            # stops if the move would place the piece out of bounds
            if (next_state_x >= self.get_dimension() or next_state_y >= self.get_dimension()):
                continue

            next_state_pos = (next_state_x, next_state_y)

            # booleans for whether or not there is a piece in the way of moving
            target_is_black = next_state_pos in self.get_position_black()
            target_is_red = next_state_pos in self.get_position_red()

            # if the move is complete and there is nothing in the way
            if (not target_is_black or not target_is_red):
                return next_state_pos

            # there is a piece in the target area, so we can possibly jump
            else:
                # if the piece in the way is the same color as the current player, then don't jump"""
                if ((self.get_current_player() == BLACK and target_is_black) or (self.get_current_player() == RED and target_is_red)):
                    continue

                else:
                    # jump
                    jump_x = next_state_x[0] + move_pos[0]
                    jump_y = next_state_y[1] + move_pos[1]

                    # stops if the next move is going to be out of bounds
                    if (jump_x < 0 or jump_x > self.get_dimension() or jump_y < 0 or jump_y < 0 or jump_y > self.get_dimension()):
                        continue

                    jump_pos = (jump_x, jump_y)
                    jump_is_black = jump_pos in self.get_position_black()
                    jump_is_red = jump_pos in self.get_position_red()

                    if (not jump_is_black or not jump_is_red):
                        return jump_pos

    def generate_next_game_state(self, action):
        BLACK = 1
        RED = 0

        # in this case, action would be the position of where the piece would jump
        newboard = deepcopy(self.grid)
        action_x = action[0]
        action_y = action[1]

        newboard[action_x][action_y] = self.current_player

        # if it is the black
        if self.current_player == 1:
            self.positions_black.append(action)

        else:
            self.positions_red.append(action)

        return GameState(positions_black = self.positions_black,
                         positions_red = self.positions_red,
                         grid = newboard,
                         last_action = action,
                         parent = self,
                         path_length = self.path_length + 1,
                         current_player =  self.current_player % 2 + 1)


    """ Additional accessor methods used the GUI """

    """
    Returns a 2d tuple grid of the maze.
    """

    def get_dimension(self):
        return 8

    def get_grid(self) :
        return self.grid

    def get_position_black(self):
        return self.positions_black

    def get_position_red(self):
        return self.positions_red

    def get_current_player(self):
        return self.current_player
