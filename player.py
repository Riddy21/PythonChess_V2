from utils import *
import threading
import random
from time import sleep

# FIXME: Make a variable to tell if the thread failed

class Player:
    HUMAN = 'human'
    COMPUTER = 'computer'
    def __init__(self, game, color, type):
        super().__init__()
        self.game = game
        self.color = color
        self.type = type

    @run_synchronously
    def undo_move(self, num=1):
        self.game.undo_move(num)


class Human(Player):
    def __init__(self, game, color):
        super().__init__(game, color, Player.HUMAN)

    @run_synchronously
    def handle_move(self, col, row):
        self.game.handle_move(col, row)


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
        # Don't do anything on checkmate or stalemate
        if 'mate' in self.game.game_state:
            # Pause
            self.game.switch_turn_event.wait()
            return

        LOCK.acquire()
        # get all playable pieces
        playable_pieces = self.game.get_playable_piece_coords()

        # Get all possible moves
        playable_moves = set()
        # FIXME: Check will cause "no more moves"
        for piece in playable_pieces:
            moves = self.game.get_next_poss_moves(*piece)
            for move in moves:
                playable_moves.add((*piece, *move))


        # TODO: This is a placeholder
        # chose the move to make
        # NOTE: Lock to make sure game only accessed by one at a time
        if playable_moves:
            move = random.sample(playable_moves, 1)[0]
            self.game.full_move(*move)
        if self.game.game_state == '%s pawn promo' % self.color:
            self.game.make_pawn_promo('Queen')
        LOCK.release()

