import tkinter as tk
from GUI_Menu import MenuGUI


# Create another window with menu
# Passes back game window
def createGame():
    # Creates window and passes back to user
    game_window = tk.Tk()
    MenuGUI(game_window)
    return game_window


# Go to 1P Board
# Must pass in the window
def go_to_1P(window):
    # Initiate game interface on window with 1P parameter
    print("1")


# Go to 2P Board
# Must pass in the window
def go_to_2P(window):
    # Initiate game interface on window with 1P parameter
    print("2")


# loop windows
# Can pass in as many variables as needed
def loop(*windows):
    # loop through all windows and loop them
    for i in windows:
        i.mainloop()
