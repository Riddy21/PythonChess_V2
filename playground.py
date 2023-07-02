from game import Game
from pieces import *
from gui import ChessboardGUI
from player import Computer, Human


#board = [[Blank()] * 8 for i in range(8)]
#board[3][0] = King('black')
#board[0][6] = Pawn('black')
#board[4][7] = King('white')

for i in range(10):
    print("------ game %s ------" % i+1)
    game = Game()
    ai1 = Computer(game=game, color='black')
    ai2 = Computer(game=game, color='white')
    thread1 = ai1.start()
    thread2 = ai2.start()

    thread1.join()
    thread2.join()
#gui = ChessboardGUI(game, ai)

#gui.run()



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
