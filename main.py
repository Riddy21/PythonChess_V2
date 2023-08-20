from game import Game
from gui import ChessboardGUI
from player import Computer, Human
import logging

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
