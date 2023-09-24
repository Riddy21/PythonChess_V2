from utils import *
import threading
import random
from time import sleep
from settings import *
from search_tree import SearchTree
import logging

# FIXME: Make a variable to tell if the thread failed

class Player:
    HUMAN = 'human'
    COMPUTER = 'computer'
    def __init__(self, game, color, player_type):
        self.game = game
        if type(color) == str:
            color = COLORS.get_by_value(color)
        self.color = color
        self.type = player_type

    # FIXME: Figure out how to handle undo moves for AI without losing track
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
        self.search_tree = SearchTree(game)
        self.search_tree.populate(3)

    @run_in_thread
    def start(self):
        while self.running:
            if self.game.turn != self.color:
                self.game.switch_turn_event.wait()
            else:
                self.make_move()
        logging.info('Quitting player')
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

        # Calculate 2 layers deeper if game has already started
        if self.game.moves:
            self.search_tree.populate_continue(depth=2, moves_made=self.game.moves[-2:])

        best_move_node = self.search_tree.get_best_move()

        move = best_move_node.move
        promo = best_move_node.promo

        LOCK.acquire()
        self.game.full_move(*move[0], *move[1])

        # Pawn promo
        if promo != None:
            self.game.make_pawn_promo(promo)
        LOCK.release()

