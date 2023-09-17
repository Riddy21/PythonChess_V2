import logging
from game import Game
from player import *
from gui import ChessboardGUI

if __name__ == "__main__":
    game = Game()
    ai = Computer(game, 'black')
    player = Human(game, 'white')
    #player = Computer(game, 'white')
    gui = ChessboardGUI(game, p1=ai, p2=player)
    ai.start()
    #player.start()

    #game.switch_turn_event.release()

    gui.run()
