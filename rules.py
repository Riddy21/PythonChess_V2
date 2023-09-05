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
    @classmethod
    def is_castle(cls, x, y, board):
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
                        return cls.MoveType.LEFT_CASTLE

            if x == 4 and y == 7 and board[x, y].num_moves == 0:
                # The rook on the right must be at starting position with 0 move count
                if board[7, 7].str_rep == 'R' and board[7, 7].num_moves == 0:
                    # there must not be anything blocking the path
                    if board[5, 7].str_rep == '-' and \
                            board[6, 7].str_rep == '-':
                        return cls.MoveType.RIGHT_CASTLE
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
                        return cls.MoveType.LEFT_CASTLE

            if x == 4 and y == 0 and board[x, y].num_moves == 0:
                # The rook on the right must be at starting position with 0 move count
                if board[7, 0].str_rep == 'r' and board[7, 0].num_moves == 0:
                    # there must not be anything blocking the path
                    if board[5, 0].str_rep == '-' and \
                            board[6, 0].str_rep == '-':
                        return cls.MoveType.RIGHT_CASTLE

    @staticmethod
    def chk_limit_moves(board, x, y, poss_moves):
        bad_moves = set()
        # Copy the board given
        #FIXME: remove copy later
        probe_board = board.copy()

        # Do the move
        from move import Move
        move = Move(board, x, y, poss_moves)

        

        


