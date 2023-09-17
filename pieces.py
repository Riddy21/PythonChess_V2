from typing import Any
from collections import defaultdict
import uuid
from settings import *
from rules import Rules

# TODO: Use sets and tuples for poss moves

# Abstract Piece Class
class _Piece(object):
    def __init__(self, value, color, str_rep):
        # initiate variables
        self.value = value
        self.color = color
        self.str_rep = str_rep

    def get_moves(self, x, y, board, scan_mode=False):
        return []

    # Private: Limits possible moves based on check cases
    def chk_limit_moves(self, board, myx, myy, poss_moves):
        from game import Game
        # Make a copy of the current game using the board and turn
        probe_game = Game(turn=self.color, board=board, scan_mode=True)

        bad_moves = set()

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
            if Rules.isin_check((king_x, king_y), probe_game.board):
                bad_moves.add((my_move[0], my_move[1]))

            # switches back
            probe_game.switch_turn()

            probe_game.undo_move()

            probe_game.handle_move(myx, myy)

        probe_game.undo_move()

        # Diff the 2 sets
        poss_moves = poss_moves.difference(bad_moves)

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

    # Pawn move set given the location of the piece
    def get_moves(self, x, y, board, scan_mode=False):
        poss_moves = set()

        poss_moves = poss_moves.union(Rules.get_pawn_moves((x, y), board))

        poss_moves = poss_moves.union(Rules.get_enpassante_moves((x, y), board))

        # only do this line if not scanning opponent for check to avoid getting stuck in recursive loop
        if not scan_mode:
            poss_moves = self.chk_limit_moves(board, x, y, poss_moves)

        return poss_moves

class Rook(_Piece):
    def __init__(self, color):
        str_rep = PIECES.ROOK.value['str_rep']
        if color == COLORS.WHITE:
            str_rep = str_rep.upper()
        # Makes a piece with set values and images
        super().__init__(PIECES.ROOK.value['value'], color, str_rep)

    # Returns possible moves this piece can make
    def get_moves(self, x, y, board, scan_mode=False):
        poss_moves = set()

        poss_moves = poss_moves.union(Rules.get_orthogonal_moves((x, y), board))

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
        poss_moves = set()
        poss_moves = poss_moves.union(Rules.get_knight_moves((x, y), board))
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
        poss_moves = set()

        poss_moves = poss_moves.union(Rules.get_diagonal_moves((x, y), board))

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
        poss_moves = set()

        poss_moves = poss_moves.union(Rules.get_diagonal_moves((x, y), board))
        poss_moves = poss_moves.union(Rules.get_orthogonal_moves((x, y), board))

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
        poss_moves = set()

        poss_moves = poss_moves.union(Rules.get_diagonal_moves((x, y), board, spread=1))
        poss_moves = poss_moves.union(Rules.get_orthogonal_moves((x, y), board, spread=1))

        poss_moves = poss_moves.union(Rules.get_left_castle_moves((x, y), board))
        poss_moves = poss_moves.union(Rules.get_right_castle_moves((x, y), board))

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

        bad_moves = set()

        # Skip if king can't move
        if not poss_moves:
            return set()

        # Loop through all pieces on the board
        for y in range(8):
            for x in range(8):
                # Advance each opponent piece and save possible moves
                op_moves = probe_game.get_next_poss_moves(x, y)

                # If the piece is a pawn, add the left and right capture into op_moves
                # and remove the move in front of the pawn
                if probe_game.turn == COLORS.BLACK and board[x, y].str_rep == 'p':
                    if x < 7 and y <= 7:
                        op_moves.add((x + 1, y + 1))
                    if x > 0 and y <= 7:
                        op_moves.add((x - 1, y + 1))
                    if y <= 5:
                        try:
                            op_moves.remove((x, y + 1))
                            op_moves.remove((x, y + 2))
                        except KeyError:
                            pass
                elif probe_game.turn == COLORS.WHITE and board[x, y].str_rep == 'P':
                    if x < 7 and y >= 0:
                        op_moves.add((x + 1, y - 1))
                    if x > 0 and y >= 0:
                        op_moves.add((x - 1, y - 1))
                    if y >= 2:
                        try:
                            op_moves.remove((x, y - 1))
                            op_moves.remove((x, y - 2))
                        except KeyError:
                            pass

                # loop through all possible moves
                for op_move in op_moves:
                    # if the move is the same as the king's moves
                    if op_move in poss_moves:
                        # Save the move in a list
                        bad_moves.add(tuple(op_move))

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
                    if Rules.isin_check((x, y), probe_game.board):
                        # if it is add to bad moves
                        bad_moves.add((x, y))
                    # switch back
                    probe_game.switch_turn()
                    # undo move
                    probe_game.undo_move()


        # Diff the 2 sets
        poss_moves = poss_moves.difference(bad_moves)

        # delete the new game
        del probe_game

        # Return poss_moves
        return poss_moves

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

