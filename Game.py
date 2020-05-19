# Game class initiated when the game board is displayed
class Game:
    def __init__(self,GUI):
        # GUI pointer for changing GUI from game class
        self.GUI = GUI

        # 2D array of pieces to represent board
        self.board = [[''] * 8] * 8

        # stack of all old moves and current move
        self.moves = []

        # string representing the turn colour of the game
        self.turn = 'white'

        # State defining whether you are selecting a piece or where to move it
        self.move_state = 'select'

    # TODO: set board as a specific config
    def set_board(self,config):
        # TODO: set board by updating self.board

        #TODO: sync board
        pass

    # TODO: print board in string format using string representation
    def __str__(self):
        print("Not done yet")



