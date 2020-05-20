from Pieces import Blank, Bishop, King, Knight, Rook, Pawn, Queen


# Game class initiated when the game board is displayed
class Game:
    def __init__(self,GUI):
        # GUI pointer for changing GUI from game class
        self.GUI = GUI

        # 2D array of pieces to represent board
        self.board = [[Blank()] * 8 for i in range(8)]

        # stack of all old moves and current move
        self.moves = []

        # string representing the turn colour of the game
        self.turn = 'white'

        # State defining whether you are selecting a piece or where to move it
        self.move_state = 'select'

    # TODO: set board as a specific config
    def set_board(self,config):
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

        #TODO: sync board
        self.GUI.sync_board()


    # TODO: print board in string format using string representation
    def __str__(self):
        print("Not done yet")



