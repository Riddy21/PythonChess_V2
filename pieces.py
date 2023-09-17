from typing import Any
from collections import defaultdict
import uuid
from settings import *
from rules import Rules

# Abstract Piece Class
class _Piece(object):
    def __init__(self, value, color, str_rep):
        # initiate variables
        self.value = value
        self.color = color
        self.str_rep = str_rep

    def get_moves(self, x, y, board, scan_mode=False):
        raise RuntimeError("Trying to access blank moves")

    def __str__(self):
        str = '\n    color: %s\n' \
              '    str_rep: %s\n' \
              % (self.color, self.str_rep)
        return str


class Pawn(_Piece):
    def __init__(self, color):
        str_rep = PIECES.PAWN.value['str_rep']
        if color == COLORS.WHITE:
            str_rep = str_rep.upper()

        # Makes a piece with set values and images
        super().__init__(PIECES.PAWN.value['value'], color, str_rep)

    # Pawn move set given the location of the piece
    def get_moves(self, x, y, board, scan_mode=False):
        poss_moves = set()

        poss_moves = poss_moves.union(Rules.get_pawn_moves((x, y), board))

        poss_moves = poss_moves.union(Rules.get_enpassante_moves((x, y), board))

        # only do this line if not scanning opponent for check to avoid getting stuck in recursive loop
        if not scan_mode:
            Rules.chk_limit_moves((x, y), board, poss_moves)

        return poss_moves

class Rook(_Piece):
    def __init__(self, color):
        str_rep = PIECES.ROOK.value['str_rep']
        if color == COLORS.WHITE:
            str_rep = str_rep.upper()
        # Makes a piece with set values and images
        super().__init__(PIECES.ROOK.value['value'], color, str_rep)

    # Returns possible moves this piece can make
    def get_moves(self, x, y, board, scan_mode=False):
        poss_moves = set()

        poss_moves = poss_moves.union(Rules.get_orthogonal_moves((x, y), board))

        # only do this line if not scanning opponent for check to avoid getting stuck in recursive loop
        if not scan_mode:
            Rules.chk_limit_moves((x, y), board, poss_moves)

        return poss_moves


class Knight(_Piece):
    def __init__(self, color):
        str_rep = PIECES.KNIGHT.value['str_rep']
        if color == COLORS.WHITE:
            str_rep = str_rep.upper()
        # Makes a piece with set values and images
        super().__init__(PIECES.KNIGHT.value['value'], color, str_rep)

    # Returns possible moves this piece can make
    def get_moves(self, x, y, board, scan_mode=False):
        poss_moves = set()
        poss_moves = poss_moves.union(Rules.get_knight_moves((x, y), board))
        # only do this line if not scanning opponent for check to avoid getting stuck in recursive loop
        if not scan_mode:
            Rules.chk_limit_moves((x, y), board, poss_moves)

        return poss_moves


class Bishop(_Piece):
    def __init__(self, color):
        str_rep = PIECES.BISHOP.value['str_rep']
        if color == COLORS.WHITE:
            str_rep = str_rep.upper()
        # Makes a piece with set values and images
        super().__init__(PIECES.BISHOP.value['value'], color, str_rep)

    def get_moves(self, x, y, board, scan_mode=False):
        poss_moves = set()

        poss_moves = poss_moves.union(Rules.get_diagonal_moves((x, y), board))

        # only do this line if not scanning opponent for check to avoid getting stuck in recursive loop
        if not scan_mode:
            Rules.chk_limit_moves((x, y), board, poss_moves)

        return poss_moves


class Queen(_Piece):
    def __init__(self, color):
        str_rep = PIECES.QUEEN.value['str_rep']
        if color == COLORS.WHITE:
            str_rep = str_rep.upper()

        # Makes a piece with set values and images
        super().__init__(PIECES.QUEEN.value['value'], color, str_rep)

    def get_moves(self, x, y, board, scan_mode=False):
        poss_moves = set()

        poss_moves = poss_moves.union(Rules.get_diagonal_moves((x, y), board))
        poss_moves = poss_moves.union(Rules.get_orthogonal_moves((x, y), board))

        # only do this line if not scanning opponent for check to avoid getting stuck in recursive loop
        if not scan_mode:
            Rules.chk_limit_moves((x, y), board, poss_moves)

        return poss_moves


class King(_Piece):
    def __init__(self, color):
        str_rep = PIECES.KING.value['str_rep']
        if color == COLORS.WHITE:
            str_rep = str_rep.upper()

        # Makes a piece with set values and images
        super().__init__(PIECES.KING.value['value'], color, str_rep)


    def get_moves(self, x, y, board, scan_mode=False):
        poss_moves = set()

        poss_moves = poss_moves.union(Rules.get_diagonal_moves((x, y), board, spread=1))
        poss_moves = poss_moves.union(Rules.get_orthogonal_moves((x, y), board, spread=1))

        poss_moves = poss_moves.union(Rules.get_left_castle_moves((x, y), board))
        poss_moves = poss_moves.union(Rules.get_right_castle_moves((x, y), board))

        # only do this line if not scanning opponent for check to avoid getting stuck in recursive loop
        if not scan_mode:
            Rules.chk_limit_moves((x, y), board, poss_moves)

        return poss_moves

# TODO: Try take out blank piece
class Blank(_Piece):
    def __init__(self, color=None):
        super().__init__(0, None, PIECES.BLANK.value['str_rep'])

class PieceLibrary(object):
    """
    Class the holds a copy of all the pieces
    """
    class PieceLibraryException(Exception):
        """Exception for handling piece creation"""
        pass

    PIECE_MAPPING = {
            PIECES.ROOK : Rook,
            PIECES.KNIGHT : Knight,
            PIECES.BISHOP : Bishop,
            PIECES.QUEEN : Queen,
            PIECES.KING : King,
            PIECES.PAWN : Pawn,
            PIECES.BLANK : Blank,
            }
    COLOR_LIST = COLORS

    LIBRARY = defaultdict(dict)
    for piece, piece_obj in PIECE_MAPPING.items():
        for color in COLOR_LIST:
            LIBRARY[piece][color] = piece_obj(color)

    @classmethod
    def get_piece_and_color_by_str_rep(cls, str_rep):
        """
        Returns the piece and color information based on the string rep
        """
        # Get piece by the PIECES str rep, kind of hacky
        try:
            piece = PIECES.get_by_str_rep(str_rep.lower())
        except KeyError:
            raise cls.PieceLibraryException('Could not find piece with value %s' % str_rep)

        if str_rep.isupper():
            color = cls.COLOR_LIST.WHITE
        else:
            color = cls.COLOR_LIST.BLACK

        return piece, color
        
    @classmethod
    def get_piece_ref(cls, piece, color):
        if piece and color:
            return cls.LIBRARY[piece][color]
        else:
            return None

    @classmethod
    def get_piece_copy(cls, piece, color):
        if piece and color:
            return cls.PIECE_MAPPING[piece](color)
        else:
            return None
