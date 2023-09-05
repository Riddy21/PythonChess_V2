from typing import Any
import copy
from pieces import *
from rules import Rules
from enum import Enum
import logging

# Class to record moves and change game board
class Move(object):
    """Class for moving pieces on the board"""
    # init
    def __init__(self, board, x, y, poss_moves, scan_mode=False):
        # Board was not included to save a bit on memory

        # Parameter for move stage
        self.move_stage = "selected"

        # Parameter for to location, initiate as 'move not finished yet'
        self.move_to = -1, -1

        # Parameter for from location
        self.move_from = x, y

        self.move_piece = board[x, y].str_rep

        # Parameters for move type
        self.move_type = "not set"

        self.pawn_promo = 'disabled'

        # Parameter for Move color
        self.move_colour = board[x, y].color

        # Parameter for possible next moves and set to the piece's move array
        self.poss_moves = poss_moves

        # Parameter for captured Piece
        self.captured = 'None'

        # Scan mode
        self.scan_mode = scan_mode

    @staticmethod
    def get_poss_moves(board, turn, x, y, scan_mode=False):
        """
        Function for checking if player picked a piece of the right colour and type
        """
        # if the piece is not blank and is the right colour for the turn
        if board[x, y].str_rep != "-" and board[x, y].color == turn:
            # Add move_id to piece being moved (must be changed before get_moves)
            # only is added if its proper valid move and append move stays true
            # When only will append when the function is not looking ahead to the next move

            # Get the possible moves
            poss_moves = board[x, y].get_moves(x, y, board, scan_mode=scan_mode)

            # If there is still moves left
            if not poss_moves:
                if not scan_mode:
                    logging.debug("No more moves")

                # Remove move num hist
                return []

            # Return the proper poss_moves
            return poss_moves
        if not scan_mode:
            logging.debug("Invalid selection")
        return []

    @classmethod
    def get_all_poss_moves(cls, board):
        """
        Function for checking if player picked a piece of the right colour and type
        """
        poss_moves = dict()
        for loc, square in board:
            if type(square.piece) != Blank:
                poss_moves[loc] = cls.get_poss_moves(board, square.color, loc[0], loc[1], scan_mode=True)
        return poss_moves

    # Removes move_id from piece being moved in case of reselection
    def deselect_move(self, board):
        frox, froy = self.move_from[0], self.move_from[1]

    # Makes a pawn promotion by creating and replacing an old piece
    def make_pawn_promo(self, piece_type, board):
        #only make promotion if in ready state
        if self.pawn_promo != 'ready':
            logging.debug("Invalid pawn promotion")
            return -1

        # Set as for easier use
        tox, toy = self.move_to

        # Make a new piece with same ID, moves history, move history count
        if piece_type == 'Queen':
            new_piece = PieceLibrary.get_piece_ref(PIECES.QUEEN, self.move_colour)
        elif piece_type == 'Rook':
            new_piece = PieceLibrary.get_piece_ref(PIECES.ROOK, self.move_colour)
        elif piece_type == 'Knight':
            new_piece = PieceLibrary.get_piece_ref(PIECES.KNIGHT, self.move_colour)
        elif piece_type == 'Bishop':
            new_piece = PieceLibrary.get_piece_ref(PIECES.BISHOP, self.move_colour)
        else:
            logging.error("wrong piece choice")
            return -1

        # Place in old piece's spot, do not change num moves
        board[tox, toy].piece = new_piece

        self.pawn_promo = 'completed'
        logging.debug('Pawn promoted to %s', piece_type)

    def make_move(self, board, x, y):
        """
        validate move and make the move based on the end coordinates
        """

        # Tries to check if move is valid and returns the move type
        proposed_move = self._try_move(board, x, y)
        # Check if it is a valid move
        # ** Don't set move to until validated
        if proposed_move == -1:
            logging.debug("invalid move")
            return -1

        # if valid move then:
        # Set move stage
        self.move_stage = 'moved'

        # Clear poss moves to empty
        self.poss_moves = []

        # set move_to to x y now that it is verified as a valid move
        self.move_to = x, y

        # change game board based on move locations and move type and save to after move
        self.move_type = proposed_move

        # for easier recognition
        frox, froy = self.move_from
        tox, toy = self.move_to

        # Add move count to moved piece
        board[frox, froy].num_moves += 1

        # Do corresponding move
        if self.move_type == 'enpassant':
            if not self.scan_mode:
                logging.debug('enpassant from %d, %d to %d, %d' % (frox, froy, tox, toy))
            if self.move_colour == COLORS.BLACK:
                self.captured = board[tox, toy - 1]
                board[tox, toy - 1] = board.BLANK_SQUARE
            else:
                self.captured = board[tox, toy + 1]
                board[tox, toy + 1] = board.BLANK_SQUARE
            board[tox, toy], board[frox, froy] = board[frox, froy], board[tox, toy]

        elif self.move_type == 'lcastle':
            if board[0, froy].str_rep != '-':
                if not self.scan_mode:
                    logging.debug('left castle at %d, %d' % (frox, froy))
                # add move count to rook
                board[0, froy].num_moves += 1
                # add move id to rook
                board[tox, toy], board[frox, froy] = board[frox, froy], board[tox, toy]
                board[0, froy], board[3, froy] = board[3, froy], board[0, froy]
            else:
                logging.error("Wrong piece type for castle")

        elif self.move_type == 'rcastle':
            if board[7, froy].str_rep != '-':
                if not self.scan_mode:
                    logging.debug('right castle at %d, %d' % (frox, froy))
                # add move count to rook
                board[7, froy].num_moves += 1
                # add move id to rook
                board[tox, toy], board[frox, froy] = board[frox, froy], board[tox, toy]
                board[7, froy], board[5, froy] = board[5, froy], board[7, froy]
            else:
                logging.debug(self.move_type, "WRONG")

        elif self.move_type == 'capture':
            if not self.scan_mode:
                logging.debug('capture: from %d,%d to %d,%d' % (frox, froy, tox, toy))
            # Capture can be passed by reference because it will never be touched again after being captured
            self.captured = board[tox, toy]
            board[tox, toy] = board[frox, froy]
            board[frox, froy] = board.BLANK_SQUARE

        elif self.move_type == 'move':
            if not self.scan_mode:
                logging.debug('move: from %d,%d to %d,%d' % (frox, froy, tox, toy))
            board[tox, toy], board[frox, froy] = board[frox, froy], board[tox, toy]

    # Undo a move
    def undo_move(self, board):
        # for easier recognition
        frox, froy = self.move_from
        tox, toy = self.move_to

        if not self.scan_mode:
            logging.debug('undo')

        # if pawn Promotion is true
        if self.pawn_promo == 'completed':
            # convert piece back into pawn with all specifications
            board[tox, toy].piece = PieceLibrary.get_piece_ref(PIECES.PAWN, self.move_colour)

        # revert move piece's move count and move history
        board[tox, toy].num_moves -= 1

        # revert move piece back to from location by switching to and from
        board[tox, toy], board[frox, froy] = board[frox, froy], board[tox, toy]

        # If the move was a left castle
        if self.move_type == 'lcastle':
            # delete rook move id and decrement move count
            if board[3, toy].str_rep != '-':
                board[3, toy].num_moves -= 1
                # revert rook back to location
                board[0, toy], board[3, toy] = board[3, toy], board[0, toy]

        # else If the move was a right castle
        elif self.move_type == 'rcastle':
            # delete rook move id and decrement move count
            if board[5, toy].str_rep != '-':
                board[5, toy].num_moves -= 1
                # revert rook back to location
                board[7, toy], board[5, toy] = board[5, toy], board[7, toy]

        # else If the move was an enpassant
        elif self.move_type == 'enpassant':
            # replace captured piece back to old location
            if self.move_colour == COLORS.BLACK:
                board[tox, toy - 1] = self.captured
            elif self.move_colour == COLORS.WHITE:
                board[tox, toy + 1] = self.captured

        # else if the move was a capture
        elif self.move_type == 'capture':
            # replace captured piece back to location
            board[tox, toy] = self.captured

        # else if the move was a move do nothing

    # Private: Validate move
    def is_valid_move(self, tox, toy):
        # If the board piece has the move in its list of possible moves
        if [tox, toy] in self.poss_moves:
            return True
        else:
            return False

    # Tries move and returns move type if valid
    def _try_move(self, board, x, y):

        # Check if valid move on highlights
        if not self.is_valid_move(x, y):
            return -1

        frox, froy = self.move_from

        # Confirms whether a castle happened when the piece was moved
        is_castle = Rules.is_castle(frox, froy, board)

        # Confirms whether enpassant could happen when the piece is moved
        is_enpassant = board[frox, froy].is_enpassant(x, y)

        # Sets instance variable pawn promo based on whether the piece is ready for a pawn promotion
        if board[frox, froy].piece.is_pawn_promo(x, y):
            self.pawn_promo = 'ready'

        # If it is left castle
        if is_castle == Rules.MoveType.LEFT_CASTLE:
            return 'lcastle'
        # If it is right castle
        elif is_castle == Rules.MoveType.RIGHT_CASTLE:
            return 'rcastle'
        # If the move is enpassant
        elif is_enpassant:
            return 'enpassant'
        # If is capture
        elif board[x, y].str_rep != "-":
            return 'capture'
        # If is normal move
        else:
            return 'move'

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __str__(self):
        str = ''
        str += 'move stage: %s\n' \
               'move to: %s\n' \
               'move from: %s\n' \
               'move piece: %s\n' \
               'move type: %s\n' \
               'move colour: %s\n' \
               'captured pieces: %s\n' \
               % (self.move_stage, self.move_to, self.move_from,
                  self.move_piece, self.move_type, self.move_colour, self.captured)
        return str

    # TODO: make converter from str_rep to object
