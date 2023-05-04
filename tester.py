from game import Game
from pieces import *


board = [[Blank()] * 8 for i in range(8)]
board[0][2] = Pawn('white')
board[1][1] = Pawn('white')
board[2][2] = Pawn('black')

game = Game(board=board)

print(game)

# Try pawn promo
game.full_move(0, 2, 0, 1)
print(game.get_game_state())
print(game.turn)
print(game)
game.full_move(2, 2, 2, 4)
print(game.get_game_state())
print(game.turn)
print(game)
game.full_move(0, 1, 0, 0)
print(game.get_game_state())
print(game.turn)
print(game)
game.make_pawn_promo('Queen')
print(game.get_game_state())
print(game.turn)
print(game)
game.make_pawn_promo('Rook')
print(game.get_game_state())
print(game.turn)
print(game)
