import unittest
from search_tree import SearchTree
from game import Game
from timeit import default_timer as timer

class TestSearchTree(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.tree = SearchTree(self.game)

    def tearDown(self):
        self.game.quit()

    def test_get_all_moves(self):
        moves = self.tree._get_all_moves(self.game)

        starting_moves = {(5, 6, 5, 5), (6, 7, 7, 5), (6, 6, 6, 4),
                          (2, 6, 2, 5), (1, 7, 0, 5), (0, 6, 0, 4),
                          (7, 6, 7, 4), (3, 6, 3, 4), (5, 6, 5, 4),
                          (1, 7, 2, 5), (2, 6, 2, 4), (1, 6, 1, 5),
                          (4, 6, 4, 5), (6, 6, 6, 5), (0, 6, 0, 5),
                          (6, 7, 5, 5), (7, 6, 7, 5), (3, 6, 3, 5),
                          (1, 6, 1, 4), (4, 6, 4, 4)}

        self.assertEqual(moves, starting_moves)

    def test_populate(self):
        start = timer()
        self.tree.populate(depth=2)
        end = timer()

        length = end - start
        self.assertEqual(self.tree.num_nodes, 420)
        self.assertEqual(self.tree.num_leaves, 400)
        self.assertLess(length, 5)

