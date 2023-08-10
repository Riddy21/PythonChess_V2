import unittest
from pieces import *
from settings import *

class TestPieceLibrary(unittest.TestCase):
    def setUp(self):
        self.library = PieceLibrary()

    def test_get_piece_ref(self):
        piece = self.library.get_piece_ref('-')
        self.assertEqual(type(piece), Blank)

        piece = self.library.get_piece_ref('R')
        self.assertEqual(type(piece), Rook)
        self.assertEqual(piece.colour, 'white')

        piece = self.library.get_piece_ref('q')
        self.assertEqual(type(piece), Queen)
        self.assertEqual(piece.colour, 'black')

        with self.assertRaises(PieceLibrary.PieceLibraryException):
            self.library.get_piece_ref('c')

        # These should be the same piece
        piece2 = self.library.get_piece_ref('q')
        self.assertEqual(piece, piece2)

    def test_get_piece_copy(self):
        piece = PieceLibrary.get_piece_copy('n')
        self.assertEqual(Knight, type(piece))
        self.assertEqual('black', piece.colour)

        piece = PieceLibrary.get_piece_copy('r')
        self.assertEqual(Rook, type(piece))
        self.assertEqual('black', piece.colour)

        piece = PieceLibrary.get_piece_copy('Q')
        self.assertEqual(Queen, type(piece))
        self.assertEqual('white', piece.colour)

        piece = PieceLibrary.get_piece_copy('-')
        self.assertEqual(Blank, type(piece))
        self.assertEqual('none', piece.colour)

        with self.assertRaises(PieceLibrary.PieceLibraryException) as context:
            piece = PieceLibrary.get_piece_copy(' ')

        # These should not be the same piece
        piece2 = PieceLibrary.get_piece_copy('q')
        self.assertNotEqual(piece, piece2)

class TestPawn(unittest.TestCase):
    def setUp(self):
        self.piece = Pawn('white')

    def test_placeholder(self):
        pass

if __name__ == '__main__':
    unittest.main()
