import unittest
from pieces import _Piece
from settings import *
from board import *
from rules import *
from move import *

class TestRules(unittest.TestCase):
    def test_isin_check(self):
        board = BoardManager.get_board_from_file('Presets/check.txt')
        self.assertTrue(Rules.isin_check((4, 0), board))

    # Test is enpassant
    def test_is_enpassant(self):
        # Valid enpassant
        board = BoardManager.get_board_from_file('Presets/ready_to_enpass.txt')

        # Make move
        Move.full_move((6,1), (6,3), board)
        
        self.assertTrue(Rules.is_enpassant((5, 3), (6, 2), board))
        self.assertFalse(Rules.is_enpassant((5, 3), (5, 2), board))

    # Test is castle
    def test_is_castle(self):
        # Valid Castle
        board = BoardManager.get_board_from_file('Presets/ready_to_castle.txt')

        self.assertFalse(Rules.is_left_castle((4, 7), (6, 7), board))
        self.assertTrue(Rules.is_right_castle((4, 7), (6, 7), board))
        self.assertFalse(Rules.is_left_castle((4, 7), (5, 7), board))

    # Test is pawn promo
    def test_is_pawn_promo(self):
        board = BoardManager.get_board_from_file('Presets/ready_to_promo.txt')

        self.assertTrue(Rules.is_pawn_promo((0, 1), (0, 0), board))
        self.assertFalse(Rules.is_pawn_promo((1, 6), (1, 5), board))
        self.assertFalse(Rules.is_pawn_promo((0, 7), (0, 5), board))
        
    def test_get_pawn_moves(self):
        board = BoardManager.get_board_from_file('Presets/default.txt')

        poss_moves = Rules.get_pawn_moves((0, 1), board)
        self.assertEqual(poss_moves, {(0, 2), (0, 3)})

        poss_moves = Rules.get_pawn_moves((0, 6), board)
        self.assertEqual(poss_moves, {(0, 5), (0, 4)})

        # Make a move then test
        Move.full_move((0, 1), (0,2), board)
        poss_moves = Rules.get_pawn_moves((0, 2), board)
        self.assertEqual(poss_moves, {(0, 3)})

    def test_get_orthogonal_moves(self):
        board = BoardManager.get_board_from_file('Presets/castle_into_check.txt')

        poss_moves = Rules.get_orthogonal_moves((0, 7), board)
        self.assertEqual(poss_moves, {(0, 6), (0, 5), (1, 7), (2, 7), (3, 7)})

        poss_moves = Rules.get_orthogonal_moves((0, 7), board, spread=1)
        self.assertEqual(poss_moves, {(0, 6), (1, 7)})

    def test_get_diagonal_moves(self):
        board = BoardManager.get_board_from_file('Presets/castle_into_check.txt')
        
        poss_moves = Rules.get_diagonal_moves((2, 4), board)
        self.assertEqual(poss_moves, {(1, 5), (4, 6), (5, 1), (4, 2), (0, 6), (0, 2), (3, 3), (1, 3), (3, 5)})

        poss_moves = Rules.get_diagonal_moves((2, 4), board, spread=1)
        self.assertEqual(poss_moves, {(1, 3), (3, 3), (1, 5), (3, 5)})

    def test_get_knight_moves(self):
        board = BoardManager.get_board_from_file('Presets/default.txt')
        poss_moves = Rules.get_knight_moves((1, 0), board)
        self.assertEqual(poss_moves, {(0, 2), (2, 2)})

    def test_chk_limit_moves(self):
        board = BoardManager.get_board_from_file('Presets/check.txt')
        ans = Rules.chk_limit_moves(board, 4, 0, [[5, 1]])
        self.assertEqual(ans, [])

        ans = Rules.chk_limit_moves(board, 6, 1, [[6, 2], [6, 3]])
        self.assertEqual(ans, [[6, 2]])

        BoardManager.set_board(board, 'Presets/castle_into_check.txt')

        ans = Rules.chk_limit_moves(board, 4, 7, [[3, 7], [4, 7]])
        self.assertEqual(ans, [[3, 7]])
