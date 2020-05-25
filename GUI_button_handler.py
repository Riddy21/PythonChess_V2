from Game import Game


# Helper functions for GUI Button interaction

# Function for Starting in 1 Player
def goto_1p(GUI):
    # console message
    print("switching to 1 player....")

    # Destroy previous frame
    GUI.frame.destroy()

    # Create Game object and pass in the GUI and set to self.game
    game = Game(GUI)
    GUI.game = game

    # Set GUI state to 1P
    GUI.state = '1P'

    # Generate 1p game board
    GUI.create_board(1)

    # Must set board before being able to play
    game.set_board()

    # TODO: Initiate AI


# Function for Starting in 2 Player
def goto_2p(GUI):
    # console message
    print("switching to 2 player....")

    # Destroy previous frame
    GUI.frame.destroy()

    # Create a game object and pass in the GUI as set self.game
    game = Game(GUI)
    GUI.game = game

    # Set GUI state to 2P
    GUI.state = '2P'

    # Generate 2p game board
    GUI.create_board(2)

    # Must set board before being able to play
    game.set_board()


# Registers a touch on the board and records it to the game
def pressed(GUI, x, y):

    # console message
    print(x, y)

    # Gets move status of last element of move queue

    # If move is in progress, register the end location and make move

    # If move finished, start new move and enter coordinates


# Returns to main menu
def back_to_menu(GUI):
    # console message
    print("Going back to menu...")

    # Destroy frame game frame
    GUI.frame.destroy()

    # Reset and save the game board

    # Set GUi state
    GUI.state = 'Menu'

    # Switch to main page
    GUI.__init__(GUI.window)


def quit_win(GUI):
    # console message
    print("Quitting game")

    # Save game state

    # Quit
    GUI.window.quit()
