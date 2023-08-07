from pieces import *

class Board(object):
    """
    Board object keeps a copy of all the pieces on the board,
    As light weight as possible
    """
    # A singleton reference to all pieces
    W_PAWN = Pawn('white')
    W_QUEEN = Queen('white')
    W_BISHOP = Bishop('white')
    W_ROOK = Rook('white')
    W_KNIGHT = Knight('white')
    W_KING = King('white')

    B_PAWN = Pawn('black')
    B_QUEEN = Queen('white')
    B_BISHOP = Bishop('white')
    B_ROOK = Rook('white')
    B_KNIGHT = Knight('white')
    B_KING = King('white')
    def __init__(self, config_file=None):
        """Constructor"""
        if config_file:
            set_board(config_file)


    def set_board(config_file):
        """Sets the board based on config file"""
        # TODO
        pass
