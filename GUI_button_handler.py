import Game as g
# Helper functions for GUI Button interaction

# Function for Starting in 1 Player
def goto_1p(GUI):
    # Destroy previous frame
    GUI.frame.destroy()

    # Create Game object and pass in the GUI and set to self.game
    GUI.game = g.Game(GUI)

    # TODO: Initiate AI

    # Set GUI state to 1P
    GUI.state = '1P'

    # Generate 1p game board
    GUI._create_board(1)

    # Must set board before being able to play
    GUI.game.set_board("Hello")


# Function for Starting in 2 Player
def goto_2p(GUI):
    # Destroy previous frame
    GUI.frame.destroy()

    # Create a game object and pass in the GUI as set self.game
    GUI.game = g.Game(GUI)

    # Set GUI state to 2P
    GUI.state = '2P'

    # Generate 2p game board
    GUI._create_board(2)

    # Must set board before being able to play
    GUI.game.set_board("Hello")

# Returns to main menu
def back_to_menu(GUI):
    # Destroy frame game frame
    GUI.frame.destroy()

    # Reset and save the game board

    # Set GUi state
    GUI.state = 'Menu'

    # Switch to main page
    GUI.__init__(GUI.window)


def quit(GUI):
    # Save game state

    # Quit
    GUI.window.quit()


