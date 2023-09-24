import unittest
from search_tree import SearchTree
from game import Game
from settings import *
from timeit import default_timer as timer

class TestSearchTree(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.tree = SearchTree(self.game)

    def tearDown(self):
        self.game.quit()

    def test_get_all_moves(self):
        moves = self.tree._get_all_moves(self.game.board, turn=COLORS.WHITE)

        starting_moves = {((5, 6), (5, 5)), ((6, 7), (7, 5)), ((6, 6), (6, 4)),
                          ((2, 6), (2, 5)), ((1, 7), (0, 5)), ((0, 6), (0, 4)),
                          ((7, 6), (7, 4)), ((3, 6), (3, 4)), ((5, 6), (5, 4)),
                          ((1, 7), (2, 5)), ((2, 6), (2, 4)), ((1, 6), (1, 5)),
                          ((4, 6), (4, 5)), ((6, 6), (6, 5)), ((0, 6), (0, 5)),
                          ((6, 7), (5, 5)), ((7, 6), (7, 5)), ((3, 6), (3, 5)),
                          ((1, 6), (1, 4)), ((4, 6), (4, 4))}

        self.assertEqual(moves, starting_moves)

    def test_populate(self):
        start = timer()
        self.tree.populate(depth=2)
        end = timer()

        length = end - start
        self.assertEqual(self.tree.num_nodes, 420)
        self.assertEqual(self.tree.num_leaves, 400)
        self.assertLess(length, 0.5)

    def test_promotion(self):
        # Testing when the search tree needs to make pawn promo
        self.game.set_board('Presets/ready_to_promo.txt')

        start = timer()
        self.tree.populate(depth=2)
        end = timer()

        length = end - start
        self.assertEqual(self.tree.num_nodes, 558)
        self.assertEqual(self.tree.num_leaves, 531)
        self.assertLess(length, 0.5)

    def test_populate_continue(self):
        start = timer()
        self.tree.populate(depth=1)
        self.tree.populate_continue(depth=1)
        end = timer()

        length = end - start
        self.assertEqual(self.tree.num_nodes, 420)
        self.assertEqual(self.tree.num_leaves, 400)
        self.assertLess(length, 0.5)

    def test_populate_continue_with_moves_made(self):
        self.tree.populate(depth=2)

        best_move = self.tree.get_best_move().move

        self.game.full_move(*best_move[0], *best_move[1])

        self.game.full_move(0, 1, 0, 2)

        self.tree.populate_continue(2, self.game.moves[-2:])

    def test_get_best_move(self):
        self.game.set_board('Presets/almost_checkmate.txt')
        self.game.set_turn(COLORS.BLACK)

        self.tree.populate(depth=2)

        best_move = self.tree.get_best_move()

        self.assertEqual(best_move.move, ((2, 6), (2, 7)))
        self.assertEqual(best_move.promo, None)

        # TODO: Make a test with a pawn promo
        self.game.set_board('Presets/promo_check.txt')
        self.game.set_turn(COLORS.WHITE)

        self.tree.populate(depth=2)

        best_move = self.tree.get_best_move()

        self.assertEqual(best_move.move, ((2, 1), (2, 0)))
        self.assertEqual(best_move.promo, PIECES.KNIGHT)


if __name__ == '__main__':
    unittest.main()

