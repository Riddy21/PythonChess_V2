from settings import *
from rules import Rules
class Predict(object):
    @staticmethod
    def get_points(move, board, turn, poss_moves):
        """
        Gets the points of the move based on the captured piece
        """
        # If other player has no possible moves, you've checkmated them
        if not poss_moves and move.move_colour == turn:
            return math.inf

        # If you have no possible moves, you've been checkmated
        elif not poss_moves and move.move_colour != turn:
            return -math.inf

        # If captures a piece, add points
        elif move.move_type == 'capture' and move.move_colour == turn:
            return move.captured.piece.value

        # If lose a piece, subtract points
        elif move.move_type == 'capture' and move.move_colour != turn:
            return -move.captured.piece.value

        else:
            # Else give 0 points
            return 0
