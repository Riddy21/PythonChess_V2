import threading
import random
from time import sleep

# Ai class that can analyse a game and take control of a specific color
class Ai:
    def __init__(self, game, color):
        # Needs a game to control and a color to control
        self.game = game
        self.color = color

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
        if playable_moves:
            move = random.sample(playable_moves, 1)[0]
            self.game.full_move(*move)

