import unittest
from pieces import *
from settings import *

class TestPieceFactory(unittest.TestCase):
    def test_get_piece(self):
        piece = PieceFactory.get_piece('n')
        self.assertEqual(Knight, type(piece))
        self.assertEqual('black', piece.colour)

        piece = PieceFactory.get_piece('r')
        self.assertEqual(Rook, type(piece))
        self.assertEqual('black', piece.colour)

        piece = PieceFactory.get_piece('Q')
        self.assertEqual(Queen, type(piece))
        self.assertEqual('white', piece.colour)

        piece = PieceFactory.get_piece('-')
        self.assertEqual(Blank, type(piece))
        self.assertEqual('none', piece.colour)

        with self.assertRaises(PieceCreationException) as context:
            piece = PieceFactory.get_piece(' ')

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

        with self.assertRaises(KeyError):
            self.library.get_piece_ref('c')

        # These should be the same piece
        piece2 = self.library.get_piece_ref('q')
        self.assertEqual(piece, piece2)

    def test_get_piece_copy(self):
        piece = self.library.get_piece_copy('-')
        self.assertEqual(type(piece), Blank)

        piece = self.library.get_piece_copy('R')
        self.assertEqual(type(piece), Rook)
        self.assertEqual(piece.colour, 'white')

        piece = self.library.get_piece_copy('q')
        self.assertEqual(type(piece), Queen)
        self.assertEqual(piece.colour, 'black')

        with self.assertRaises(KeyError):
            self.library.get_piece_copy('c')

        # These should not be the same piece
        piece2 = self.library.get_piece_copy('q')
        self.assertNotEqual(piece, piece2)

class TestPawn(unittest.TestCase):
    def setUp(self):
        self.piece = Pawn('white')

    def test_placeholder(self):
        pass

if __name__ == '__main__':
    unittest.main()
