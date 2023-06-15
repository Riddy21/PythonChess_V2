from game import Game
from ai import Ai
from time import sleep
from pieces import *
from gui import ChessboardGUI


board = [[Blank()] * 8 for i in range(8)]
board[3][0] = King('black')
board[0][7] = Rook('white')
board[4][7] = King('white')

game = Game(board=board)
ai = Ai(game=game, color='black')
gui = ChessboardGUI(game, ai)

gui.run()



## Try pawn promo
#game.full_move(0, 2, 0, 1)
#print(game.get_game_state())
#print(game.turn)
#print(game)
#sleep(1)
#print(game.get_game_state())
#print(game.turn)
#print(game)
#game.full_move(1, 1, 1, 0)
#game.make_pawn_promo('Queen')
#print(game.get_game_state())
#print(game.turn)
#print(game)
#sleep(1)
#print(game.get_game_state())
#print(game.turn)
#print(game)
