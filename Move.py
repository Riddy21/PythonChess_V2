from typing import Any

from Pieces import Blank, Bishop, King, Knight, Rook, Pawn, Queen


# Function for checking if player picked a piece of the right colour and type
def is_valid_selection(board, turn, x, y):
    if getattr(board[x][y], 'str_rep') != "-" and getattr(board[x][y], 'colour') == turn:
        return True
    print("Invalid selection")
    return False


# TODO: Class to record moves and change game board
class Move():
    # init
    def __init__(self, board, turn, x, y):
        # Parameter for move stage
        self.move_stage = "selected"

        # Parameter for to location, initiate as 'move not finished yet'
        self.move_to = -1, -1

        # Parameter for from location
        self.move_from = x, y

        # Parameters for move type
        self.move_type = "not set"

        # Parameter for Move color
        self.move_colour = board[x][y].colour

        # Parameter for turn colour
        self.turn_colour = turn

        # Parameter for possible next moves and set to the piece's move array
        self.poss_moves = board[x][y].get_moves(x, y, board)

        # Parameter for captured Piece
        self.captured = 'None'

        self.board_before = [[""] * 8 for i in range(8)]
        # Parameter for board in string rep before move
        for x in range(8):
            for y in range(8):
                self.board_before[x][y] = board[x][y].str_rep

    # validate move and make the move based on the end coordinates
    def make_move(self, board, x, y):

        # Tries to check if move is valid and returns the move type
        proposed_move = self._try_move(board, x, y)
        # Check if it is a valid move
        # ** Don't set move to until validated
        if proposed_move == -1:
            print("invalid move")
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

        # Make move
        frox = self.move_from[0]
        froy = self.move_from[1]
        tox = self.move_to[0]
        toy = self.move_to[1]

        # Add move count to moved piece
        setattr(board[frox][froy], 'move_count', getattr(board[frox][froy], 'move_count') + 1)

        if self.move_type == 'capture':
            print('capture: from %d,%d to %d,%d' % (frox, froy, tox, toy))
            self.captured = board[tox][toy].str_rep
            board[tox][toy] = board[frox][froy]
            board[frox][froy] = Blank()

        elif self.move_type == 'move':
            print('move: from %d,%d to %d,%d' % (frox, froy, tox, toy))
            board[tox][toy], board[frox][froy] = board[frox][froy], board[tox][toy]

        # TODO: finish other move types

    # TODO: Undo a move
    def undo_move(self):
        # undo move using the board_before and capture pieces
        pass

    # Private: Validate move
    def is_valid_move(self, x, y):
        return True
        # TODO: Check moves based on highlights that each piece allows

    # Tries move and returns move type if valid
    def _try_move(self, board, x, y):

        # Check if valid move on highlights
        if not self.is_valid_move(x, y):
            return -1

        # Check what type of move based on the pieces unique rule set
        # Check for castling, enpassente and pawn promotion
        # If it does not fullfill requirements, return -1

        # If is capture
        if getattr(board[x][y], 'str_rep') != "-":
            return 'capture'
        # If is normal move
        else:
            return 'move'

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    # TODO: make converter from str_rep to object
