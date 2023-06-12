from game import Game
from ai import Ai
from time import sleep
from pieces import *


board = [[Blank()] * 8 for i in range(8)]
board[0][2] = Pawn('white')
board[1][1] = Pawn('white')
board[2][2] = Pawn('black')

game = Game(board=board)
ai = Ai(game=game, color='black')
ai_thread = ai.start()

print(game)

# Try pawn promo
game.full_move(0, 2, 0, 1)
print(game.get_game_state())
print(game.turn)
print(game)
sleep(1)
print(game.get_game_state())
print(game.turn)
print(game)
game.full_move(1, 1, 1, 0)
game.make_pawn_promo('Queen')
print(game.get_game_state())
print(game.turn)
print(game)
sleep(1)
print(game.get_game_state())
print(game.turn)
print(game)
