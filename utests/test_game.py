import unittest
from game import Game
from pieces import Queen, Pawn

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def tearDown(self):
        self.game.quit()

    def compare_boards(self, board1, board2):
        for x1, x2 in zip(board1, board2):
            for y1, y2 in zip(x1, x2):
                self.assertEqual(y1.colour, y2.colour)
                self.assertEqual(type(y1), type(y2))

    def test_set_board(self):
        # Setup the board to the right config
        self.game.set_board('presets/check.txt')

        self.assertEqual(type(self.game.board[7][3]), Queen)
        self.assertEqual(type(self.game.board[5][2]), Pawn)

    def test_get_board_from_config_file(self):
        board = self.game.get_board_from_config_file('presets/check.txt')

        self.assertEqual(type(board[7][3]), Queen)
        self.assertEqual(type(board[5][2]), Pawn)

        # invalid test
        with self.assertRaises(IOError) as context:
            self.game.get_board_from_config_file('./presets/invalid.txt')

    def test_switch_turn(self):
        # Set the board to check
        self.game.set_board('presets/check.txt')

        self.assertEqual(self.game.turn, 'white')
        self.game.switch_turn()
        self.assertEqual(self.game.turn, 'black')

    def test_get_game_state(self):
        # Set the board to check
        self.game.set_board('presets/check.txt')

        self.assertEqual(self.game.game_state, 'black check')
        self.game.switch_turn()
        self.assertEqual(self.game.game_state, 'black check')


    def test_full_move(self):
        # Set the board to check
        self.game.set_board('presets/check.txt')
        golden = Game.get_board_from_config_file('presets/check.txt')
        # Black move
        self.game.switch_turn()

        # do an invalid move on the right color
        self.assertEqual(-1, self.game.full_move(0, 1, 0, 2))
        self.compare_boards(self.game.board, golden)

        # do a invalid move on the other color
        self.assertEqual(-1, self.game.full_move(0, 6, 0, 5))
        self.compare_boards(self.game.board, golden)

        # do a valid move
        self.assertEqual(None, self.game.full_move(6, 1, 6, 2))

        # Check piece
        self.assertEqual(type(self.game.board[6][2]), Pawn)
        self.assertEqual(self.game.board[6][2].colour, 'black')

    def test_make_pawn_promo(self):
        # Set the board to check
        self.game.set_board('presets/promo.txt')

        self.assertEqual(self.game.game_state, 'white pawn promo')

        # Make promotion

if __name__ == '__main__':
    unittest.main()
