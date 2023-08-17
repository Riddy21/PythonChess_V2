import unittest
from pieces import *
from board import BoardManager
#from new_pieces import *
from settings import *

class TestPieceLibrary(unittest.TestCase):
    def setUp(self):
        self.library = PieceLibrary()

    def test_get_piece_ref(self):
        piece_enum, color = self.library.get_piece_and_color_by_str_rep('-')
        piece = self.library.get_piece_ref(piece_enum, color)
        self.assertEqual(type(piece), Blank)

        piece_enum, color = self.library.get_piece_and_color_by_str_rep('R')
        piece = self.library.get_piece_ref(piece_enum, color)
        self.assertEqual(type(piece), Rook)
        self.assertEqual(piece.colour, 'white')

        piece_enum, color = self.library.get_piece_and_color_by_str_rep('q')
        piece = self.library.get_piece_ref(piece_enum, color)
        self.assertEqual(type(piece), Queen)
        self.assertEqual(piece.colour, 'black')

        with self.assertRaises(PieceLibrary.PieceLibraryException):
            self.library.get_piece_and_color_by_str_rep('c')

        # These should be the same piece
        piece_enum, color = self.library.get_piece_and_color_by_str_rep('q')
        piece2 = self.library.get_piece_ref(piece_enum, color)
        self.assertEqual(piece, piece2)

    def test_get_piece_copy(self):
        piece_enum, color = self.library.get_piece_and_color_by_str_rep('n')
        piece = self.library.get_piece_copy(piece_enum, color)
        self.assertEqual(Knight, type(piece))
        self.assertEqual('black', piece.colour)

        piece_enum, color = self.library.get_piece_and_color_by_str_rep('r')
        piece = self.library.get_piece_copy(piece_enum, color)
        self.assertEqual(Rook, type(piece))
        self.assertEqual('black', piece.colour)

        piece_enum, color = self.library.get_piece_and_color_by_str_rep('Q')
        piece = self.library.get_piece_copy(piece_enum, color)
        self.assertEqual(Queen, type(piece))
        self.assertEqual('white', piece.colour)

        piece_enum, color = self.library.get_piece_and_color_by_str_rep('-')
        piece = self.library.get_piece_copy(piece_enum, color)
        self.assertEqual(Blank, type(piece))
        self.assertEqual('none', piece.colour)

        with self.assertRaises(PieceLibrary.PieceLibraryException) as context:
            self.library.get_piece_and_color_by_str_rep(' ')

        # These should not be the same piece
        piece_enum, color = self.library.get_piece_and_color_by_str_rep('Q')
        piece2 = self.library.get_piece_copy(piece_enum, color)
        self.assertNotEqual(piece, piece2)

class TestPawn(unittest.TestCase):
    def setUp(self):
        self.piece = Pawn(COLORS.WHITE.value)
        self.board = BoardManager.get_board()

    def test_get_moves_start(self):
        BoardManager.set_board(self.board, 'Presets/default.txt')
        moves = self.piece.get_moves(0, 6, self.board, scan_mode=True)

        self.assertEqual([[0, 5], [0, 4]], moves)

if __name__ == '__main__':
    unittest.main()
