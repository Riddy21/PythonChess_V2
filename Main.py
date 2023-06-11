from game import Game
from gui import ChessboardGUI

if __name__ == "__main__":
    game = Game()
    gui = ChessboardGUI(game)

    gui.run()
