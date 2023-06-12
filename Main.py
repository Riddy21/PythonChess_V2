from game import Game
from gui import ChessboardGUI
from ai import Ai

if __name__ == "__main__":
    #GameManager()
    game = Game()
    ai = Ai(game, 'black')
    gui = ChessboardGUI(game, ai)
    #ai.start()

    gui.run()
