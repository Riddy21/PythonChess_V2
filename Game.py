from typing import Any

from Pieces import Blank, Bishop, King, Knight, Rook, Pawn, Queen
from Move import Move


# Game class initiated when the game board is displayed
class Game:
    def __init__(self):
        # 2D array of pieces to represent board
        self.board = [[Blank()] * 8 for i in range(8)]

        # captured Pieces
        self.captured_white = []
        self.captured_black = []

        # stack of all old moves and current move
        # TODO: Make the list as a max undo of a certain length
        self.moves = []

        # string representing the turn colour of the game
        self.turn = 'white'

    # TODO: set board as a specific config
    def set_board(self):
        # set board by updating self.board
        self.board[0][0] = Rook('black')
        self.board[7][0] = Rook('black')
        self.board[1][0] = Knight('black')
        self.board[6][0] = Knight('black')
        self.board[2][0] = Bishop('black')
        self.board[5][0] = Bishop('black')
        self.board[3][0] = Queen('black')
        self.board[4][0] = King('black')
        self.board[0][1] = Pawn('black')
        self.board[1][1] = Pawn('black')
        self.board[2][1] = Pawn('black')
        self.board[3][1] = Pawn('black')
        self.board[4][1] = Pawn('black')
        self.board[5][1] = Pawn('black')
        self.board[6][1] = Pawn('black')
        self.board[7][1] = Pawn('black')
        self.board[0][7] = Rook('white')
        self.board[7][7] = Rook('white')
        self.board[1][7] = Knight('white')
        self.board[6][7] = Knight('white')
        self.board[2][7] = Bishop('white')
        self.board[5][7] = Bishop('white')
        self.board[3][7] = Queen('white')
        self.board[4][7] = King('white')
        self.board[0][6] = Pawn('white')
        self.board[1][6] = Pawn('white')
        self.board[2][6] = Pawn('white')
        self.board[3][6] = Pawn('white')
        self.board[4][6] = Pawn('white')
        self.board[5][6] = Pawn('white')
        self.board[6][6] = Pawn('white')
        self.board[7][6] = Pawn('white')

        # TODO: set according to config\

    # Function to switch turns
    def switch_turn(self):
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

    # TODO: Might be errors if the full Move is not valid... test later
    # Function to make complete move from to-coordinates and from-coordinates
    def full_move(self, frox, froy, tox, toy):
        if self.move_from(frox, froy) == -1:
            return -1
        if self.move_to(tox, toy) == -1:
            return -1

    # Function to check return what move stage we are at and handle move button
    def handle_move(self, x, y):
        # Check if moving from or moving to
        if len(self.moves) == 0 or getattr(self.moves[-1], 'move_stage') == 'moved':
            # If fresh board with no moves or move is finished move from this location
            self.move_from(x, y)
        else:
            # if the player selects a different piece to move
            if getattr(self.board[x][y], 'colour') == self.turn:
                # Removes move_id from piece and deletes move
                self.moves[-1].deselect_move(self.board)
                self.moves.pop(-1)
                self.move_from(x, y)
            # otherwise start a new move
            else:
                self.move_to(x, y)

    # Function to start move
    def move_from(self, x, y):
        # Check if it is a valid selection, if not, exit the function
        if not Move.is_valid_selection(self.board, self.turn, x, y):
            return -1

        # Create a new move and add to list and pass the len of move list as move id
        self.moves.append(Move(self.board, x, y, len(self.moves)))

    # Function to end move,
    def move_to(self, x, y):
        # Makes move on the most recent move, if invalid move, don't switch sides
        if self.moves[-1].make_move(self.board, x, y) == -1:
            return -1

        # Append captured pieces to the correct captured list
        captured_piece = getattr(self.moves[-1], 'captured')
        if captured_piece == 'None':
            pass
        elif getattr(captured_piece, 'colour') == 'black':
            self.captured_black.append(captured_piece)
        elif getattr(captured_piece, 'colour') == 'white':
            self.captured_white.append(captured_piece)

        self.switch_turn()

    # TODO: Function to undo move

    # TODO: Convert chess coords to int coords

    # TODO: Static: Converts Object board to string board

    # TODO: Static: Converts String board to Object board

    # TODO: print board in string format using string representation

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def __str__(self):
        str = ''

        # Add board string reps
        for y in range(8):
            for x in range(8):
                str += self.board[x][y].str_rep + ' '
            str += '\n'

        return str
