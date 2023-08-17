from settings import *
from abc import abstractmethod, ABC
from moves import Move

class Piece(ABC):
    """
    Parent class piece that contains all properties shared across all chess pieces
    """
    def __init__(self, value: int, color: COLORS, str_rep: str):
        """
        Constructor
        """
        self.value = value
        self.color = color
        self.str_rep = str_rep

    @abstractmethod
    def get_moves(location, board):
        """
        Default moves possible for that piece without considering the board or position
        """
        pass

    def __str__(self):
        return self.str_rep

class Pawn(Piece):
    """
    Pawn object
    """
    def __init__(self, color):
        """
        Constructor
        """
        super().__init__(PIECES.PAWN.value['value'], color, PIECES.PAWN.value['str_rep'])

    @staticmethod
    def get_moves(location, board):
        """
        Return a list of move objects detailing which moves are possible
        """
        poss_moves = []

        # Black moves
        if getattr(board[x, y].piece, 'colour') == 'black':
            i = 1

            # Do Move detection
            while i <= 2 and y + i <= 7:
                piece_detect = self._piece_detect(x, y, x, y + i, board)
                # piece in front blocks move
                if getattr(board[x, y + i].piece, 'colour') == 'white':
                    break

                # basic
                elif piece_detect == 'self obstructed':
                    break

                elif piece_detect == 'opponent obstructed':
                    break

                # no 2nd move on 2nd turn
                if self.move_count >= 1:
                    poss_moves.append([x, y + i])
                    break

                # add the position and increment counter
                poss_moves.append([x, y + i])
                i += 1

            # NOTE: ONLY WHEN SCAN MODE AND KING CAN BE CAPTURED
            # Sideways Capture, ** if in scan mode, side captures count even if there is no piece currently there
            if x < 7 and y < 7 and getattr(board[x + 1, y + 1].piece, 'colour') == 'white':
                poss_moves.append([x + 1, y + 1])
            if x > 0 and y < 7 and getattr(board[x - 1, y + 1].piece, 'colour') == 'white':
                poss_moves.append([x - 1, y + 1])

        # white moves
        elif getattr(board[x, y].piece, 'colour') == 'white':
            i = 1

            while i <= 2 and y - i >= 0:
                piece_detect = self._piece_detect(x, y, x, y - i, board)

                # piece in front blocks move
                if getattr(board[x, y - i].piece, 'colour') == 'black':
                    break

                # basic
                elif piece_detect == 'self obstructed':
                    break

                elif piece_detect == 'opponent obstructed':
                    break

                # no 2nd move on 2nd turn
                elif self.move_count >= 1:
                    poss_moves.append([x, y - i])
                    break

                # add the position and increment counter
                poss_moves.append([x, y - i])
                i += 1

            # NOTE: ONLY WHEN SCAN MODE AND KING CAN BE CAPTURED
            # Sideways Capture
            if x < 7 and y > 0 and getattr(board[x + 1, y - 1].piece, 'colour') == 'black':
                poss_moves.append([x + 1, y - 1])
            if x > 0 and y > 0 and getattr(board[x - 1, y - 1].piece, 'colour') == 'black':
                poss_moves.append([x - 1, y - 1])

        # enPassante
        if self.colour == 'white' and y == 3:
            if (x + 1 in range(8)) and getattr(board[x + 1, y].piece, 'colour') == 'black' and \
                    getattr(board[x + 1, y].piece, 'move_count') == 1 and \
                    getattr(board[x + 1, y].piece, 'move_num_history')[-1] == (self.move_num_history[-1] - 1):
                if self._piece_detect(x, y, x + 1, y - 1, board) == 'opponent obstructed' or \
                        self._piece_detect(x, y, x + 1, y - 1, board) == 'unobstructed':
                    poss_moves.append([x + 1, y - 1])
                    self.enpassant_pos.append([x + 1, y - 1])
            if (x - 1 in range(8)) and getattr(board[x - 1, y].piece, 'colour') == 'black' and \
                    getattr(board[x - 1, y].piece, 'move_count') == 1 and \
                    getattr(board[x - 1, y].piece, 'move_num_history')[-1] == (self.move_num_history[-1] - 1):
                if self._piece_detect(x, y, x - 1, y - 1, board) == 'opponent obstructed' or \
                        self._piece_detect(x, y, x - 1, y - 1, board) == 'unobstructed':
                    poss_moves.append([x - 1, y - 1])
                    self.enpassant_pos.append([x - 1, y - 1])
        elif self.colour == 'black' and y == 4:
            if (x + 1 in range(8)) and getattr(board[x + 1, y].piece, 'colour') == 'white' and \
                    getattr(board[x + 1, y].piece, 'move_count') == 1 and \
                    getattr(board[x + 1, y].piece, 'move_num_history')[-1] == (self.move_num_history[-1] - 1):
                if self._piece_detect(x, y, x + 1, y + 1, board) == 'opponent obstructed' or \
                        self._piece_detect(x, y, x + 1, y + 1, board) == 'unobstructed':
                    poss_moves.append([x + 1, y + 1])
                    self.enpassant_pos.append([x + 1, y + 1])
            if (x - 1 in range(8)) and getattr(board[x - 1, y].piece, 'colour') == 'white' and \
                    getattr(board[x - 1, y].piece, 'move_count') == 1 and \
                    getattr(board[x - 1, y].piece, 'move_num_history')[-1] == (self.move_num_history[-1] - 1):
                if self._piece_detect(x, y, x - 1, y + 1, board) == 'opponent obstructed' or \
                        self._piece_detect(x, y, x - 1, y + 1, board) == 'unobstructed':
                    poss_moves.append([x - 1, y + 1])
                    self.enpassant_pos.append([x - 1, y + 1])

        return poss_moves

