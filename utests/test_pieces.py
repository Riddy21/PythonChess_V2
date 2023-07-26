import unittest
from pieces import *

class TestPieceFactory(unittest.TestCase):
    def setUp(self):
        self.factory = PieceFactory()

    def test_get_piece(self):
        piece = self.factory.get_piece('n')
        self.assertEqual(Knight, type(piece))
        self.assertEqual('black', piece.colour)

class TestPawn(unittest.TestCase):
    def setUp(self):
        self.piece = Pawn('white')

    def test_placeholder(self):
        print("hello world")

if __name__ == '__main__':
    unittest.main()
