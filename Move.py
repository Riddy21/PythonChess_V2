from Pieces import Blank, Bishop, King, Knight, Rook, Pawn, Queen

# TODO:
# check if str_rep check works
# chack if passing board updates correctly


# Function for checking if player picked a piece of the right colour and type
def is_valid_selection(board, turn, x, y):
    if board[x][y].str_rep != "_" and board[x][y].colour == turn:
        return True
    print("Invalid selection")
    return False


# TODO: Class to record moves and change game board
class Move():
    # init
    def __init__(self, board, turn, x, y):
        # Parameter for move stage
        self.move_stage = "select"

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

        # Parameter for captured Piece
        self.captured = 'None'

        self.board_before = [[""] * 8 for i in range(8)]
        # Parameter for board in string rep before move
        for x in range(8):
            for y in range(8):
                self.board_before[x][y] = board[x][y].str_rep

    # validate move and make the move based on the end coordinates
    def make_move(self, x, y, board):
        # Check if it is a valid move
        # ** Don't set move to until validated
        if not self.is_valid_move(x, y):
            print("invalid move")
            return -1

        # set move_to to x y now that it is verified as a valid move
        self.move_to = x, y

        # change game board based on move locations and move type and save to after move
        self.move_type = self._get_move_type(board)

        # Make move
        frox = self.move_from[0]
        froy = self.move_from[1]
        tox = self.move_to[0]
        toy = self.move_to[1]

        if self.move_type == 'capture':
            self.captured = board[tox][toy].str_rep
            board[tox][toy] = board[frox][froy]
            board[frox][froy] = Blank()

        elif self.move_type == 'move':
            board[tox][toy], board[frox][froy] = board[frox][froy], board[tox][toy]

        # TODO: finish other ones

    # TODO: Undo a move
    def undo_move(self):
        # undo move using the board_before and capture pieces
        pass

    # Private: Validate move
    def is_valid_move(self, x, y):
        return True
        # TODO: Do checks as such:
        # if not self._turn_check():
        #     return False
        # else:
        #     return True

    # TODO: Private: Checks if the move is a valid castle ** make sure to update move type here!

    # TODO: Private: Checks if the move is a valid enpassante ** make sure to update move type here!

    # TODO: Private: Checks if the move is a valid pawn promotion ** make sure to update move type here!

    # TODO: Find move type
    def _get_move_type(self, board):
        # Check if the move type has already been set as a castle, pawn_promo, or enpassante
        if self.move_type == 'castle' or self.move_type == 'pawn_promo' or self.move_type == 'enpassante':
            return self.move_type

        # convert move_to to x,y
        x = self.move_to[0]
        y = self.move_to[1]

        # If is capture
        if board[x][y].str_rep != "_":
            return 'capture'

        # If is normal move
        else:
            return 'move'

    # TODO: make converter from str_rep to object
