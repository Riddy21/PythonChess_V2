import GUI as gui
import time


# Make functions to control interface

#TODO: Make GUI button handler into main function! and have option to initiate GUI

# class Main():
#     # Main function takes in parameters about GUI and kicks off GUI window setup according to with GUI or without GUI
#     def __init__(self, GUI=True):
#         # enable or disable GUI
#         if GUI:
#             self.gui = GUI.create_window()
#         else:
#             self.gui = 'null'



def main():
    # Create new Game
    game_Window = gui.create_window()
    gui.loop(game_Window)




if __name__ == '__main__':
    main()
