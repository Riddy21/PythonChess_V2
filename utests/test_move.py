import unittest
from board import *
from move import *

class TestMove(unittest.TestCase):
    def setUp(self):
        self.board = BoardManager.get_board_from_file('Presets/check.txt')

    def compare_boards(self, board1, board2):
        for ((x1, y1), square1), ((x2, y2), square2) in zip(board1.items(), board2.items()):
            self.assertEqual(square1.piece.color, square2.piece.color)
            self.assertEqual(type(square2.piece), type(square1.piece))

    def test_full_move(self):
        # bad move
        with self.assertRaises(Move.MoveError):
            move = Move.full_move((2,2), (0,2), self.board)

        # good move
        move = Move.full_move((6,1), (6,2), self.board)
        golden = BoardManager.get_board_from_file('Presets/check_blocked.txt')
        self.compare_boards(golden, self.board)

    def test_get_all_poss_moves(self):
        poss_moves = Move.get_all_poss_moves(self.board, scan_mode=True)
        golden = {(1, 0): {(0, 2), (2, 2)},
                  (4, 0): {(5, 1)},
                  (6, 0): {(7, 2)},
                  (0, 1): {(0, 2), (0, 3)},
                  (1, 1): {(1, 2), (1, 3)},
                  (2, 1): {(2, 3), (2, 2)},
                  (3, 1): {(3, 2), (3, 3)},
                  (4, 1): {(4, 2), (4, 3)},
                  (6, 1): {(6, 2), (6, 3)},
                  (7, 1): {(7, 2)},
                  (5, 2): {(5, 3), (5, 4)},
                  (7, 3): {(4, 0), (4, 3), (3, 7), (4, 6),
                           (5, 1), (6, 4), (1, 3), (7, 4),
                           (6, 2), (5, 5), (7, 1), (0, 3),
                           (2, 3), (3, 3), (7, 2), (5, 3),
                           (7, 5), (6, 3)},
                  (4, 4): {(4, 2), (4, 3)},
                  (0, 6): {(0, 4), (0, 5)},
                  (1, 6): {(1, 4), (1, 5)},
                  (2, 6): {(2, 4), (2, 5)},
                  (3, 6): {(3, 4), (3, 5)},
                  (5, 6): {(5, 4), (5, 5)},
                  (6, 6): {(6, 4), (6, 5)},
                  (7, 6): {(7, 4), (7, 5)},
                  (1, 7): {(2, 5), (0, 5)},
                  (4, 7): {(3, 7), (4, 6)},
                  (5, 7): {(2, 4), (0, 2), (4, 6), (1, 3), (3, 5)},
                  (6, 7): {(7, 5), (4, 6), (5, 5)}}
        self.assertEqual(poss_moves, golden)

