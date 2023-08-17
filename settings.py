from utils import *
import math
import pygame

DEFAULT_BOARD_PRESET_PATH = "Presets/default.txt"
BOARD_HEIGHT = 8
BOARD_WIDTH = 8


class COLORS(ChessEnum):
    WHITE = 'white'
    BLACK = 'black'

class PIECES(ChessEnum):
    ROOK = {
           'str_rep' : 'r',
           'asset'   : {
                       COLORS.WHITE : pygame.image.load("./Assets/Chess_tile_rd.png"),
                       COLORS.BLACK : pygame.image.load("./Assets/Chess_tile_rl.png"),
                       },
           'value'   : 5,
           }
    KNIGHT = {
           'str_rep' : 'n',
           'asset'   : {
                       COLORS.WHITE : pygame.image.load("./Assets/Chess_tile_nd.png"),
                       COLORS.BLACK : pygame.image.load("./Assets/Chess_tile_nl.png"),
                       },
           'value'   : 3,
           }
    BISHOP = {
           'str_rep' : 'b',
           'asset'   : {
                       COLORS.WHITE : pygame.image.load("./Assets/Chess_tile_bd.png"),
                       COLORS.BLACK : pygame.image.load("./Assets/Chess_tile_bl.png"),
                       },
           'value'   : 3,
           }
    QUEEN = {
           'str_rep' : 'q',
           'asset'   : {
                       COLORS.WHITE : pygame.image.load("./Assets/Chess_tile_qd.png"),
                       COLORS.BLACK : pygame.image.load("./Assets/Chess_tile_ql.png"),
                       },
           'value'   : 9,
           }
    KING = {
           'str_rep' : 'k',
           'asset'   : {
                       COLORS.WHITE : pygame.image.load("./Assets/Chess_tile_kd.png"),
                       COLORS.BLACK : pygame.image.load("./Assets/Chess_tile_kl.png"),
                       },
           'value'   : math.inf,
           }
    PAWN = {
           'str_rep' : 'p',
           'asset'   : {
                       COLORS.WHITE : pygame.image.load("./Assets/Chess_tile_pd.png"),
                       COLORS.BLACK : pygame.image.load("./Assets/Chess_tile_pl.png"),
                       },
           'value'   : 1,
           }
    BLANK = {
           'str_rep' : '-',
           'asset'   : pygame.image.load("./Assets/Blank.png")
           }


