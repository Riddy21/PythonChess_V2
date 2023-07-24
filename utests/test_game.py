import unittest
from game import Game

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def tearDown(self):
        self.game.quit()

    def test_set_board(self):
        # Setup the board to the right config
        self.game.set_board('Presets/check.txt')

        file = open('Presets/check.txt')
        golden = ''.join(file.readlines())
        file.close()

        self.assertEqual(str(self.game), golden)

    def test_switch_turn(self):
        # Set the board to check
        self.game.set_board('Presets/check.txt')

        self.assertEqual(self.game.turn, 'white')
        self.game.switch_turn()
        self.assertEqual(self.game.turn, 'black')

if __name__ == '__main__':
    unittest.main()
