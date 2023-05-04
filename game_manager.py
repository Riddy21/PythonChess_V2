#!/usr/bin/env python3

from gui import GUI
from game import Game
import time

# TODO: Make self.main.game.moves easier to access from GUI
# TODO: Include mode choice in Game class

class GameManager():
    # Main function takes in parameters about GUI and kicks off GUI window setup according to with GUI or without GUI
    # Mode = 1 for interactive GUI
    # Mode = 2 for Command line control with GUI
    # Mode = 3 for Command line control with no GUI in 1 player mode
    # Mode = 4 for Command line control with no GUI in 2 player mode
    def __init__(self, mode = 1):
        self.game = ""
        self.game_mode = mode
        # GUI enabled game
        if self.game_mode == 1:
            # Create GUI object
            self.gui = GUI(self)

            # Loop gui
            self.loop()


        # GUI enabled main without loop
        elif self.game_mode == 2:
            self.gui = GUI(self)

        # Comand line control with no GUI
        elif self.game_mode == 3:
            self.game = Game()

        elif self.game_mode == 4:
            self.game = Game()

        else:
            print("Not a selection!")

    # returns True or False based on whether the game is in the pawn promo state
    def is_pawn_promo_state(self):
        if len(self.game.moves) != 0:
            # TODO: make corresponding passing function in game
            return self.game.moves[-1].pawn_promo
        return -1

    # Chooses pawn promotion piece when in pawn promo state
    def choose_pawn_promo(self, piece):
        # If the game is in pawn promo stage
        if self.is_pawn_promo_state() == 'ready':
            # Make pawn promotion
            self.game.make_pawn_promo(piece)
            self.gui.destroy_popup()
        else:
            print('Not in pawn promo state')

        # Rebuild the game board buttons if gui is used
        if self.game_mode <= 2:
            self.gui.sync_board()

    # Function to undo a move on the board
    def undo(self):
        self.game.undo_move()

        # Rebuild the game board buttons if gui is used
        if self.game_mode <= 2:
            self.gui.sync_board()

    # GUI functions ** Only to be used in GUI mode **

    # Loops GUIs to activate
    def loop(self):
        # loop gui update
        self.gui.loop()

    # Function for Starting in 1 Player
    def goto_1p(self):
        # console message
        print("switching to 1 player....")

        # Destroy previous frame
        self.gui.destroy_frame()

        # Create Game object and pass in the GUI and set to self.game
        self.game = Game()
        setattr(self.gui, 'game', self.game)

        # Set GUI state to 1P
        setattr(self.gui, 'state', '1P')

        # Generate 1p game board
        self.gui.create_board(1)

        # sync GUI
        self.gui.sync_board()

        self.gui.update()

        # TODO: Initiate AI

    # Function for Starting in 2 Player
    def goto_2p(self):
        # console message
        print("switching to 2 player....")

        # Destroy previous frame
        self.gui.destroy_frame()

        # Create Game object and pass in the GUI and set to self.game
        self.game = Game()
        setattr(self.gui, 'game', self.game)

        # Set GUI state to 1P
        setattr(self.gui, 'state', '1P')

        # Generate 1p game board
        self.gui.create_board(1)

        # sync GUI
        self.gui.sync_board()

        self.gui.update()

    # Registers a touch on the board and records it to the game
    def pressed(self, x, y):

        # make move based on move handler
        self.game.handle_move(x, y)

        # sync board
        self.gui.sync_board()

        self.gui.update()

    # Returns to main menu
    def back_to_menu(self):
        # console message
        print("Going back to menu...")

        # Destroy frame game frame
        self.gui.destroy_frame()

        # Reset and save the game board

        # Set GUi state
        setattr(self.gui, 'state', 'Menu')

        # Switch to main page
        self.gui.create_menu()

        self.gui.update()

    def quit_win(self):
        # console message
        print("Quitting game")

        # Save game state

        # Quit
        self.gui.window.quit()

        self.gui.update()


# def main():
#     # Create new Game
#     game_Window = gui.create_window()
#     gui.loop(game_Window)


if __name__ == '__main__':
    Main()
    # main()
