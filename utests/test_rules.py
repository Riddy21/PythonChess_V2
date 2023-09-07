import unittest
from pieces import _Piece
from settings import *
from board import *
from rules import *
from game import Game

class TestRules(unittest.TestCase):
    def test_isin_check(self):
        board = BoardManager.get_board_from_file('Presets/check.txt')
        self.assertTrue(Rules.isin_check((4, 0), board))

    #FIXME: Test is enpassant
    def test_is_enpassant(self):

        # Valid enpassant
        game = Game()
        game.set_turn(COLORS.BLACK)

        game.full_move(4, 1, 4, 3)
        self.assertTrue(Rules.is_enpassant((5, 3), (4, 2), game.board))
        self.assertFalse(Rules.is_enpassant((5, 3), (5, 2), game.board))

    #FIXME: Test is castle

    #FIXME: Test is pawn promo

    def test_chk_limit_moves(self):
        board = BoardManager.get_board_from_file('Presets/check.txt')
        ans = Rules.chk_limit_moves(board, 4, 0, [[5, 1]])
        self.assertEqual(ans, [])

        ans = Rules.chk_limit_moves(board, 6, 1, [[6, 2], [6, 3]])
        self.assertEqual(ans, [[6, 2]])

        BoardManager.set_board(board, 'Presets/castle_into_check.txt')

        ans = Rules.chk_limit_moves(board, 4, 7, [[3, 7], [4, 7]])
        self.assertEqual(ans, [[3, 7]])
