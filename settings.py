from utils import *

DEFAULT_BOARD_PRESET_PATH = "Presets/default.txt"
BOARD_HEIGHT = 8
BOARD_WIDTH = 8

class COLORS(ChessEnum):
    WHITE = 'white'
    BLACK = 'black'

class PIECES(ChessEnum):
    ROOK = 'r'
    KNIGHT = 'n'
    BISHOP = 'b'
    QUEEN = 'q'
    KING = 'k'
    PAWN = 'p'
    BLANK = '-'
