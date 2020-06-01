import tkinter as tk
from functools import partial

# Main Page class
from typing import Any


class GUI:
    # Constructor  with reference to root
    def __init__(self, main):
        # Create window
        self.window = tk.Tk()

        # main class needs to be passed in
        # to access the button functions. Not conventional but used
        # very frequently so more convenient this way
        self.main = main

        # Setup window
        self.window.title("Chess")
        self.window.geometry("500x500")
        self.window.resizable(0, 0)

        # GUI state
        self.state = "Menu"

        # GUI highlights
        self.highlights = [[''] * 8 for i in range(8)]

        # Board Grid
        self.boardGUI = [[0] * 8 for i in range(8)]

        # Setup menu
        self.create_menu()

    # Creates menu GUI
    def create_menu(self):
        # console message
        print("Starting Menu....")

        # Create a frame and pack with interface
        self.frame = tk.Frame(self.window)
        self.title = tk.Label(self.frame, pady=85, text="Ridvan's Chess")
        self.oneP = tk.Button(self.frame, text="One Player", padx=220, pady=50, command=lambda: self.main.goto_1p())
        self.twoP = tk.Button(self.frame, text='Two Player', padx=220, pady=50, command=lambda: self.main.goto_2p())
        self.close = tk.Button(self.frame, text='Close', padx=230, pady=20, command=lambda: self.main.quit_win())
        self.title.grid(row=0)
        self.oneP.grid(row=1)
        self.twoP.grid(row=2)
        self.close.grid(row=3)
        self.frame.pack()

    # Function for Quitting
    def create_board(self, mode):
        # console message
        print("Creating Board....")

        self.frame = tk.Frame(self.window)
        self.frame.pack()

        # 1P or 2P screen setup
        if mode == 1:
            self.player1 = tk.Label(self.frame, text='You')
            self.player2 = tk.Label(self.frame, text='CPU')

        else:
            self.player1 = tk.Label(self.frame, text='Player 1')
            self.player2 = tk.Label(self.frame, text='Player 2')

        # bottom buttons
        self.home = tk.Button(self.frame, text='Home', command=lambda: self.main.back_to_menu())
        self.close = tk.Button(self.frame, text='Close', command=lambda: self.main.quit_win())
        self.undo = tk.Button(self.frame, text='Undo')

        self.player1.grid(columnspan=2, row=0, column=0)
        self.player2.grid(columnspan=2, row=0, column=6)
        self.home.grid(columnspan=2, row=9, column=0)
        self.close.grid(columnspan=2, row=9, column=6)
        self.undo.grid(columnspan=2, row=9, column=3)

        i = 0

        # Create Board as series of buttons and save to 2D array
        for y in range(8):
            for x in range(8):
                if i % 2 == 0 and y % 2 == 0:
                    self.boardGUI[x][y] = tk.Button(self.frame, highlightbackground='white', highlightthickness=4,
                                                    command = partial(self.main.pressed, x, y))
                elif not i % 2 == 0 and not y % 2 == 0:
                    self.boardGUI[x][y] = tk.Button(self.frame, highlightbackground='white', highlightthickness=4,
                                                    command = partial(self.main.pressed, x, y))
                else:
                    self.boardGUI[x][y] = tk.Button(self.frame, highlightbackground='black', highlightthickness=4,
                                                    command = partial(self.main.pressed, x, y))
                i = i + 1
                self.boardGUI[x][y].grid(row=y + 1, column=x)

        self.sync_board()

    # Resync the board with the GUIs
    def sync_board(self):
        board = self.main.game.board

        self.set_highlights()

        # Restore board colour
        self._restore_board_colour()

        # Sync board with the board array on game
        for y in range(8):
            for x in range(8):
                image = tk.PhotoImage(file=getattr(board[x][y], 'image'))
                self.boardGUI[x][y].configure(image=image)
                self.boardGUI[x][y].photo = image
                if self.highlights[x][y] == 'cyan':
                    self.boardGUI[x][y].configure(highlightbackground='cyan')

        # Revert highlights back to default
        self.highlights = [[''] * 8 for i in range(8)]

    # Restore board colour back to checker board
    def _restore_board_colour(self):
        i = 0
        for y in range(8):
            for x in range(8):
                if i % 2 == 0 and y % 2 == 0:
                    self.boardGUI[x][y].configure(highlightbackground='white')
                elif not i % 2 == 0 and not y % 2 == 0:
                    self.boardGUI[x][y].configure(highlightbackground='white')
                else:
                    self.boardGUI[x][y].configure(highlightbackground='black')
                i = i + 1

    # Set highlighted squares that can be moved to
    def set_highlights(self):
        if len(self.main.game.moves) != 0:
            # highlight the board squares that are indicated by the game in cyan
            for elements in self.main.game.moves[-1].poss_moves:
                self.highlights[elements[0]][elements[1]] = 'cyan'

    # Put gui in mainloop
    def loop(self):
        self.window.mainloop()

    def destroy_frame(self):
        self.frame.destroy()

    # Setters and getters
    # # Get game object from GUi
    # def get_game(self):
    #     return self.game
    #
    # def set_game(self, game):
    #     self.game = game
    #
    # def set_state(self):

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


