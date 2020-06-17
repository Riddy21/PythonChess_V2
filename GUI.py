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

        # Make GUI frame
        self.frame = ""

        # Make popup window
        self.popup = ""

        # GUI state
        self.state = "Menu"

        # GUI highlights
        self.highlights = [[''] * 8 for i in range(8)]

        # Board Grid
        self.boardGUI = [[0] * 8 for i in range(8)]

        # Setup menu
        self.create_menu()

        self.update()

    # Creates menu GUI
    def create_menu(self):
        # console message
        print("Starting Menu....")

        # Create a frame and pack with interface
        self.frame = tk.Frame(self.window)
        title = tk.Label(self.frame, pady=85, text="Ridvan's Chess")
        oneP = tk.Button(self.frame, text="One Player", padx=220, pady=50, command=lambda: self.main.goto_1p())
        twoP = tk.Button(self.frame, text='Two Player', padx=220, pady=50, command=lambda: self.main.goto_2p())
        close = tk.Button(self.frame, text='Close', padx=230, pady=20, command=lambda: self.main.quit_win())
        title.grid(row=0)
        oneP.grid(row=1)
        twoP.grid(row=2)
        close.grid(row=3)
        self.frame.pack()

    # Function for Quitting
    def create_board(self, mode):
        # console message
        print("Creating Board....")

        self.frame = tk.Frame(self.window)
        self.frame.pack()

        # 1P or 2P screen setup
        if mode == 1:
            player1 = tk.Label(self.frame, text='You')
            player2 = tk.Label(self.frame, text='CPU')

        else:
            player1 = tk.Label(self.frame, text='Player 1')
            player2 = tk.Label(self.frame, text='Player 2')

        # bottom buttons
        home = tk.Button(self.frame, text='Home', command=lambda: self.main.back_to_menu())
        close = tk.Button(self.frame, text='Close', command=lambda: self.main.quit_win())
        undo = tk.Button(self.frame, text='Undo', command=self.main.undo)

        player1.grid(columnspan=2, row=0, column=0)
        player2.grid(columnspan=2, row=0, column=6)
        home.grid(columnspan=2, row=9, column=0)
        close.grid(columnspan=2, row=9, column=6)
        undo.grid(columnspan=2, row=9, column=3)

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

        # Update for non-interactive mode
        self.update()

        # Listen for pawn promotion, if pawn promoted initiate popup window
        if self.main.is_pawn_promo_state() == 'ready':
            self.make_popup()

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
            for elements in self.main.get_poss_moves():
                self.highlights[elements[0]][elements[1]] = 'cyan'

    # Put gui in mainloop
    def loop(self):
        self.window.mainloop()

    # Updates gui for one cycle
    def update(self):
        self.window.update()

    # Destroys the frame to switch windows
    def destroy_frame(self):
        self.frame.destroy()

    # Popup functions

    # Makes a popup frame for paw promotion
    def make_popup(self):
        # Make popup window
        self.popup = tk.Tk()

        # configure and style
        self.popup.title("Promotion")
        self.popup.geometry("315x50")
        self.popup.resizable(0, 0)
        tk.Label(self.popup, text='Choose Piece').grid(row=1, columnspan=2, column=1)
        textlist = ['Queen', 'Rook', 'Knight', 'Bishop']
        c = 0
        for i in textlist:
            # Command is partial because needs to be current i
            button = tk.Button(self.popup, padx=17, text=i, command=partial(self.main.choose_pawn_promo, i))
            button.grid(row=2, column=c)
            c += 1

        # add closing handler
        self.popup.protocol("WM_DELETE_WINDOW", self.on_closing)

        # if in gamemode 1
        if self.main.game_mode == 1:
            # put in loop
            self.popup.mainloop()

        # if not interactive
        else:
            self.popup.update()

    # handles popup manual closing event
    def on_closing(self):
        self.main.choose_pawn_promo('Queen')
        self.destroy_popup()

    # Quits the popup
    def destroy_popup(self):
        try:
            self.popup.destroy()
        except:
            pass


    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


