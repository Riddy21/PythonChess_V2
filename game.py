from typing import Any
import sys, os
from pieces import *
from move import Move
from threading import Event, Lock
from copy import deepcopy
from board import BoardManager
from settings import *
import logging

# NOTE: Next things to do

# TODO: Move get game state down to a solver engine that is only passed a game board
# Change game board to an object
# Add a dict of pieces to the game board so that it's easier to access and faster
# 1. Use dict of pieces, with coordinates as a property?
# Change pieces to singletons that are referenced in the board
#   1. Made piece library to implement this change
# Edit Pices to be must more lite weight
# TODO: Make a lock decorator to lock the functions that need locking
#       NOTE: Make sure that they don't call each other
#             only lock forward facing functions that modify shared variables

class GameInternalError(Exception):
    """
    This exception is thrown when an internal error occurs
    """
    pass

class GameUserError(Exception):
    """
    This exception is raised when the user of the API provides
    incorrect input
    """
    pass

# Game class initiated when the game board is displayed
class Game:
    def __init__(self, turn=COLORS.WHITE, board=None, moves=None, captured_white=None, captured_black=None, prev_game_state='normal'):
        if captured_black is None:
            captured_black = []
        if captured_white is None:
            captured_white = []
        if moves is None:
            moves = []

        # captured Pieces
        self.captured_white = captured_white
        self.captured_black = captured_black

        # stack of all old moves and current move
        self.moves = moves

        # string representing the turn colour of the game
        if type(turn) == str:
            turn = COLORS.get_by_str_rep(turn)
        self.turn = turn
        self.switch_turn_event = Event()

        self.game_state = prev_game_state

        # if board was not loaded by passing a parameter, set the board
        if not board:
            self.set_board()
        else:
            self.board = board.copy()

        # TODO: Add poss moves attribute here and check every switch turn


    @staticmethod
    def get_board_from_config_file(config_file):
        """Reads the config file and returns the board object"""
        return BoardManager.get_board_from_file(config_file)


    def set_board(self, config_file=DEFAULT_BOARD_PRESET_PATH):
        # Create blank board
        self.board = self.get_board_from_config_file(config_file)
        self.update_game_state()

    def export_board(self, filename):
        """
        Saves the current board in a file
        """
        if os.path.isfile(filename):
            logging.warning('Overwriting %s', filename)
        file = open(filename, 'w')
        file.write(self.__str__())
        file.close()

    # Function to switch turns
    def switch_turn(self):
        self.switch_turn_quiet()

        # Set multiprocessing event
        self.alert_players()

    def set_turn(self, turn):
        """Sets turn to the color specified"""
        if self.turn in (COLORS.WHITE, COLORS.BLACK):
            self.turn = turn
        else:
            raise GameUserError("Not a valid turn setting")

        self.update_game_state()

    # switch turns without notifying players
    def switch_turn_quiet(self):
        if self.turn == COLORS.WHITE:
            self.turn = COLORS.BLACK
        else:
            self.turn = COLORS.WHITE

        self.update_game_state()

    # Function to make complete move from to-coordinates and from-coordinates
    def full_move(self, frox, froy, tox, toy):
        if self.move_from(frox, froy) == -1:
            return -1
        if self.move_to(tox, toy) == -1:
            return -1

    # Function to change pawn promotion piece
    def make_pawn_promo(self, promo_type):
        # if the pawn promotion goes through, switch turns
        try:
            if self.moves[-1].make_pawn_promo(promo_type, self.board) != -1:
                self.switch_turn()
            else:
                raise GameUserError("Pawn promo failed")
        except IndexError:
            raise GameInternalError("There are no moves in the stack") from None
        # TODO: turn return -1 to a try catch

    # Function to undo a move and remove it from the move list
    def undo_move(self, num=1):
        for i in range(num):
            # undo move and delete move
            if len(self.moves) != 0:
                # if in selection mode
                if getattr(self.moves[-1], 'move_stage') == 'selected':
                    # exit from selection mode
                    self.moves[-1].deselect_move(self.board)
                    del self.moves[-1]
                else:
                    self.moves[-1].undo_move(self.board)
                    del self.moves[-1]
                    self.switch_turn_quiet() # Make sure no players are alerted
        self.alert_players()

    # Function to check return what move stage we are at and handle move button
    def handle_move(self, x, y):
        # Check if moving from or moving to
        if not self.moves or getattr(self.moves[-1], 'move_stage') == 'moved':
            # If fresh board with no moves or move is finished move from this location
            self.move_from(x, y)
        else:
            # if the player selects a different piece to move
            if self.board[x, y].color == self.turn:
                # Removes move_id from piece and deletes move
                self.moves[-1].deselect_move(self.board)
                del self.moves[-1]
                self.move_from(x, y)
            # otherwise start a new move
            else:
                self.move_to(x, y)

    # Function to start move
    def move_from(self, x, y):
        # DOn't allow move if pawn promotion is valid
        if self.moves and self.moves[-1].pawn_promo == 'ready':
            logging.debug("Invalid Selection, pawn promotion underway")
            return -1
        # Get possible moves
        poss_moves = Move.get_poss_moves(self.board, self.turn, x, y)

        # Check if it is a valid selection, if not, exit the function
        if not poss_moves:
            return -1

        # Create a new move and add to list and pass the len of move list as move id
        self.moves.append(Move(self.board, x, y, poss_moves))

    # Function to return possible moves for the piece entered without making the move
    def get_next_poss_moves(self, x, y):
        poss_moves = Move.get_poss_moves(self.board, self.turn, x, y)

        return poss_moves


    # Faster way to access current poss moves without recalculating all poss moves
    def get_current_poss_moves(self):
        if self.moves:
            return self.moves[-1].poss_moves
        return ()

    # get the coordinates of the pieces that are playable on that turn
    def get_playable_piece_coords(self):
        playable = set()
        for (x, y), square in self.board.items():
            if square.piece.color == self.turn:
                if self.get_next_poss_moves(x, y):
                    playable.add((x, y))
        return playable


    # Function to end move,
    def move_to(self, x, y):
        # Makes move on the most recent move, if invalid move, don't switch sides
        if self.moves[-1].make_move(self.board, x, y) == -1:
            return -1

        # FIXME One the get_game_state is stateless, you can update game state here

        # Append captured pieces to the correct captured list
        captured_piece = getattr(self.moves[-1], 'captured')
        if captured_piece == 'None':
            pass
        elif captured_piece.color == COLORS.BLACK:
            self.captured_black.append(captured_piece)
        elif captured_piece.color == COLORS.WHITE:
            self.captured_white.append(captured_piece)

        # if the move results in pawn promotion don't switch turn
        if self.moves[-1].pawn_promo == 'ready':
            # FIXME: make this a side process that happens every time the board changes
            self.update_game_state()
        else:
            self.switch_turn()

    def update_game_state(self):
        self.game_state = self.get_game_state()

    # FIXME: remove dependency on turn you are checking and enable it to be stateless
    def get_game_state(self):
        """
        Gets the the state of the game
        white pawn promo
        white check
        white checkmate
        white pawn promo
        black check
        black checkmate
        stalemate
        MUST BE IN THE TURN OF THE SIDE YOU'RE CHECKING
        """

        can_move = False
        in_check = False

        # in opponent's turn currently
        num_pieces = 0

        # loops through all pieces on the board
        for (x, y), item in self.board.items():
            piece = item.piece
            # pawn promo check
            if y == 0 and piece.str_rep == 'P':
                return 'white pawn promo'

            if y == BOARD_HEIGHT - 1 and piece.str_rep == 'p':
                return 'black pawn promo'

            # If the piece iterated on is piece of the next turn
            if piece.color != None:
                num_pieces += 1
            if piece.color == self.turn:
                # If the piece is the king
                if piece.str_rep == 'k' or piece.str_rep == 'K':
                    # Test if it is in check
                    in_check = Rules.isin_check((x, y), self.board)
                # Try to move it and if there are no more moves
                if self.get_next_poss_moves(x, y):
                    # set can move to true and break out
                    can_move = True

        # If there's only 2 kings left
        if num_pieces <= 2:
            return 'stalemate'

        if not can_move:
            if in_check:
                return '%s checkmate' % self.turn.value
            else:
                return 'stalemate'

        elif in_check:
            return '%s check' % self.turn.value

        else:
            return 'normal'

    # Get the coordinates of that type of piece
    def get_piece_coords(self, piece_str):
        coords = set()
        for (x, y), square in self.board.items():
            if square.piece.str_rep == piece_str:
                coords.add((x,y))
        return coords

    # Convert chess coords to int coords
    def get_chess_coords(self, col, row):
        return f"{chr(97+col)}{8-row}"

    # Static: Converts Object board to string board
    def get_chess_board_string_array(self):
        return [[self.board[x, y].piece.str_rep for x in range(8)] for y in range(8)]

    # TODO: Static: Converts String board to Object board

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def __str__(self):
        return self.board.__str__()

    def print_move_counts(self):
        string = ''

        # Add board string reps
        for y in range(len(self.board[0])):
            for x in range(len(self.board)):
                string += str(self.board[x][y].move_count) + ' '
            string += '\n'

        print(string)

    def print_move_hist(self):
        string = ''

        # Add board string reps
        for y in range(len(self.board[0])):
            for x in range(len(self.board)):
                string += str(len(self.board[x][y].move_num_history)) + ' '
            string += '\n'

        print(string)

    def alert_players(self):
        """Notify players that move can be made"""
        self.switch_turn_event.set()
        self.switch_turn_event.clear()

    def quit(self):
        """Exits the game"""
        self.alert_players()
        del self
        return
