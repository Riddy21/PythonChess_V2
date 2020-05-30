from GUI import GUI
from Game import Game
import time


# Make functions to control interface

# TODO: Make GUI button handler into main function! and have option to initiate GUI

class Main():
    # Main function takes in parameters about GUI and kicks off GUI window setup according to with GUI or without GUI
    def __init__(self, gui_en=True):
        self.game = ""
        # GUI enabled game
        if gui_en:
            self.gui = GUI(self)
            self.loop()


        # GUI non enabled main
        else:
            pass

    # GUI functions

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

        # Must set board before being able to play
        self.game.set_board()

        # sync GUI
        self.gui.sync_board()

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

        # Must set board before being able to play
        self.game.set_board()

        # sync GUI
        self.gui.sync_board()

    # Registers a touch on the board and records it to the game
    def pressed(self, x, y):

        # make move based on move handler
        self.game.handle_move(x,y)

        # sync board
        self.gui.sync_board()

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

    def quit_win(self):
        # console message
        print("Quitting game")

        # Save game state

        # Quit
        self.gui.window.quit()


# def main():
#     # Create new Game
#     game_Window = gui.create_window()
#     gui.loop(game_Window)


if __name__ == '__main__':
    Main()
    # main()
