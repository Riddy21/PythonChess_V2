from pieces import *
from settings import *
from copy import deepcopy

# FIXME: Try and hide Blank objects
class Board(dict):
    """Special dictionary object to contain board items"""
    class Square(object):
        """
        Object representing a tile on the board
        """
        def __init__(self, piece=Blank(), num_moves=0):
            """Constructor"""
            self.piece = piece
            self.num_moves = num_moves
    
        def copy(self):
            if REFERENCE_PIECES:
                return Board.Square(self.piece, self.num_moves)
            else:
                return Board.Square(deepcopy(self.piece), self.num_moves)

        def __getattr__(self, value):
            return self.piece.__getattribute__(value)
    
        def __str__(self):
            return str((self.piece.str_rep, self.num_moves))

    BLANK_SQUARE = Square()
    
    def copy(self):
        """Override the copy method of a dict"""
        new_copy = Board()
        for key, value in self.items():
            new_copy[key] = value.copy()
        return new_copy

    def __str__(self):
        """Print function Override"""
        return BoardManager.get_board_str(self)


# TODO: Make a serialization class to save the board object
class BoardManager(object):
    """
    Board object keeps a copy of all the pieces on the board,
    As light weight as possible
    """
    PIECE_LIBRARY = PieceLibrary()

    @classmethod
    def get_board(cls):
        """Get a new empty board"""
        return Board()

    @classmethod
    def set_board(cls, board, config_file):
        """Sets a board in place"""
        file = open(config_file)
        for row, line in enumerate(file):
            # turn into array
            line = line.replace('\n', '')
            pieces = line.split(' ')
            
            # Get the piece
            for col, piece_str in enumerate(pieces):
                # Do error checking
                if row > BOARD_HEIGHT-1 or col > BOARD_WIDTH-1:
                    raise IOError("Config file %s not in the right format" % config_file)

                piece, color = cls.PIECE_LIBRARY.get_piece_and_color_by_str_rep(piece_str)
                if REFERENCE_PIECES:
                    piece_ref = cls.PIECE_LIBRARY.get_piece_ref(piece, color)
                else:
                    piece_ref = cls.PIECE_LIBRARY.get_piece_copy(piece, color)

                if piece_ref:
                    board[col, row] = Board.Square(piece_ref)

        if row != BOARD_HEIGHT-1 or col != BOARD_WIDTH-1:
            file.close()
            raise IOError("Config file %s not in the right format" % config_file)
        file.close()

    @classmethod
    def get_board_from_file(cls, config_file):
        """Creates a new board object with the setting"""
        board = Board()
        cls.set_board(board, config_file)
        return board

    @staticmethod
    def copy_board(board):
        """Gets a deep copy of the board"""
        return board.copy()

    @staticmethod
    def get_board_str(board):
        """Return string of board"""
        string = ''

        # Add board string reps
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                string += board[x, y].piece.str_rep + ' '
            string = string[:-1] + '\n'
        return string

    @staticmethod
    def get_move_counts_str(board): # pragma: no cover
        """Return a board layout of the num moves"""
        string = ''

        # Add board string reps
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                string += "%01d" % board[x, y].num_moves + ' '
            string = string[:-1] + '\n'
        return string
