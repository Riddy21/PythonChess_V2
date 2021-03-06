from typing import Any
import sys, os
from Pieces import Blank, Bishop, King, Knight, Rook, Pawn, Queen
from Move import Move


# Game class initiated when the game board is displayed
class Game:
    def __init__(self, turn='white', board=None, moves=None, captured_white=None, captured_black=None, scan_mode=False):
        if captured_black is None:
            captured_black = []
        if captured_white is None:
            captured_white = []
        if moves is None:
            moves = []
        if board is None:
            board = []

        # 2D array of pieces to represent board
        self.board = board

        # captured Pieces
        self.captured_white = captured_white
        self.captured_black = captured_black

        # stack of all old moves and current move
        # TODO: Make the list as a max undo of a certain length
        self.moves = moves

        # string representing the turn colour of the game
        self.turn = turn

        # scan mode to stop recursive loop of checking check and checkmate
        self.scan_mode = scan_mode

        # TODO: Add functionality to set board from savefile
        # if board was not loaded by passing a parameter, set the board
        if not self.board:
            self.set_board()

        # games state
        self.game_state = 'normal'

    # TODO: set board as a specific config
    def set_board(self):
        # Create blank board
        self.board = [[Blank()] * 8 for i in range(8)]
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

    # Function to change pawn promotion piece
    def make_pawn_promo(self, promo_type):
        self.moves[-1].make_pawn_promo(promo_type, self.board)

    # Function to undo a move and remove it from the move list
    def undo_move(self):
        # undo move and delete move
        if len(self.moves) != 0:
            # if in selection mode
            if getattr(self.moves[-1], 'move_stage') == 'selected':
                # exit from selection mode
                self.moves[-1].deselect_move(self.board)
                del self.moves[-1]
            else:
                self.moves[-1].undo_move(self.board)
                del self.moves[-1]
                self.switch_turn()

    # Function to check return what move stage we are at and handle move button
    def handle_move(self, x, y):
        # Check if moving from or moving to
        if not self.moves or getattr(self.moves[-1], 'move_stage') == 'moved':
            # If fresh board with no moves or move is finished move from this location
            self.move_from(x, y)
        else:
            # if the player selects a different piece to move
            if getattr(self.board[x][y], 'colour') == self.turn:
                # Removes move_id from piece and deletes move
                self.moves[-1].deselect_move(self.board)
                del self.moves[-1]
                self.move_from(x, y)
            # otherwise start a new move
            else:
                self.move_to(x, y)

    # Function to start move
    def move_from(self, x, y):
        # Get possible moves
        poss_moves = Move.get_poss_moves(self.board, self.turn, x, y, len(self.moves), scan_mode=self.scan_mode)

        # Check if it is a valid selection, if not, exit the function
        if not poss_moves:
            return -1

        # Create a new move and add to list and pass the len of move list as move id
        self.moves.append(Move(self.board, x, y, len(self.moves), poss_moves, scan_mode=self.scan_mode))

    # Function to return possible moves for the piece entered without making the move
    def get_next_poss_moves(self, x, y):
        poss_moves = Move.get_poss_moves(self.board, self.turn, x, y, len(self.moves), scan_mode=self.scan_mode,
                                         look_ahead=True)

        return poss_moves

    # Faster way to access current poss moves without recalculating all poss moves
    def get_current_poss_moves(self):
        if self.moves:
            return self.moves[-1].poss_moves

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

    # Gets the the state of the game
    # white checked
    # white checkmated
    # black checked
    # black checkmated
    # stalemate
    # MUST BE IN THE TURN OF THE SIDE YOU'RE CHECKING
    def get_game_state(self):
        # Disable print statements
        sys.stdout = open(os.devnull, 'w')

        can_move = False
        in_check = False

        # in opponent's turn currently

        # loops through all pieces on the board
        for y in range(8):
            for x in range(8):
                # If the piece iterated on is piece of the next turn
                if getattr(self.board[x][y], 'colour') == self.turn:
                    # If the piece is the king
                    if getattr(self.board[x][y], 'str_rep') == 'k' or getattr(self.board[x][y], 'str_rep') == 'K':
                        # Test if it is in check
                        in_check = self.board[x][y].isin_check(x, y, self)
                    # Try to move it and if there are no more moves
                    if self.get_next_poss_moves(x, y):
                        # set can move to true and break out
                        can_move = True

        # Restore print statements
        sys.stdout = sys.__stdout__

        if not can_move:
            if in_check:
                return '%s checkmate' % self.turn
            else:
                return 'stalemate'

        elif in_check:
            return '%s check' % self.turn

        else:
            return 'normal'

    # TODO: Convert chess coords to int coords

    # TODO: Static: Converts Object board to string board

    # TODO: Static: Converts String board to Object board

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
