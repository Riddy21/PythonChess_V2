import unittest
from copy import deepcopy
from board import BoardManager
import sys
from game import Game
from pieces import Rook, Blank
from settings import *

class TestBoard(unittest.TestCase):
    def setUp(self):
        pass

    def test_set_board(self):
        board = BoardManager.get_board()
        BoardManager.set_board(board, 'Presets/check.txt')

        file = open('Presets/check.txt', 'r')
        golden = file.read()

        # make sure the file and the object is the same
        self.assertEqual(str(board), golden)

        file.close()

    def test_copyable(self):
        board = BoardManager.get_board_from_file('Presets/check.txt')
        # Test if you can make a deep copy without problems
        new_board = BoardManager.copy_board(board)
        # Add a move to one of them
        board[0, 0].num_moves += 1

        # New board
        self.assertFalse(board is new_board)
        # new
        self.assertFalse(board[0, 0] is \
                        new_board[0, 0])
        self.assertTrue(board[0, 0].piece is \
                        new_board[0, 0].piece)
        self.assertNotEqual(board[0, 0].num_moves, \
                        new_board[0, 0].num_moves)

    @unittest.expectedFailure # FIXME: try and make blank pieces empty
    def test_access_empty_piece(self):
        board = BoardManager.get_board_from_file('Presets/default.txt')

        # try calling an empty piece
        self.assertEqual(type(board[0, 3].piece), Blank);

        # Try printing the length of board
        self.assertEqual(len(board), 4*8)

    def test_get_attribute(self):
        board = BoardManager.get_board_from_file('Presets/default.txt')

        self.assertEqual(board[0, 0].piece.color, COLORS.BLACK)
        self.assertEqual(board[0, 0].color, COLORS.BLACK)
        self.assertEqual(type(board[0, 0].piece), Rook )
        self.assertEqual(getattr(board[0, 0], 'str_rep'), 'r' )

        self.assertEqual(board[0, 0].num_moves, 0)
if __name__ == '__main__':
    unittest.main()
