from parallel_util import *
import random
from time import sleep

LOCK = threading.Lock()

class Player:
    HUMAN = 'human'
    COMPUTER = 'computer'
    def __init__(self, game, color, type):
        super().__init__()
        self.game = game
        self.color = color
        self.type = type

    def undo_move(self, num=1):
        for i in range(num):
            LOCK.acquire()
            self.game.undo_move()
            LOCK.release()


class Human(Player):
    def __init__(self, game, color):
        super().__init__(game, color, Player.HUMAN)

    def handle_move(self, col, row):
        LOCK.acquire()
        self.game.handle_move(col, row)
        LOCK.release()


# Ai class that can analyse a game and take control of a specific color
class Computer(Player):
    def __init__(self, game, color):
        super().__init__(game, color, Player.COMPUTER)
        self.running = True

    @run_in_thread
    def start(self):
        while self.running:
            if self.game.turn != self.color:
                self.game.switch_turn_event.wait()
            else:
                self.make_move()
        print('Quitting player')
        exit()

    def quit(self):
        self.running = False
        # Make sure to alert all players
        self.game.alert_players()


    def make_move(self):
        # get all playable pieces
        playable_pieces = self.game.get_playable_piece_coords()

        # Get all possible moves
        playable_moves = set()
        # FIXME: Check will cause "no more moves"
        for piece in playable_pieces:
            LOCK.acquire()
            moves = self.game.get_next_poss_moves(*piece)
            LOCK.release()
            for move in moves:
                playable_moves.add((*piece, *move))

        # Don't do anything on checkmate or stalemate
        if 'mate' in self.game.game_state:
            # Pause
            self.game.switch_turn_event.wait()
            return

        # TODO: This is a placeholder
        # chose the move to make
        # NOTE: Lock to make sure game only accessed by one at a time
        LOCK.acquire()
        if playable_moves:
            move = random.sample(playable_moves, 1)[0]
            self.game.full_move(*move)
        if self.game.game_state == '%s pawn promo' % self.color:
            self.game.make_pawn_promo('Queen')

        LOCK.release()

