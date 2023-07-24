import unittest
from game import Game

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def tearDown(self):
        self.game.quit()

    def test_set_board(self):
        self.game.set_board('Presets/check.txt')
        golden = ''.join(open('Presets/check.txt').readlines())
        self.assertEqual(str(self.game), golden)

    def test_switch_turn(self):
        self.assertEqual(self.game.turn, 'white')
        self.game.switch_turn()
        self.assertEqual(self.game.turn, 'black')

if __name__ == '__main__':
    unittest.main()
