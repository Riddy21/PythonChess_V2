import unittest
from copy import deepcopy
from board import BoardManager
import sys
from game import Game

class TestBoard(unittest.TestCase):
    def setUp(self):
        pass

    def test_set_board(self):
        board = BoardManager.get_board()
        BoardManager.set_board(board, 'Presets/check.txt')

        file = open('Presets/check.txt', 'r')
        golden = file.read()

        # make sure the file and the object is the same
        self.assertEqual(board.__str__(), golden)

        file.close()

    def test_copyable(self):
        board = BoardManager.get_board_from_file('Presets/check.txt')
        # Test if you can make a deep copy without problems
        new_board = board.copy()
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
