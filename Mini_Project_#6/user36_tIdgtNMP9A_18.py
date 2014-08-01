"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(90)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    if board.check_win() != None:
        return SCORES[board.check_win()], (-1, -1)
    else:
        lst = []
        for square in board.get_empty_squares():
            temp_board = board.clone()
            row, col = square[0], square[1]
            temp_board.move(row, col, player)
            result = mm_move(temp_board, provided.switch_player(player))
            if result[0] == SCORES[player]:
                return result[0], square
            else:
                lst.append((result[0], square))
        if player == provided.PLAYERX:
            score = max(lst)[0]
            best_move = max(lst)[1]
        else:
            score = min(lst)[0]
            best_move = min(lst)[1]
        return score, best_move
                


def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#import user36_AQLww3W1YBS5oCt as unit_test
#unit_test.test_mm_move(mm_move)

#provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
