from enum import Enum

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

    @staticmethod
    def chk_limit_moves(board, x, y):
        pass
