from enum import Enum
import math
from settings import *

class Rules(object):
    class ObstructionType(Enum):
        """
        Enumerates the types of obstructions in the chess game
        """
        SELF_OBSTRUCTED = 'self obstructed'
        OPPONENT_OBSTRUCTED = 'opponent obstructed'
        UNOBSTRUCTED = 'unobstructed'

    @staticmethod
    def detect_obstruction(source, target, board):
        """
        Detect if the piece is obstructed
        """
        # make sure its not checking its self
        if source != target:
            # Same colour pieces
            if board[source].color == board[target].color:
                return Rules.ObstructionType.SELF_OBSTRUCTED
            # opponent pieces
            elif board[target].color != None:
                return Rules.ObstructionType.OPPONENT_OBSTRUCTED
            else:
                return Rules.ObstructionType.UNOBSTRUCTED

    @staticmethod
    def get_pawn_moves(source, board):
        """
        Gets the moves that pawns usually make
        """
        x, y = source
        poss_moves = set()

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
                    poss_moves.add((x, y + i))
                    break

                # add the position and increment counter
                poss_moves.add((x, y + i))
                i += 1

            # NOTE: ONLY WHEN SCAN MODE AND KING CAN BE CAPTURED
            # Sideways Capture, ** if in scan mode, side captures count even if there is no piece currently there
            if x < 7 and y < 7 and board[x + 1, y + 1].color == COLORS.WHITE:
                poss_moves.add((x + 1, y + 1))
            if x > 0 and y < 7 and board[x - 1, y + 1].color == COLORS.WHITE:
                poss_moves.add((x - 1, y + 1))

        # white moves
        elif board[x, y].color == COLORS.WHITE:
            i = 1

            while i <= 2 and y - i >= 0:
                piece_detect = Rules.detect_obstruction((x, y), (x, y - i), board)
                if piece_detect != Rules.ObstructionType.UNOBSTRUCTED:
                    break

                # no 2nd move on 2nd turn
                elif board[x, y].num_moves >= 1:
                    poss_moves.add((x, y - i))
                    break

                # add the position and increment counter
                poss_moves.add((x, y - i))
                i += 1

            # NOTE: ONLY WHEN SCAN MODE AND KING CAN BE CAPTURED
            # Sideways Capture
            if x < 7 and y > 0 and board[x + 1, y - 1].color == COLORS.BLACK:
                poss_moves.add((x + 1, y - 1))
            if x > 0 and y > 0 and board[x - 1, y - 1].color == COLORS.BLACK:
                poss_moves.add((x - 1, y - 1))

        return poss_moves


    @staticmethod
    def get_left_castle_moves(source, board):
        """
        Gets the castle moves if they are valid
        """
        source = tuple(source)
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
                        return {(2, 7)}
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
                        return {(2, 0)}

        return {}

    @staticmethod
    def get_right_castle_moves(source, board):
        """
        Gets the castle moves if they are valid
        """
        source = tuple(source)
        # White Piece
        if board[source].color == COLORS.WHITE:
            # The king must be at starting position with 0 move count
            if source == (4, 7) and board[source].num_moves == 0:
                # The rook on the left must be at starting position with 0 move count
                if board[7, 7].str_rep == 'R' and board[7, 7].num_moves == 0:
                    # there must not be anything blocking the path
                    if board[5, 7].str_rep == '-' and \
                            board[6, 7].str_rep == '-':
                        return {(6, 7)}
        # Black Piece
        if board[source].color == COLORS.BLACK:
            # The king must be at starting position with 0 move count
            if source == (4, 0) and board[source].num_moves == 0:
                # The rook on the left must be at starting position with 0 move count
                if board[7, 0].str_rep == 'r' and board[7, 0].num_moves == 0:
                    # there must not be anything blocking the path
                    if board[5, 0].str_rep == '-' and \
                            board[6, 0].str_rep == '-':
                        return {(6, 0)}

        return {}

    @staticmethod
    def get_enpassante_moves(source, board):
        source = tuple(source)
        x, y = source
        poss_moves = set()
        if board[source].color == COLORS.WHITE and y == 3:
            if (x + 1 in range(8)) and board[x + 1, y].color == COLORS.BLACK and \
                    board[x + 1, y].num_moves == 1:
                if Rules.detect_obstruction((x, y), (x + 1, y - 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.add((x+1, y-1))
            if (x - 1 in range(8)) and board[x - 1, y].color == COLORS.BLACK and \
                    board[x - 1, y].num_moves == 1:
                if Rules.detect_obstruction((x, y), (x - 1, y - 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.add((x-1, y-1))
        elif board[source].color == COLORS.BLACK and y == 4:
            if (x + 1 in range(8)) and board[x + 1, y].color == COLORS.WHITE and \
                    board[x + 1, y].num_moves == 1:
                if Rules.detect_obstruction((x, y), (x + 1, y + 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.add((x+1, y+1))
            if (x - 1 in range(8)) and board[x - 1, y].color == COLORS.WHITE and \
                    board[x - 1, y].num_moves == 1:
                if Rules.detect_obstruction((x, y), (x - 1, y + 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.add((x-1, y+1))

        return poss_moves

    @staticmethod
    def get_orthogonal_moves(source, board, spread=math.inf):
        """
        Get moves horizontally and vertically
        """
        x, y = source
        poss_moves = set()

        i = 1
        # All x moves below x
        while x - i >= 0 and i <= spread:
            if Rules.detect_obstruction((x, y), (x - i, y), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x - i, y), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.add((x - i, y))
                break
            poss_moves.add((x - i, y))
            i += 1

        i = 1
        # All x moves above x
        while (x + i) <= 7 and i <= spread:
            if Rules.detect_obstruction((x, y), (x + i, y), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x + i, y), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.add((x + i, y))
                break
            poss_moves.add((x + i, y))
            i += 1

        i = 1
        # All y moves below y
        while y - i >= 0 and i <= spread:
            if Rules.detect_obstruction((x, y), (x, y - i), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x, y - i), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.add((x, y - i))
                break
            poss_moves.add((x, y - i))
            i += 1
        i = 1
        # All x moves above y
        while (y + i) <= 7 and i <= spread:
            if Rules.detect_obstruction((x, y), (x, y + i), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x, y + i), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.add((x, y + i))
                break
            poss_moves.add((x, y + i))
            i += 1

        return poss_moves

    @staticmethod
    def get_knight_moves(source, board):
        """
        Get knight hop moves
        """
        x, y = source
        poss_moves = set()

        if x + 2 <= 7:
            if y + 1 <= 7:
                if Rules.detect_obstruction((x, y), (x + 2, y + 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.add((x + 2, y + 1))
            if y - 1 >= 0:
                if Rules.detect_obstruction((x, y), (x + 2, y - 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.add((x + 2, y - 1))

        if x + 1 <= 7:
            if y + 2 <= 7:
                if Rules.detect_obstruction((x, y), (x + 1, y + 2), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.add((x + 1, y + 2))
            if y - 2 >= 0:
                if Rules.detect_obstruction((x, y), (x + 1, y - 2), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.add((x + 1, y - 2))
        if x - 2 >= 0:
            if y + 1 <= 7:
                if Rules.detect_obstruction((x, y), (x - 2, y + 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.add((x - 2, y + 1))
            if y - 1 >= 0:
                if Rules.detect_obstruction((x, y), (x - 2, y - 1), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.add((x - 2, y - 1))
        if x - 1 >= 0:
            if y + 2 <= 7:
                if Rules.detect_obstruction((x, y), (x - 1, y + 2), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.add((x - 1, y + 2))
            if y - 2 >= 0:
                if Rules.detect_obstruction((x, y), (x - 1, y - 2), board) != Rules.ObstructionType.SELF_OBSTRUCTED:
                    poss_moves.add((x - 1, y - 2))

        return poss_moves

    @staticmethod
    def get_diagonal_moves(source, board, spread=math.inf):
        """
        Get diagonal movements (bishop) with the spread being how many moves out
        """
        poss_moves = set()
        x, y = source

        i = 1
        # All moves top left
        while x - i >= 0 and y - i >= 0 and i <=spread:
            if Rules.detect_obstruction((x, y), (x - i, y - i), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x - i, y - i), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.add((x - i, y - i))
                break
            poss_moves.add((x - i, y - i))
            i += 1

        i = 1
        # All moves bottom right
        while x + i <= 7 and y + i <= 7 and i <= spread:
            if Rules.detect_obstruction((x, y), (x + i, y + i), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x + i, y + i), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.add((x + i, y + i))
                break
            poss_moves.add((x + i, y + i))
            i += 1

        i = 1
        # All y moves below y
        while x - i >= 0 and y + i <= 7 and i <= spread:
            if Rules.detect_obstruction((x, y), (x - i, y + i), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x - i, y + i), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.add((x - i, y + i))
                break
            poss_moves.add((x - i, y + i))
            i += 1

        i = 1
        # All x moves above y
        while x + i <= 7 and y - i >= 0 and i <= spread:
            if Rules.detect_obstruction((x, y), (x + i, y - i), board) == Rules.ObstructionType.SELF_OBSTRUCTED:
                break
            elif Rules.detect_obstruction((x, y), (x + i, y - i), board) == Rules.ObstructionType.OPPONENT_OBSTRUCTED:
                poss_moves.add((x + i, y - i))
                break
            poss_moves.add((x + i, y - i))
            i += 1

        return poss_moves

    @staticmethod
    def isin_check(king_loc, board):
        if board[king_loc].color == COLORS.WHITE:
            turn = COLORS.BLACK
        else:
            turn = COLORS.WHITE

        from move import Move
        for (x, y), square in board:
            if square.color == turn:
                # Check possible moves
                poss_moves = board[(x, y)].get_moves(x, y, board, scan_mode=True)
                if tuple(king_loc) in poss_moves:
                    return True

        return False

    # Check for whether castle move was made
    @staticmethod
    def is_left_castle(source, target, board):
        source = tuple(source)
        target = tuple(target)
        if target in Rules.get_left_castle_moves(source, board):
            return True
        return False

    # Check for whether castle move was made
    @staticmethod
    def is_right_castle(source, target, board):
        source = tuple(source)
        target = tuple(target)
        if target in Rules.get_right_castle_moves(source, board):
            return True
        return False

    @staticmethod
    def is_enpassant(source, target, board):
        source = tuple(source)
        target = tuple(target)
        if target in Rules.get_enpassante_moves(source, board):
            return True
        return False


    # TODO: Convert pawn promo to a move that returns multiple options for moves
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
    def chk_limit_moves(source, board, poss_moves):
        from pieces import King
        from board import BoardManager
        from move import Move
        probe_board = board.copy()
        
        # Iterate through possible moves and check if any puts you in check
        remove_moves = set()
        for move in poss_moves:
            # Do the move
            move_obj = Move.full_move(source, move, probe_board)
            # check if in check
            king_location = BoardManager.find(King, probe_board, probe_board[move].color, num=1).pop()
            if Rules.isin_check(king_location, probe_board):
                remove_moves.add(move)
            # undo the move
            move_obj.undo_move(probe_board)

        poss_moves -= remove_moves
        
    @staticmethod
    def get_game_state(board):
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
        from move import Move

        black_can_move = False
        white_can_move = False
        black_in_check = False
        white_in_check = False

        num_pieces = 0

        # loops through all pieces on the board
        for (x, y), item in board.items():
            piece = item.piece
            if piece.color != None:
                num_pieces += 1
            # pawn promo check
            if y == 0 and piece.str_rep == 'P':
                return 'white pawn promo'

            if y == BOARD_HEIGHT - 1 and piece.str_rep == 'p':
                return 'black pawn promo'
            # If the piece is the king
            if piece.str_rep == 'k':
                # Test if it is in check
                black_in_check = Rules.isin_check((x, y), board)
            if piece.str_rep == 'K':
                white_in_check = Rules.isin_check((x, y), board)
            # Try to move it and if there are no more moves
            if Move.get_poss_moves(board, piece.color, x, y):
                if piece.color == COLORS.WHITE:
                    # set can move to true and break out
                    white_can_move = True

                else:
                    black_can_move = True

        if black_in_check and not black_can_move:
            return 'black checkmate'
        elif white_in_check and not white_can_move:
            return 'white checkmate'
        elif black_in_check:
            return 'black check'
        elif white_in_check:
            return 'white check'
        elif not white_can_move:
            return 'white stalemate'
        elif not black_can_move:
            return 'black stalemate'
        elif num_pieces == 2:
            return 'stalemate'
        else:
            return 'normal'
        


        

        


