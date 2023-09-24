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

        LOCK.acquire()
        #TODO Save calculated tree to speed up algorithm and don't reset 
        self.search_tree.reset()
        self.search_tree.populate(2)
        move, promo = self.search_tree.get_best_move()
        self.game.full_move(*move[0], *move[1])

        # Pawn promo
        if promo != None:
            self.game.make_pawn_promo(promo)
        LOCK.release()

