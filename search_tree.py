from copy import deepcopy
from game import Game

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
        self.game = game
        self.num_nodes = 0
        self.num_leaves = 0

    def populate(self, depth=5):
        """Populates the game tree with moves to a certain depth"""
        self._populate_node_recursive(self.root, self.game, depth)
    
    def _populate_node_recursive(self, node, game, layers_to_go):
        if layers_to_go == 0:
            self.num_leaves += 1
            return
        # Get the moves from the current game
        moves = self._get_all_moves(game)

        for move in moves:
            # Add the child node
            child = SearchTreeNode(move)
            # Make copy of game
            # FIXME: Change this to a new lightweight game object
            new_game = Game(turn=game.turn, board=game.board, moves=game.moves,
                            captured_white=game.captured_white,
                            captured_black=game.captured_black)
            # make the current move on the game
            new_game.full_move(*move)
            # populate the child node
            self._populate_node_recursive(child, new_game, layers_to_go-1)
            # Add child to the node
            node.add_child(child)
            self.num_nodes += 1

    @staticmethod
    def _get_all_moves(game):
        playable_pieces = game.get_playable_piece_coords()

        playable_moves = set()

        # get all possible next moves
        for piece in playable_pieces:
            moves = game.get_next_poss_moves(*piece)
            for move in moves:
                playable_moves.add((*piece, *move))

        return playable_moves
