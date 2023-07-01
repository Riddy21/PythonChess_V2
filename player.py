import threading
import random
from time import sleep

class Player:
    HUMAN = 'human'
    COMPUTER = 'computer'
    def __init__(self, game, color, type):
        super().__init__()
        self.game = game
        self.color = color
        self.type = type

    def start(self):
        def threaded_start():
            while 'mate' not in self.game.get_game_state():
                # TODO: Change this to event based later
                sleep(1)
                if self.game.turn == self.color:
                    self.make_move()
        start_thread = threading.Thread(target=threaded_start)
        start_thread.start()

        return start_thread


    def make_move(self):
        raise TypeError("Cannot make move on Player class")
        


class Human(Player):
    def __init__(self, game, color):
        super().__init__(game, color, Player.HUMAN)


# Ai class that can analyse a game and take control of a specific color
class Computer(Player):
    def __init__(self, game, color):
        super().__init__(game, color, Player.COMPUTER)

    def make_move(self):
        # get all playable pieces
        playable_pieces = self.game.get_playable_piece_coords()

        # Get all possible moves
        playable_moves = set()
        # FIXME: Check will cause "no more moves"
        for piece in playable_pieces:
            moves = self.game.get_next_poss_moves(*piece)
            #print(self.game.board[piece[0]][piece[1]])
            #print(moves)
            for move in moves:
                playable_moves.add((*piece, *move))

        # chose the move to make
        # FIXME: This is a placeholder
        print(self.game.game_state)
        if self.game.game_state == '%s pawn promo' % self.color:
            self.game.make_pawn_promo('Queen')
        if playable_moves:
            move = random.sample(playable_moves, 1)[0]
            self.game.full_move(*move)

