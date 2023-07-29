import unittest
from game import *
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
        self.game.set_board('Presets/check.txt')

        self.assertEqual(type(self.game.board[7][3]), Queen)
        self.assertEqual(type(self.game.board[5][2]), Pawn)

    def test_get_board_from_config_file(self):
        board = self.game.get_board_from_config_file('Presets/check.txt')

        self.assertEqual(type(board[7][3]), Queen)
        self.assertEqual(type(board[5][2]), Pawn)

        # invalid test
        with self.assertRaises(GameUserError) as context:
            self.game.get_board_from_config_file('./Presets/invalid.txt')

    def test_switch_turn(self):
        # Set the board to check
        self.game.set_board('Presets/check.txt')

        self.assertEqual(self.game.turn, 'white')
        self.game.switch_turn()
        self.assertEqual(self.game.turn, 'black')

    def test_set_turn(self):
        # Set the board to check
        self.game.set_board('Presets/check.txt')

        self.assertEqual(self.game.turn, 'white')
        self.game.set_turn('black')
        self.assertEqual(self.game.turn, 'black')

    def test_get_game_state(self):
        # Set the board to check
        self.game.set_board('Presets/check.txt')

        self.assertEqual(self.game.game_state, 'black check')
        self.game.switch_turn()
        self.assertEqual(self.game.game_state, 'black check')

        # Set the board to check
        self.game.set_board('Presets/promo.txt')
        self.assertEqual(self.game.game_state, 'white pawn promo')


    def test_full_move(self):
        # Set the board to check
        self.game.set_board('Presets/check.txt')
        golden = Game.get_board_from_config_file('Presets/check.txt')
        # Black move
        self.game.set_turn('black')

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
        self.game.set_board('Presets/promo.txt')

        # Try making a move on both sides
        self.assertEqual(-1, self.game.full_move(6, 1, 6, 2))
        self.assertEqual(-1, self.game.full_move(0, 1, 0, 2))

        self.assertEqual('white', self.game.turn)

        # Make promotion
        self.game.make_pawn_promo('Queen')

        self.assertEqual('black', self.game.turn)

    def test_undo_move(self):
        # Set the board to check
        self.game.set_board('Presets/check.txt')
        golden = Game.get_board_from_config_file('Presets/check.txt')

        self.game.undo_move()

        # Black move and undo
        self.game.switch_turn()
        self.game.full_move(6, 1, 6, 2)
        self.game.undo_move()
        
        self.compare_boards(self.game.board, golden)

    def test_export_board(self):
        self.game.set_board('Presets/check.txt')
        test_out_file = 'utests/export_test/test.txt'
        if os.path.isfile(test_out_file):
            os.remove(test_out_file)
        self.game.export_board(test_out_file)

        test_file = open('utests/export_test/test.txt').readlines()
        gold_file = open('utests/export_test/golden.txt').readlines()

        self.assertEqual(test_file, gold_file)

        # try opening the file
        self.game.set_board(test_out_file)
        os.remove(test_out_file)

    def test_handle_move(self):
        # Set the board to check
        self.game.set_board('Presets/check.txt')
        golden = Game.get_board_from_config_file('Presets/check.txt')
        self.game.set_turn('black')

        # do an invalid move on the right color
        self.game.handle_move(0, 1)
        self.game.handle_move(0, 2)
        self.compare_boards(self.game.board, golden)

        # do a invalid move on the other color
        self.game.handle_move(0, 6)
        self.game.handle_move(0, 5)
        self.compare_boards(self.game.board, golden)

        # do a valid move
        self.game.handle_move(6, 1)
        self.game.handle_move(6, 2)

        # Check piece
        self.assertEqual(type(self.game.board[6][2]), Pawn)
        self.assertEqual(self.game.board[6][2].colour, 'black')

    def test_get_next_poss_moves(self):
        # Set the board to check
        self.game.set_board('Presets/check.txt')
        self.game.set_turn('black')

        golden = [[6, 2]]
        self.assertEqual(golden, self.game.get_next_poss_moves(6, 1))

    def test_get_current_poss_moves(self):
        # Set the board to check
        self.game.set_board('Presets/check.txt')
        self.game.set_turn('black')

        self.assertEqual((), self.game.get_current_poss_moves())
        self.game.handle_move(6, 1)
        golden = [[6, 2]]
        self.assertEqual(golden, self.game.get_current_poss_moves())

    def test_get_playable_piece_coords(self):
        # Set the board to check
        self.game.set_board('Presets/check.txt')
        self.game.set_turn('black')

        golden = {(6, 1)}
        self.assertEqual(golden, self.game.get_playable_piece_coords())

    def test_get_piece_coords(self):
        # Set the board to check
        self.game.set_board('Presets/check.txt')

        golden = {(7, 3)}
        self.assertEqual(golden, self.game.get_piece_coords('Q'))

if __name__ == '__main__':
    unittest.main()
