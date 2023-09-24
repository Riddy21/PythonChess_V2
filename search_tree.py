from copy import deepcopy
from move import Move
from settings import *
from rules import Rules
from predict import Predict
import math
import logging

class SearchTreeNode(object):
    """Node of the search tree"""
    def __init__(self, move_obj, board=None, promo=None):
        self.children = []
        self.children_dict = {}
        self.move = None
        self.move_obj = None
        self.points = 0
        self.board = board
        self.promo = promo

        if move_obj:
            self.move = (move_obj.move_from, move_obj.move_to)
            self.move_obj = move_obj

    def evaluate_points(self, orig_turn, next_poss_moves):
        """Evaluate points gained in the previous move"""
        self.points = Predict.get_points(self.move_obj, self.board, orig_turn, next_poss_moves)

    def add_child(self, node):
        """
        Add child node, will add the points of the child to the node
        """
        self.children.append(node)
        self.children_dict[node.move] = node

    def __str__(self):
        out = str(self.move) + " %d" % self.points + '\n'
        for child in self.children:
            out += str(child).replace('\n', '\n    ')[:-4]
        return out

class SearchTreeRoot(SearchTreeNode):
    """Root of the search tree"""
    def __init__(self):
        super().__init__(None)

    def evaluate_points(self, turn, next_poss_moves):
        # Root doesn't have points
        self.points = 0

    def __str__(self):
        # FIXME: Still fixing the print
        out = 'ROOT\n'
        for child in self.children:
            out += str(child).replace('\n', '\n    ')[:-4]
        return out
        

class SearchTree(object):
    """Search tree for the game object to search for the best possible moves"""
    def __init__(self, game):
        self.root = None
        self.game = game
        self.num_nodes = 0
        self.num_leaves = 0
        self.depth = 0

    # TODO: Add function to add one more row to the tree

    def populate(self, depth=5):
        """Populates the game tree with moves to a certain depth"""
        self.num_nodes = 0
        self.num_leaves = 0
        self.root = SearchTreeRoot()
        self._populate_node_recursive(self.root, self.game.board, depth, self.game.turn)
        self.depth = depth

    def populate_continue(self, depth=5, moves_made=None):
        """Populates a prepopulated tree further"""
        if moves_made:
            for move in moves_made:
                move_tuple = (move.move_from, move.move_to)
                self.root = self.root.children_dict[move_tuple]
                self.depth -= 1

        self.num_leaves = 0
        self._populate_node_recursive(self.root, self.game.board, depth+self.depth, self.game.turn)
        self.depth = depth + self.depth

    def reset(self):
        self.root = None
        self.num_nodes = 0
        self.num_leaves = 0

    def get_best_move(self):
        """
        Gets the best move based on the points tallied in the nodes
        """
        if self.root == None:
            logging.error("Please populate the root")

        poss_moves = dict()
        # loop through next moves
        for node in self.root.children:
            # Tally up the points under the tree
            poss_moves[node] = self._add_avg_points_recursive(node)
        
        # FIXME: Still not always making the best move
        best_move_node = max(poss_moves, key=poss_moves.get)

        #return the move and the promo if there is any
        return best_move_node

    @classmethod
    def _add_avg_points_recursive(cls, node):
        """
        Add the current node's points with the average of the child points
        """
        # add the current points
        points = node.points

        # If it's a leaf node just return the points
        if not node.children:
            return points

        # Average teh points of the children
        total = 0
        for child in node.children:
            total += cls._add_avg_points_recursive(child)
        points += total/len(node.children)

        return points
    
    def _populate_node_recursive(self, node, board, layers_to_go, turn):
        if layers_to_go == 0:
            self.num_leaves += 1
            return

        if turn == COLORS.WHITE:
            next_turn = COLORS.BLACK
        else:
            next_turn = COLORS.WHITE

        # If the node is already populated, then just keep going
        if node.children != []:
            for child in node.children:
                self._populate_node_recursive(child, child.board, layers_to_go-1, next_turn)
            return

        # Get the moves from the current game
        moves = self._get_all_moves(board, turn)

        node.evaluate_points(self.game.turn, moves)

        for move in moves:
            if Rules.is_pawn_promo(*move, board):
                valid_pieces = [PIECES.QUEEN, PIECES.ROOK, PIECES.KNIGHT, PIECES.BISHOP]
                for piece in valid_pieces:
                    # Make copy of board
                    new_board = board.copy()
                    # make the current move on the game
                    move_obj = Move.full_move(*move, new_board)
                    # make the promo
                    move_obj.make_pawn_promo(piece, new_board)

                    # Add the child node
                    child = self._add_child_node(node, move_obj, new_board, piece)
                    # populate the child node
                    self._populate_node_recursive(child, new_board, layers_to_go-1, next_turn)

            else:
                # Make copy of board
                new_board = board.copy()

                # make the current move on the game
                move_obj = Move.full_move(*move, new_board)

                # Add the child node
                child = self._add_child_node(node, move_obj, new_board)
                # populate the child node
                self._populate_node_recursive(child, new_board, layers_to_go-1, next_turn)

    def _add_child_node(self, parent, move, board, promo=None):
        # Add the child node
        child = SearchTreeNode(move, board, promo)
        parent.add_child(child)
        self.num_nodes += 1
        return child

    @staticmethod
    def _get_all_moves(board, turn):
        playable_moves_dict = Move.get_all_poss_moves(board, turn)

        playable_moves = set()

        # get all possible next moves
        for source, targets in playable_moves_dict.items():
            for target in targets:
                playable_moves.add((source, target))

        return playable_moves
