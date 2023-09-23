from settings import *
from rules import Rules
class Predict(object):
    @staticmethod
    def get_points(move, board, turn):
        """
        Gets the points of the move based on the captured piece
        """
        # If captures a piece, add points
        if move.move_type == 'capture' and move.move_colour == turn:
            return move.captured.piece.value

        # If lose a piece, subtract points
        elif move.move_type == 'capture' and move.move_colour != turn:
            return -move.captured.piece.value

        else:
            # Else give 0 points
            return 0
