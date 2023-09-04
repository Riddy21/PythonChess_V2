import unittest
from pieces import _Piece
from settings import *
from board import *

class TestRules(unittest.TestCase):
    def setUp(self):
        self.piece = _Piece(10, COLORS.BLACK, '5')
        self.board = BoardManager.get_board_from_file('Presets/check.txt')

    def test_chk_limit_moves(self):
        ans = self.piece.chk_limit_moves(self.board, 4, 0, [5, 1])
        self.assertEqual(ans, [])
        print(ans)
