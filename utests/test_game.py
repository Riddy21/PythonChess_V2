import unittest
from game import Game

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def tearDown(self):
        self.game.quit()

    def test_switch_turn(self):
        print(self.game.turn)
        self.game.switch_turn()
        print(self.game.turn)

if __name__ == '__main__':
    unittest.main()
