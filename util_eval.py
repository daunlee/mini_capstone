# Lab 2: Games (Connect-4, Roomba Race)
# Name(s): Daun Lee, Tara Yu
# Email(s): daulee20@bergen.org, erjyu20@bergen.org

from connectfour_gamestate import ConnectFourGameState
from tictactoe_gamestate import TicTacToeGameState
from nim_gamestate import NimGameState
from roomba_gamestate import RoombaRaceGameState
"""
In order to use any of the search methods in lab2_algorithms.py
you'll need define some utility functions and heuristic evaluation functions.

A few have been provided for you, and you can create as many additional ones as
you like (add to the game specific dict to show them on the GUI)

You MUST implement the following:
Part 1:
    basic_endgame_utility
    faster_endgame_utility
    win_paths_eval_tictactoe
Part 2:
    weighted_chains_eval_connectfour
Part 3:
    aggressive_eval_roomba
    defensive_eval_roomba

You MAY wish to implement the following to stretch your creativity:
    advanced_heuristic_eval_connectfour
    advanced_heuristic_eval_roomba

Some useful built-in python methods:
    any(list-like) - returns if at least one True
    all(list-like) - returns if all are True
    sum(list-like) - returns sum of all (??)
    listobj.count(item) - returns count of items in list
"""

### Part 1: Basic Utility Functions, TicTacToe #########################################

## General purpose evaluation functions: ###########

def basic_endgame_utility(state, maximizer_player_num):
    """ Given an endgame state and the player number of the "maximizer",
    returns utility 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie.
    """
    ## TODO
    winner_player_num = state.endgame_winner();
    if (winner_player_num == maximizer_player_num):
        return 1000
    elif (winner_player_num == 0):
        return 0
    else:
        return -1000

def faster_endgame_utility(state, maximizer_player_num):
    """ Given an endgame state and the player number of the "maximizer",
    returns 0 in case of a tie, or a utility with abs(score) >= 1000,
    returning larger absolute scores for winning/losing sooner.
    This incentivizes winning more quickly, and losing later.
    """
    ## TODO
    winner_player_num = state.endgame_winner();
    if (winner_player_num == maximizer_player_num):
        return (2000 - state.get_path_length())
    elif (winner_player_num == 0):
        return 0
    else:
        return (-2000 + state.get_path_length())

def always_zero(state, maximizer_player_num):
    """ Always returns zero.
    Works as a dummy heuristic evaluation function for any situation.
    Truly useful heuristic evaluation functions must almost always be game-specific!
    """
    return 0


## Nim specific evaluation functions: ###########

def empty_rows_eval_nim(state, maximizer_player_num):
    """ Given a non-endgame NimGameState, estimate the value
    (expected utility) of the state from maximizer_player_num's view.

    Return the fraction of rows that are empty. The more empty rows, the better.
    This is not a zero-sum evaluation - both max and min get the same est. utility.
    Still, this can be helpful because usually forcing rows to empty is good.
    """
    return [state.get_stones_in_pile(p) for p in range(state.get_num_piles())].count(0) / state.get_num_piles()

nim_functions = {
    "endgame_util_fn_dict" : {"basic": basic_endgame_utility,
                         "faster": faster_endgame_utility},

    "heuristic_eval_fn_dict" : {"zero": always_zero,
                                "empty rows": empty_rows_eval_nim}
}


## TicTacToe specific evaluation functions: ###########

## Edges are valued least, center valued highest.
space_values_tictactoe = {  (0,0):20, (0,1):10, (0,2):20,
                            (1,0):10, (1,1):30, (1,2):10,
                            (2,0):20, (2,1):10, (2,2):20}

def space_values_eval_tictactoe(state, maximizer_player_num):
    """ Given a non-endgame TicTacToeGameState, estimate the value
    (expected utility) of the state from maximizer_player_num's view.

    Return a linearly weighted sum of the "value" of each piece's position.
    Maximizer's pieces are + value, Minimizer's pieces are - value.
    """
    eval_score = 0
    for r in range(TicTacToeGameState.num_rows):
        for c in range(TicTacToeGameState.num_cols):
            piece = state.board_array[r][c]
            if piece == 0:
                continue
            elif piece == maximizer_player_num:
                eval_score += space_values_tictactoe[(r,c)]
            else:
                eval_score -= space_values_tictactoe[(r,c)]
    return eval_score

def win_paths_eval_tictactoe(state, maximizer_player_num):
    """ Given a non-endgame TicTacToeGameState, estimate the value
    (expected utility) of the state from maximizer_player_num's view.

    Return the difference in the number of possible winning paths for
    each player. More precisely:
    Return E(n) = M(n) - O(n)
    where M(n) is the total of Maximizer's possible winning lines
    O(n) is the total of Minimizer's possible winning lines.
    """

    max_poss_winpaths = 0
    min_poss_winpaths = 0

    if (maximizer_player_num == 2):
        poss_path = True
        for row in range(3):
            for col in range(3):
                if (state.get_piece_at(row, col) == 1):
                    poss_path = False

            if poss_path:
                max_poss_winpaths += 1
            poss_path = True

        poss_path = True
        for col in range(3):
            for row in range(3):
                if (state.get_piece_at(row, col) == 1):
                    poss_path = False

            if poss_path:
                max_poss_winpaths += 1
            poss_path = True

        #left to right diagonal
        poss_path = True
        for pos in range(3):
            if (state.get_piece_at(pos, pos) == 1):
                poss_path = False
        if poss_path:
            max_poss_winpaths += 1
        poss_path = True

        #right to left diagonal
        poss_path = True
        if (state.get_piece_at(0, 2) == 1 or state.get_piece_at(1, 1) == 1 or state.get_piece_at(2, 0) == 1):
            poss_path = False
        if poss_path:
            max_poss_winpaths += 1
        poss_path = True

        #calculating min possible paths
        poss_path = True
        for row in range(3):
            for col in range(3):
                if (state.get_piece_at(row, col) == 2):
                    poss_path = False

            if poss_path:
                min_poss_winpaths += 1
            poss_path = True

        poss_path = True
        for col in range(3):
            for row in range(3):
                if (state.get_piece_at(row, col) == 2):
                    poss_path = False

            if poss_path:
                min_poss_winpaths += 1
            poss_path = True

        #left to right diagonal
        poss_path = True
        for pos in range(3):
            if (state.get_piece_at(pos, pos) == 2):
                poss_path = False
        if poss_path:
            min_poss_winpaths += 1
        poss_path = True

        #right to left diagonal
        poss_path = True
        if (state.get_piece_at(0, 2) == 2 or state.get_piece_at(1, 1) == 2 or state.get_piece_at(2, 0) == 2):
            poss_path = False
        if poss_path:
            min_poss_winpaths += 1
        poss_path = True

    else:
        poss_path = True
        for row in range(3):
            for col in range(3):
                if (state.get_piece_at(row, col) == 2):
                    poss_path = False

            if poss_path:
                max_poss_winpaths += 1
            poss_path = True

        poss_path = True
        for col in range(3):
            for row in range(3):
                if (state.get_piece_at(row, col) == 2):
                    poss_path = False

            if poss_path:
                max_poss_winpaths += 1
            poss_path = True

        #left to right diagonal
        poss_path = True
        for pos in range(3):
            if (state.get_piece_at(pos, pos) == 2):
                poss_path = False
        if poss_path:
            max_poss_winpaths += 1
        poss_path = True

        #right to left diagonal
        poss_path = True
        if (state.get_piece_at(0, 2) == 2 or state.get_piece_at(1, 1) == 2 or state.get_piece_at(2, 0) == 2):
            poss_path = False
        if poss_path:
            max_poss_winpaths += 1
        poss_path = True

        # calculatin min paths
        poss_path = True
        for row in range(3):
            for col in range(3):
                if (state.get_piece_at(row, col) == 1):
                    poss_path = False

            if poss_path:
                min_poss_winpaths += 1
            poss_path = True

        poss_path = True
        for col in range(3):
            for row in range(3):
                if (state.get_piece_at(row, col) == 1):
                    poss_path = False

            if poss_path:
                min_poss_winpaths += 1
            poss_path = True

        #left to right diagonal
        poss_path = True
        for pos in range(3):
            if (state.get_piece_at(pos, pos) == 1):
                poss_path = False
        if poss_path:
            min_poss_winpaths += 1
        poss_path = True

        #right to left diagonal
        poss_path = True
        if (state.get_piece_at(0, 2) == 1 or state.get_piece_at(1, 1) == 1 or state.get_piece_at(2, 0) == 1):
            poss_path = False
        if poss_path:
            min_poss_winpaths += 1
        poss_path = True

    return max_poss_winpaths - min_poss_winpaths

tictactoe_functions = {
    "endgame_util_fn_dict" : {"basic": basic_endgame_utility,
                         "faster": faster_endgame_utility},

    "heuristic_eval_fn_dict" : {"zero": always_zero,
                                "space values": space_values_eval_tictactoe,
                                "win paths": win_paths_eval_tictactoe}
}

### Part 2 - Implement Connect Four ################################################

## Connect-four specific evaluation functions: ###########

def weighted_chains_eval_connectfour(state, maximizer_player_num):
    """
    Given a non-endgame ConnectFourGameState, estimate the value
    (expected utility) of the state
    from maximizer_player_num's view.

    Utilizes the number of piece chains found for both players and makes a weighted
    sum to estimate value.
    """
    sum = 0
    for chain_num in range(1, 5):
        sum += state.get_num_chains(chain_num, maximizer_player_num) * (chain_num/10)

    return sum

def advanced_heuristic_eval_connectfour(state, maximizer_player_num):
    """
    Given a non-endgame ConnectFourGameState, estimate the value
    (expected utility) of the state
    from maximizer_player_num's view.

    OPTIONAL
    """
    raise NotImplementedError
    return 0

connectfour_functions = {
    "endgame_util_fn_dict" : {"basic": basic_endgame_utility,
                            "faster": faster_endgame_utility},

    "heuristic_eval_fn_dict" : {"zero": always_zero,
                              "chains": weighted_chains_eval_connectfour,
                              "advanced": advanced_heuristic_eval_connectfour}
}

### Part 3 - Emergent Behaviours in Roomba Race ################################################

## Roomba Race specific evaluation functions: ###########

def aggressive_eval_roomba(state, maximizer_player_num):
    """
    Given a non-endgame RoombaRaceGameState, estimate the value
    (expected utility) of the state
    from maximizer_player_num's view.

    The closer to the opponent, the better.
    """
    raise NotImplementedError
    return 0

def defensive_eval_roomba(state, maximizer_player_num):
    """ Given a non-endgame RoombaRaceGameState, estimate the value
    (expected utility) of the state
    from maximizer_player_num's view.

    The safer, the better.
    """
    raise NotImplementedError
    return 0

def advanced_heuristic_eval_roomba(state, maximizer_player_num):
    """
    Given a non-endgame RoombaRaceGameState, estimate the value
    (expected utility) of the state
    from maximizer_player_num's view.

    OPTIONAL
    """
    raise NotImplementedError
    return 0

# DO THIS
def checkers_heuristic_eval_diff(state, maximizer_player_num):
    return True


roomba_functions = {
    "endgame_util_fn_dict" : {"basic": basic_endgame_utility,
                         "faster": faster_endgame_utility},

    "heuristic_eval_fn_dict" : {"zero": always_zero,
                                "aggressive": aggressive_eval_roomba,
                                "defensive": defensive_eval_roomba,
                                "advanced" : advanced_heuristic_eval_roomba}
}

checkerboard_functions = {
    "endgame_util_fn_dict" : {"basic": basic_endgame_utility,
                         "faster": faster_endgame_utility},

    "heuristic_eval_fn_dict" : {"zero": always_zero,
                                }
}


## Dictionary mapping games to their appropriate evaluation functions. Used by the GUIs
all_fn_dicts = { RoombaRaceGameState: roomba_functions,
    ConnectFourGameState: connectfour_functions,
    TicTacToeGameState: tictactoe_functions,
    NimGameState: nim_functions,
    CheckersGameState: checkerboard_functions}
