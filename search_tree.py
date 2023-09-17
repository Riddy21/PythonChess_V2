from copy import deepcopy
from move import Move
from settings import *

class SearchTreeNode(object):
    """Node of the search tree"""
    def __init__(self, move):
        self.children = []
        self.move = move

    def add_child(self, node):
        self.children.append(node)

    def __str__(self):
        out = str(self.move) + '\n'
        for child in self.children:
            out += str(child).replace('\n', '\n    ')[:-4]
        return out

class SearchTreeRoot(SearchTreeNode):
    """Root of the search tree"""
    def __init__(self):
        super().__init__(None)

    def __str__(self):
        # FIXME: Still fixing the print
        out = 'ROOT\n'
        for child in self.children:
            out += str(child).replace('\n', '\n    ')[:-4]
        return out
        

class SearchTree(object):
    """Search tree for the game object to search for the best possible moves"""
    def __init__(self, game):
        self.root = SearchTreeRoot()
        self.board = game.board.copy()
        self.num_nodes = 0
        self.num_leaves = 0
        self.turn = game.turn

    def populate(self, depth=5):
        """Populates the game tree with moves to a certain depth"""
        self._populate_node_recursive(self.root, self.board, depth, self.turn)
    
    def _populate_node_recursive(self, node, board, layers_to_go, turn):
        if layers_to_go == 0:
            self.num_leaves += 1
            return
        # Get the moves from the current game
        moves = self._get_all_moves(board, turn)

        for move in moves:
            # Add the child node
            child = SearchTreeNode(move)
            # Make copy of board
            new_board = board.copy()
            # make the current move on the game
            Move.full_move(*move, new_board)

            if turn == COLORS.WHITE:
                next_turn = COLORS.BLACK
            else:
                next_turn = COLORS.WHITE
            # populate the child node
            self._populate_node_recursive(child, new_board, layers_to_go-1, next_turn)
            # Add child to the node
            node.add_child(child)
            self.num_nodes += 1

    @staticmethod
    def _get_all_moves(board, turn):
        playable_moves_dict = Move.get_all_poss_moves(board, turn)

        playable_moves = set()

        # get all possible next moves
        for source, targets in playable_moves_dict.items():
            for target in targets:
                playable_moves.add((source, target))

        return playable_moves
