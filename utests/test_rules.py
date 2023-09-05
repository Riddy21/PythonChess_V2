import unittest
from pieces import _Piece
from settings import *
from board import *
from rules import *

class TestRules(unittest.TestCase):
    def setUp(self):
        self.board = BoardManager.get_board_from_file('Presets/check.txt')

    def test_isin_check(self):
        self.assertTrue(Rules.isin_check((4, 0), self.board))

    #FIXME: Test is enpassant

    #FIXME: Test is castle

    #FIXME: Test is pawn promo

    def test_chk_limit_moves(self):
        ans = Rules.chk_limit_moves(self.board, 4, 0, [[5, 1]])
        self.assertEqual(ans, [])

        ans = Rules.chk_limit_moves(self.board, 6, 1, [[6, 2], [6, 3]])
        self.assertEqual(ans, [[6, 2]])

        BoardManager.set_board(self.board, 'Presets/castle_into_check.txt')

        ans = Rules.chk_limit_moves(self.board, 4, 7, [[3, 7], [4, 7]])
        self.assertEqual(ans, [[3, 7]])
