import unittest
from pieces import *

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

class TestPawn(unittest.TestCase):
    def setUp(self):
        self.piece = Pawn('white')

    def test_placeholder(self):
        print("hello world")

if __name__ == '__main__':
    unittest.main()
