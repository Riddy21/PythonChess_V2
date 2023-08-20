from typing import Any
from collections import defaultdict
import uuid
from enum import Enum
from settings import *
from rules import Rules
from move import Move

# Abstract Piece Class
class _Piece(object):
    def __init__(self, value, color, str_rep):
        # initiate variables
        self.value = value
        self.color = color
        self.str_rep = str_rep

    # Base functions that will be overriden when necessary
    def is_castle(self, x, y, board):
        return -1

    def is_enpassant(self, x, y):
        return False

    def is_pawn_promo(self, x, y):
        return False

    def get_moves(self, x, y, board, scan_mode=False):
        return []

    # Private: Limits possible moves based on check cases
    def chk_limit_moves(self, board, myx, myy, poss_moves):
        from game import Game
        # Make a copy of the current game using the board and turn
        probe_game = Game(turn=self.color, board=board, scan_mode=True)

        bad_moves = []

        # Start a move
        probe_game.handle_move(myx, myy)

        is_king = False

        # Find personal king
        for y in range(8):
            for x in range(8):
                if self.color == COLORS.WHITE and board[x, y].piece.str_rep == 'K':
                    king_x = x
                    king_y = y
                    is_king = True
                    break
                elif self.color == COLORS.BLACK and board[x, y].piece.str_rep == 'k':
                    king_x = x
                    king_y = y
                    is_king = True
                    break

        if not is_king:
            return poss_moves

        current_poss_moves = probe_game.get_current_poss_moves()

        # Skips iterations if nothing can move
        if not current_poss_moves:
            return poss_moves

        # For each move the piece can make
        for my_move in current_poss_moves:
            # Make the move to my move
            probe_game.handle_move(my_move[0], my_move[1])

            # switch turn to king's turn
            probe_game.switch_turn()
            # Checks if king is in check
            if board[king_x, king_y].piece.isin_check(king_x, king_y, probe_game):
                bad_moves.append([my_move[0], my_move[1]])

            # switches back
            probe_game.switch_turn()

            probe_game.undo_move()

            probe_game.handle_move(myx, myy)

        probe_game.undo_move()

        # Finding difference between 2 sets
        def diff(li1, li2):
            for i in li2:
                if i in li1:
                    li1.remove(i)
            return li1

        # Diff the 2 sets
        poss_moves = diff(poss_moves, bad_moves)

        # Return poss_moves
        return poss_moves

    def __str__(self):
        str = '\n    color: %s\n' \
              '    str_rep: %s\n' \
              % (self.color, self.str_rep)
        return str


class Pawn(_Piece):
    def __init__(self, color):
        str_rep = PIECES.PAWN.value['str_rep']
        if color == COLORS.WHITE:
            str_rep = str_rep.upper()

        # Makes a piece with set values and images
        super().__init__(PIECES.PAWN.value['value'], color, str_rep)

        # Make variable to store where enpassants are, set default as empty list
        self.enpassant_pos = []

    # Pawn move set given the location of the piece
    def get_moves(self, x, y, board, scan_mode=False):
        poss_moves = []

        # Black moves
        if board[x, y].color == COLORS.BLACK:
            i = 1

            # Do Move detection
            while i <= 2 and y + i <= 7:
                piece_detect = Rules.detect_obstruction((x, y), (x, y + i), board)
                # basic
                if piece_detect != Rules.ObstructionType.UNOBSTRUCTED:
                    break

                # no 2nd move on 2nd turn
                if board[x, y].num_moves >= 1:
                    poss_moves.append([x, y + i])
                    break

                # add the position and increment counter
                poss_moves.append([x, y + i])
                i += 1

            # NOTE: ONLY WHEN SCAN MODE AND KING CAN BE CAPTURED
            # Sideways Capture, ** if in scan mode, side captures count even if there is no piece currently there
            if x < 7 and y < 7 and board[x + 1, y + 1].color == COLORS.WHITE:
                poss_moves.append([x + 1, y + 1])
            if x > 0 and y < 7 and board[x - 1, y + 1].color == COLORS.WHITE:
                poss_moves.append([x - 1, y + 1])

        # white moves
        elif board[x, y].color == COLORS.WHITE:
            i = 1

            while i <= 2 and y - i >= 0:
                piece_detect = Rules.detect_obstruction((x, y), (x, y - i), board)
                if piece_detect != Rules.ObstructionType.UNOBSTRUCTED:
                    break

                # no 2nd move on 2nd turn
                elif board[x, y].num_moves >= 1:
                    poss_moves.append([x, y - i])
                    break

                # add the position and increment counter
                poss_moves.append([x, y - i])
                i += 1

            # NOTE: ONLY WHEN SCAN MODE AND KING CAN BE CAPTURED
            # Sideways Capture
            if x < 7 and y > 0 and board[x + 1, y - 1].color == COLORS.BLACK:
                poss_moves.append([x + 1, y - 1])
            if x > 0 and y > 0 and board[x - 1, y - 1].color == COLORS.BLACK:
                poss_moves.append([x - 1, y - 1])

        # enPassante
        if self.color == COLORS.WHITE and y == 3:
            if (x + 1 in range(8)) and board[x + 1, y].color == COLORS.BLACK and \
                    board[x + 1, y].num_moves == 1:
                if Rules.detect_obstruction((x, y), (x + 1, y - 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.append([x + 1, y - 1])
                    self.enpassant_pos.append([x + 1, y - 1])
            if (x - 1 in range(8)) and board[x - 1, y].color == COLORS.BLACK and \
                    board[x - 1, y].num_moves == 1:
                if Rules.detect_obstruction((x, y), (x - 1, y - 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.append([x - 1, y - 1])
                    self.enpassant_pos.append([x - 1, y - 1])
        elif self.color == COLORS.BLACK and y == 4:
            if (x + 1 in range(8)) and board[x + 1, y].color == COLORS.WHITE and \
                    board[x + 1, y].num_moves == 1:
                if Rules.detect_obstruction((x, y), (x + 1, y + 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.append([x + 1, y + 1])
                    self.enpassant_pos.append([x + 1, y + 1])
            if (x - 1 in range(8)) and board[x - 1, y].color == COLORS.WHITE and \
                    board[x - 1, y].num_moves == 1:
                if Rules.detect_obstruction((x, y), (x - 1, y + 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.append([x - 1, y + 1])
                    self.enpassant_pos.append([x - 1, y + 1])

        # only do this line if not scanning opponent for check to avoid getting stuck in recursive loop
        if not scan_mode:
            poss_moves = self.chk_limit_moves(board, x, y, poss_moves)

        return poss_moves

    # Returns True or False based on whether a enpassant was chosen
    def is_enpassant(self, x, y):
        if [x, y] in self.enpassant_pos:
            self.enpassant_pos = []
            return True
        return False

    # Returns True or False based on whether a pawn promotion is possible
    def is_pawn_promo(self, x, y):
        if y == 7 or y == 0:
            return True
        return False


class Rook(_Piece):
    def __init__(self, color):
        str_rep = PIECES.ROOK.value['str_rep']
        if color == COLORS.WHITE:
            str_rep = str_rep.upper()
        # Makes a piece with set values and images
        super().__init__(PIECES.ROOK.value['value'], color, str_rep)

    # Returns possible moves this piece can make
    def get_moves(self, x, y, board, scan_mode=False):
        poss_moves = []

        i = 1
        # All x moves below x
        while x - i >= 0:
            if Rules.detect_obstruction((x, y), (x - i, y), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x - i, y), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.append([x - i, y])
                break
            poss_moves.append([x - i, y])
            i += 1

        i = 1
        # All x moves above x
        while (x + i) <= 7:
            if Rules.detect_obstruction((x, y), (x + i, y), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x + i, y), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.append([x + i, y])
                break
            poss_moves.append([x + i, y])
            i += 1

        i = 1
        # All y moves below y
        while y - i >= 0:
            if Rules.detect_obstruction((x, y), (x, y - i), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x, y - i), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.append([x, y - i])
                break
            poss_moves.append([x, y - i])
            i += 1
        i = 1
        # All x moves above y
        while (y + i) <= 7:
            if Rules.detect_obstruction((x, y), (x, y + i), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x, y + i), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.append([x, y + i])
                break
            poss_moves.append([x, y + i])
            i += 1

        # only do this line if not scanning opponent for check to avoid getting stuck in recursive loop
        if not scan_mode:
            poss_moves = self.chk_limit_moves(board, x, y, poss_moves)

        return poss_moves


class Knight(_Piece):
    def __init__(self, color):
        str_rep = PIECES.KNIGHT.value['str_rep']
        if color == COLORS.WHITE:
            str_rep = str_rep.upper()
        # Makes a piece with set values and images
        super().__init__(PIECES.KNIGHT.value['value'], color, str_rep)

    # Returns possible moves this piece can make
    def get_moves(self, x, y, board, scan_mode=False):
        poss_moves = []
        if x + 2 <= 7:
            if y + 1 <= 7:
                if Rules.detect_obstruction((x, y), (x + 2, y + 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.append([x + 2, y + 1])
            if y - 1 >= 0:
                if Rules.detect_obstruction((x, y), (x + 2, y - 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.append([x + 2, y - 1])

        if x + 1 <= 7:
            if y + 2 <= 7:
                if Rules.detect_obstruction((x, y), (x + 1, y + 2), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.append([x + 1, y + 2])
            if y - 2 >= 0:
                if Rules.detect_obstruction((x, y), (x + 1, y - 2), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.append([x + 1, y - 2])
        if x - 2 >= 0:
            if y + 1 <= 7:
                if Rules.detect_obstruction((x, y), (x - 2, y + 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.append([x - 2, y + 1])
            if y - 1 >= 0:
                if Rules.detect_obstruction((x, y), (x - 2, y - 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.append([x - 2, y - 1])
        if x - 1 >= 0:
            if y + 2 <= 7:
                if Rules.detect_obstruction((x, y), (x - 1, y + 2), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.append([x - 1, y + 2])
            if y - 2 >= 0:
                if Rules.detect_obstruction((x, y), (x - 1, y - 2), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.append([x - 1, y - 2])

        # only do this line if not scanning opponent for check to avoid getting stuck in recursive loop
        if not scan_mode:
            poss_moves = self.chk_limit_moves(board, x, y, poss_moves)

        return poss_moves


class Bishop(_Piece):
    def __init__(self, color):
        str_rep = PIECES.BISHOP.value['str_rep']
        if color == COLORS.WHITE:
            str_rep = str_rep.upper()
        # Makes a piece with set values and images
        super().__init__(PIECES.BISHOP.value['value'], color, str_rep)

    def get_moves(self, x, y, board, scan_mode=False):
        poss_moves = []

        i = 1
        # All moves top left
        while x - i >= 0 and y - i >= 0:
            if Rules.detect_obstruction((x, y), (x - i, y - i), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x - i, y - i), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.append([x - i, y - i])
                break
            poss_moves.append([x - i, y - i])
            i += 1

        i = 1
        # All moves bottom right
        while x + i <= 7 and y + i <= 7:
            if Rules.detect_obstruction((x, y), (x + i, y + i), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x + i, y + i), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.append([x + i, y + i])
                break
            poss_moves.append([x + i, y + i])
            i += 1

        i = 1
        # All y moves below y
        while x - i >= 0 and y + i <= 7:
            if Rules.detect_obstruction((x, y), (x - i, y + i), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x - i, y + i), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.append([x - i, y + i])
                break
            poss_moves.append([x - i, y + i])
            i += 1

        i = 1
        # All x moves above y
        while x + i <= 7 and y - i >= 0:
            if Rules.detect_obstruction((x, y), (x + i, y - i), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x + i, y - i), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.append([x + i, y - i])
                break
            poss_moves.append([x + i, y - i])
            i += 1

        # only do this line if not scanning opponent for check to avoid getting stuck in recursive loop
        if not scan_mode:
            poss_moves = self.chk_limit_moves(board, x, y, poss_moves)

        return poss_moves


class Queen(_Piece):
    def __init__(self, color):
        str_rep = PIECES.QUEEN.value['str_rep']
        if color == COLORS.WHITE:
            str_rep = str_rep.upper()

        # Makes a piece with set values and images
        super().__init__(PIECES.QUEEN.value['value'], color, str_rep)

    def get_moves(self, x, y, board, scan_mode=False):
        poss_moves = []

        # Rook moves + Bishop moves
        i = 1
        # All moves top left
        while x - i >= 0 and y - i >= 0:
            if Rules.detect_obstruction((x, y), (x - i, y - i), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x - i, y - i), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.append([x - i, y - i])
                break
            poss_moves.append([x - i, y - i])
            i += 1

        i = 1
        # All moves bottom right
        while x + i <= 7 and y + i <= 7:
            if Rules.detect_obstruction((x, y), (x + i, y + i), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x + i, y + i), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.append([x + i, y + i])
                break
            poss_moves.append([x + i, y + i])
            i += 1

        i = 1
        # All y moves below y
        while x - i >= 0 and y + i <= 7:
            if Rules.detect_obstruction((x, y), (x - i, y + i), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x - i, y + i), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.append([x - i, y + i])
                break
            poss_moves.append([x - i, y + i])
            i += 1

        i = 1
        # All x moves above y
        while x + i <= 7 and y - i >= 0:
            if Rules.detect_obstruction((x, y), (x + i, y - i), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x + i, y - i), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.append([x + i, y - i])
                break
            poss_moves.append([x + i, y - i])
            i += 1

        i = 1
        # All x moves below x
        while x - i >= 0:
            if Rules.detect_obstruction((x, y), (x - i, y), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x - i, y), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.append([x - i, y])
                break
            poss_moves.append([x - i, y])
            i += 1

        i = 1
        # All x moves above x
        while (x + i) <= 7:
            if Rules.detect_obstruction((x, y), (x + i, y), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x + i, y), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.append([x + i, y])
                break
            poss_moves.append([x + i, y])
            i += 1

        i = 1
        # All y moves below y
        while y - i >= 0:
            if Rules.detect_obstruction((x, y), (x, y - i), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x, y - i), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.append([x, y - i])
                break
            poss_moves.append([x, y - i])
            i += 1
        i = 1
        # All x moves above y
        while (y + i) <= 7:
            if Rules.detect_obstruction((x, y), (x, y + i), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x, y + i), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.append([x, y + i])
                break
            poss_moves.append([x, y + i])
            i += 1

        # only do this line if not scanning opponent for check to avoid getting stuck in recursive loop
        if not scan_mode:
            poss_moves = self.chk_limit_moves(board, x, y, poss_moves)

        return poss_moves


class King(_Piece):
    def __init__(self, color):
        str_rep = PIECES.KING.value['str_rep']
        if color == COLORS.WHITE:
            str_rep = str_rep.upper()

        # Makes a piece with set values and images
        super().__init__(PIECES.KING.value['value'], color, str_rep)


    def get_moves(self, x, y, board, scan_mode=False):
        # If castle move is possible, store castle coordinates into parameters
        poss_moves = []

        # All moves top left
        if x - 1 >= 0 and y - 1 >= 0:
            if Rules.detect_obstruction((x, y), (x - 1, y - 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                poss_moves.append([x - 1, y - 1])

        # All moves bottom right
        if x + 1 <= 7 and y + 1 <= 7:
            if Rules.detect_obstruction((x, y), (x + 1, y + 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                poss_moves.append([x + 1, y + 1])

        # All moves bottom left
        if x - 1 >= 0 and y + 1 <= 7:
            if Rules.detect_obstruction((x, y), (x - 1, y + 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                poss_moves.append([x - 1, y + 1])

        # All moves top right
        if x + 1 <= 7 and y - 1 >= 0:
            if Rules.detect_obstruction((x, y), (x + 1, y - 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                poss_moves.append([x + 1, y - 1])

        # All moves left
        if x - 1 >= 0:
            if Rules.detect_obstruction((x, y), (x - 1, y), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                poss_moves.append([x - 1, y])

        # All moves right
        if x + 1 <= 7:
            if Rules.detect_obstruction((x, y), (x + 1, y), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                poss_moves.append([x + 1, y])

        # All up
        if y - 1 >= 0:
            if Rules.detect_obstruction((x, y), (x, y - 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                poss_moves.append([x, y - 1])

        # All moves bottom
        if y + 1 <= 7:
            if Rules.detect_obstruction((x, y), (x, y + 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                poss_moves.append([x, y + 1])


        # Castling

        # If in check can't castle
        if not scan_mode:
            from game import Game
            probe_game = Game(turn=self.color, board=board, scan_mode=True)

        if scan_mode or not self.isin_check(x, y, probe_game):
            # White Piece
            if board[x, y].color == COLORS.WHITE:
                # The king must be at starting position with 0 move count
                if x == 4 and y == 7 and board[x, y].num_moves == 0:
                    # The rook on the left must be at starting position with 0 move count
                    if board[0, 7].piece.str_rep == 'R' and board[0, 7].num_moves == 0:
                        # there must not be anything blocking the path
                        if board[1, 7].piece.str_rep == '-' and \
                                board[2, 7].str_rep == '-' and \
                                board[3, 7].str_rep == '-':
                            # append move to possible moves
                            poss_moves.append([2, 7])
                            # add left castle to self
                            self.left_castle = 2, 7
                else:
                    # Reset once castle is not valid
                    self.left_castle = -1, -1

                if x == 4 and y == 7 and board[x, y].num_moves == 0:
                    # The rook on the right must be at starting position with 0 move count
                    if board[7, 7].str_rep == 'R' and board[7, 7].num_moves == 0:
                        # there must not be anything blocking the path
                        if board[5, 7].str_rep == '-' and \
                                board[6, 7].str_rep == '-':
                            # append move to possible moves
                            poss_moves.append([6, 7])
                            # add right castle to self
                            self.right_castle = 6, 7
                else:
                    # Reset once castle is not valid
                    self.right_castle = -1, -1
            # Black Piece
            if board[x, y].color == COLORS.BLACK:
                # The king must be at starting position with 0 move count
                if x == 4 and y == 0 and board[x, y].num_moves == 0:
                    # The rook on the left must be at starting position with 0 move count
                    if board[0, 0].str_rep == 'r' and board[0, 0].num_moves == 0:
                        # there must not be anything blocking the path
                        if board[1, 0].str_rep == '-' and \
                                board[2, 0].str_rep == '-' and \
                                board[3, 0].str_rep == '-':
                            # append move to possible moves
                            poss_moves.append([2, 0])
                            # add left castle to self
                            self.left_castle = 2, 0
                else:
                    # Reset once castle is not valid
                    self.left_castle = -1, -1

                if x == 4 and y == 0 and board[x, y].num_moves == 0:
                    # The rook on the right must be at starting position with 0 move count
                    if board[7, 0].str_rep == 'r' and board[7, 0].num_moves == 0:
                        # there must not be anything blocking the path
                        if board[5, 0].str_rep == '-' and \
                                board[6, 0].str_rep == '-':
                            # append move to possible moves
                            poss_moves.append([6, 0])
                            # add right castle to self
                            self.right_castle = 6, 0
                else:
                    # Reset once castle is not valid
                    self.right_castle = -1, -1

        # only do this line if not scanning opponent for check to avoid getting stuck in recursive loop
        if not scan_mode:
            poss_moves = self.chk_limit_moves(board, x, y, poss_moves)


        return poss_moves

    # Private: Limits possible moves based on check cases
    def chk_limit_moves(self, board, myx, myy, poss_moves):
        # Make a copy of the current game using the board and turn
        # ** NOT USING DEEP COPY TO SAVE MEM AND SPEED
        from game import Game
        if self.color == COLORS.WHITE:
            probe_game = Game(turn=COLORS.BLACK, board=board, scan_mode=True)
        else:
            probe_game = Game(turn=COLORS.WHITE, board=board, scan_mode=True)

        bad_moves = []

        # Skip if king can't move
        if not poss_moves:
            return []

        # Loop through all pieces on the board
        for y in range(8):
            for x in range(8):
                # Advance each opponent piece and save possible moves
                op_moves = probe_game.get_next_poss_moves(x, y)

                # If the piece is a pawn, add the left and right capture into op_moves
                # and remove the move in front of the pawn
                if probe_game.turn == COLORS.BLACK and board[x, y].str_rep == 'p':
                    if x < 7 and y <= 7:
                        op_moves.append([x + 1, y + 1])
                    if x > 0 and y <= 7:
                        op_moves.append([x - 1, y + 1])
                    if y <= 5:
                        try:
                            op_moves.remove([x, y + 1])
                            op_moves.remove([x, y + 2])
                        except ValueError:
                            pass
                elif probe_game.turn == COLORS.WHITE and board[x, y].str_rep == 'P':
                    if x < 7 and y >= 0:
                        op_moves.append([x + 1, y - 1])
                    if x > 0 and y >= 0:
                        op_moves.append([x - 1, y - 1])
                    if y >= 2:
                        try:
                            op_moves.remove([x, y - 1])
                            op_moves.remove([x, y - 2])
                        except ValueError:
                            pass

                # loop through all possible moves
                for op_move in op_moves:
                    # if the move is the same as the king's moves
                    if op_move in poss_moves:
                        # Save the move in a list
                        bad_moves.append(op_move)

        # If there is any move beside the king that cant be captured but not picked up by the check limit
        # Capture the piece and check for check
        probe_game.switch_turn()

        # loop all moves surrounding king
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = myx + i
                y = myy + j
                # If there is a piece of the opposite colour
                if (x in range(8)) and (y in range(8)) and board[x, y].color != self.color:
                    # Try the move
                    probe_game.full_move(myx, myy, x, y)

                    # switch to king's turn to check move
                    probe_game.switch_turn()
                    # check if the king is in check
                    if self.isin_check(x, y, probe_game):
                        # if it is add to bad moves
                        bad_moves.append([x, y])
                    # switch back
                    probe_game.switch_turn()
                    # undo move
                    probe_game.undo_move()

        # Finding difference between 2 sets
        def diff(li1, li2):
            for i in li2:
                if i in li1:
                    li1.remove(i)
            return li1

        # Diff the 2 sets
        poss_moves = diff(poss_moves, bad_moves)

        # delete the new game
        del probe_game

        # Return poss_moves
        return poss_moves

    # Checks if itself is in check move from is in
    # MUST BE IN THE TURN THAT YOU ARE CHECKING
    def isin_check(self, king_x, king_y, curr_game):
        # switches turn into the opponent's turn to check
        from game import Game
        if curr_game.turn == COLORS.BLACK:
            probe_game = Game(turn=COLORS.WHITE, board=curr_game.board, scan_mode=True, prev_game_state=curr_game.game_state)
        else:
            probe_game = Game(turn=COLORS.BLACK, board=curr_game.board, scan_mode=True, prev_game_state=curr_game.game_state)
        # Loop through all pieces on the board
        for y in range(8):
            for x in range(8):
                # Advance each opponent piece and save possible moves
                op_moves = probe_game.get_next_poss_moves(x, y)

                # loop through all possible moves
                for op_move in op_moves:
                    opx, opy = op_move
                    # if the move will hit the king
                    if king_x == opx and king_y == opy:
                        # Save the move in a list
                        return True
        # switches turn back
        return False

    # Check for whether castle move was made
    @staticmethod
    def is_castle(x, y, board):
        # White Piece
        if board[x, y].color == COLORS.WHITE:
            # The king must be at starting position with 0 move count
            if x == 4 and y == 7 and board[x, y].num_moves == 0:
                # The rook on the left must be at starting position with 0 move count
                if board[0, 7].piece.str_rep == 'R' and board[0, 7].num_moves == 0:
                    # there must not be anything blocking the path
                    if board[1, 7].piece.str_rep == '-' and \
                            board[2, 7].str_rep == '-' and \
                            board[3, 7].str_rep == '-':
                        return Move.MoveType.LEFT_CASTLE

            if x == 4 and y == 7 and board[x, y].num_moves == 0:
                # The rook on the right must be at starting position with 0 move count
                if board[7, 7].str_rep == 'R' and board[7, 7].num_moves == 0:
                    # there must not be anything blocking the path
                    if board[5, 7].str_rep == '-' and \
                            board[6, 7].str_rep == '-':
                        return Move.MoveType.RIGHT_CASTLE
        # Black Piece
        if board[x, y].color == COLORS.BLACK:
            # The king must be at starting position with 0 move count
            if x == 4 and y == 0 and board[x, y].num_moves == 0:
                # The rook on the left must be at starting position with 0 move count
                if board[0, 0].str_rep == 'r' and board[0, 0].num_moves == 0:
                    # there must not be anything blocking the path
                    if board[1, 0].str_rep == '-' and \
                            board[2, 0].str_rep == '-' and \
                            board[3, 0].str_rep == '-':
                        return Move.MoveType.LEFT_CASTLE

            if x == 4 and y == 0 and board[x, y].num_moves == 0:
                # The rook on the right must be at starting position with 0 move count
                if board[7, 0].str_rep == 'r' and board[7, 0].num_moves == 0:
                    # there must not be anything blocking the path
                    if board[5, 0].str_rep == '-' and \
                            board[6, 0].str_rep == '-':
                        return Move.MoveType.RIGHT_CASTLE

# TODO: Try take out blank piece
class Blank(_Piece):
    def __init__(self, color=None):
        super().__init__(0, None, PIECES.BLANK.value['str_rep'])

class PieceLibrary(object):
    """
    Class the holds a copy of all the pieces
    """
    class PieceLibraryException(Exception):
        """Exception for handling piece creation"""
        pass

    PIECE_MAPPING = {
            PIECES.ROOK : Rook,
            PIECES.KNIGHT : Knight,
            PIECES.BISHOP : Bishop,
            PIECES.QUEEN : Queen,
            PIECES.KING : King,
            PIECES.PAWN : Pawn,
            PIECES.BLANK : Blank,
            }
    COLOR_LIST = COLORS

    LIBRARY = defaultdict(dict)
    for piece, piece_obj in PIECE_MAPPING.items():
        for color in COLOR_LIST:
            LIBRARY[piece][color] = piece_obj(color)

    @classmethod
    def get_piece_and_color_by_str_rep(cls, str_rep):
        """
        Returns the piece and color information based on the string rep
        """
        # Get piece by the PIECES str rep, kind of hacky
        try:
            piece = PIECES.get_by_str_rep(str_rep.lower())
        except KeyError:
            raise cls.PieceLibraryException('Could not find piece with value %s' % str_rep)

        if str_rep.isupper():
            color = cls.COLOR_LIST.WHITE
        else:
            color = cls.COLOR_LIST.BLACK

        return piece, color
        
    @classmethod
    def get_piece_ref(cls, piece, color):
        if piece and color:
            return cls.LIBRARY[piece][color]
        else:
            return None

    @classmethod
    def get_piece_copy(cls, piece, color):
        if piece and color:
            return cls.PIECE_MAPPING[piece](color)
        else:
            return None

