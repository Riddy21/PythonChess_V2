from enum import Enum
from settings import *

class Rules(object):
    class MoveType(Enum):
        """
        Enumerates the types of moves in the chess game
        """
        LEFT_CASTLE = 'left_castle'
        RIGHT_CASTLE = 'right_castle'

    class ObstructionType(Enum):
        """
        Enumerates the types of obstructions in the chess game
        """
        SELF_OBSTRUCTED = 'self obstructed'
        OPPONENT_OBSTRUCTED = 'opponent obstructed'
        UNOBSTRUCTED = 'unobstructed'

    @classmethod
    def detect_obstruction(cls, source, target, board):
        """
        Detect if the piece is obstructed
        """
        # make sure its not checking its self
        if source != target:
            # Same colour pieces
            if board[source].color == board[target].color:
                return cls.ObstructionType.SELF_OBSTRUCTED
            # opponent pieces
            elif board[target].color != None:
                return cls.ObstructionType.OPPONENT_OBSTRUCTED
            else:
                return cls.ObstructionType.UNOBSTRUCTED

    @classmethod
    def isin_check(cls, king_loc, board):
        if board[king_loc].color == COLORS.WHITE:
            turn = COLORS.BLACK
        else:
            turn = COLORS.WHITE

        from move import Move
        for (x, y), square in board:
            if square.color == turn:
                # Check possible moves
                poss_moves = board[(x, y)].get_moves(x, y, board, scan_mode=True)
                if list(king_loc) in poss_moves:
                    return True

        return False

    # Check for whether castle move was made
    # FIXME: This is wrong, should be only when the move is a castle move
    @classmethod
    def is_castle(cls, source, target, board):
        source = tuple(source)
        target = tuple(target)
        # White Piece
        if board[source].color == COLORS.WHITE:
            # The king must be at starting position with 0 move count
            if source == (4, 7) and board[source].num_moves == 0:
                # The rook on the left must be at starting position with 0 move count
                if board[0, 7].piece.str_rep == 'R' and board[0, 7].num_moves == 0:
                    # there must not be anything blocking the path
                    if board[1, 7].piece.str_rep == '-' and \
                            board[2, 7].str_rep == '-' and \
                            board[3, 7].str_rep == '-':
                        if target == (2, 7):
                            return cls.MoveType.LEFT_CASTLE

                if board[7, 7].str_rep == 'R' and board[7, 7].num_moves == 0:
                    # there must not be anything blocking the path
                    if board[5, 7].str_rep == '-' and \
                            board[6, 7].str_rep == '-':
                        if target == (6, 7):
                            return cls.MoveType.RIGHT_CASTLE
        # Black Piece
        if board[source].color == COLORS.BLACK:
            # The king must be at starting position with 0 move count
            if source == (4, 0) and board[source].num_moves == 0:
                # The rook on the left must be at starting position with 0 move count
                if board[0, 0].str_rep == 'r' and board[0, 0].num_moves == 0:
                    # there must not be anything blocking the path
                    if board[1, 0].str_rep == '-' and \
                            board[2, 0].str_rep == '-' and \
                            board[3, 0].str_rep == '-':
                        if target == (2, 0):
                            return cls.MoveType.LEFT_CASTLE

                if board[7, 0].str_rep == 'r' and board[7, 0].num_moves == 0:
                    # there must not be anything blocking the path
                    if board[5, 0].str_rep == '-' and \
                            board[6, 0].str_rep == '-':
                        if target == (6, 0):
                            return cls.MoveType.RIGHT_CASTLE

    @classmethod
    def is_enpassant(cls, source, target, board):
        source = tuple(source)
        x, y = source
        target = tuple(target)
        if board[source].color == COLORS.WHITE and y == 3:
            if (x + 1 in range(8)) and board[x + 1, y].color == COLORS.BLACK and \
                    board[x + 1, y].num_moves == 1:
                if cls.detect_obstruction((x, y), (x + 1, y - 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    if target == (x+1, y-1):
                        return True
            if (x - 1 in range(8)) and board[x - 1, y].color == COLORS.BLACK and \
                    board[x - 1, y].num_moves == 1:
                if Rules.detect_obstruction((x, y), (x - 1, y - 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    if target == (x-1, y-1):
                        return True
        elif board[source].color == COLORS.BLACK and y == 4:
            if (x + 1 in range(8)) and board[x + 1, y].color == COLORS.WHITE and \
                    board[x + 1, y].num_moves == 1:
                if Rules.detect_obstruction((x, y), (x + 1, y + 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    if target == (x+1, y+1):
                        return True
            if (x - 1 in range(8)) and board[x - 1, y].color == COLORS.WHITE and \
                    board[x - 1, y].num_moves == 1:
                if Rules.detect_obstruction((x, y), (x - 1, y + 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    if target == (x-1, y+1):
                        return True

        return False

    @staticmethod
    def is_pawn_promo(source, target, board):
        from pieces import Pawn
        if type(board[source].piece) != Pawn:
            return False
        _, y = target
        if y == 7 or y == 0:
            return True
        return False

    @staticmethod
    def chk_limit_moves(board, x, y, poss_moves):
        bad_moves = set()
        # Copy the board given
        #FIXME: remove copy later
        probe_board = board.copy()

        # Do the move
        from move import Move
        move = Move(board, x, y, poss_moves)

        

        


