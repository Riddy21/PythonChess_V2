from Pieces import Blank, Bishop, King, Knight, Rook, Pawn, Queen
from Move import Move, is_valid_selection


# Game class initiated when the game board is displayed
class Game:
    def __init__(self):
        # 2D array of pieces to represent board
        self.board = [[Blank()] * 8 for i in range(8)]

        # captured Pieces
        self.captured_white = []
        self.captured_black = []

        # stack of all old moves and current move
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

        # TODO: set according to config

    # TODO: Move interfacing functions

    # TODO: Function to make complete move from to-coordinates and from-coordinates

    # Function to switch turns
    def switch_turn(self):
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

    # Function to check return what move stage we are at and handle move button
    def handle_move(self, x, y):
        # Check if moving from or moving to
        if len(self.moves) == 0 or getattr(self.moves[-1], 'move_stage') == 'moved':
            # If fresh board with no moves or move is finished move from this location
            print('from')
            self.move_from(x, y)
        else:
            #  If move is started finish and change side
            print('to')
            self.move_to(x, y)
            self.switch_turn()


    # Function to start move
    def move_from(self, x, y):
        # Check if it is a valid selection, if not, exit the function
        if not is_valid_selection(self.board, self.turn, x, y):
            print("Not a valid selection!")
            return

        # Create a new move and add to list
        self.moves.append(Move(self.board, self.turn, x, y))

    # Function to end move,
    def move_to(self, x, y):
        # Makes move on the most recent move
        self.moves[-1].make_move(self.board, x, y)

    # TODO: Function to undo move

    # TODO: Convert chess coords to int coords

    # TODO: Static: Converts Object board to string board

    # TODO: Static: Converts String board to Object board

    # TODO: print board in string format using string representation
    def __str__(self):
        str = ''

        # Add board string reps
        for y in range(8):
            for x in range(8):
                str += self.board[x][y].str_rep + ' '
            str += '\n'

        return str
