import tkinter as tk
from PIL.ImageTk import PhotoImage

from functools import partial

# Main Page class
from typing import Any


class GUI:
    # Constructor  with reference to root
    def __init__(self, manager):
        # Create window
        self.window = tk.Tk()

        # manager class needs to be passed in
        # to access the button functions. Not conventional but used
        # very frequently so more convenient this way
        self.manager = manager

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

        # Turn of the game
        self.turn = 'white'

        # Board Grid
        self.boardGUI = [[0] * 8 for i in range(8)]

        # Setup menu
        self.create_menu()

        self.update()

    # Creates menu GUI
    def create_menu(self):
        # console message
        print("Starting Menu....")

	# Destroy all popups
        self.destroy_popup()

        # Create a frame and pack with interface
        self.frame = tk.Frame(self.window)
        title = tk.Label(self.frame, pady=85, text="Ridvan's Chess")
        oneP = tk.Button(self.frame, text="One Player", padx=220, pady=50, command=lambda: self.manager.goto_1p())
        twoP = tk.Button(self.frame, text='Two Player', padx=220, pady=50, command=lambda: self.manager.goto_2p())
        close = tk.Button(self.frame, text='Close', padx=230, pady=20, command=lambda: self.manager.quit_win())
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
        home = tk.Button(self.frame, text='Home', command=lambda: self.manager.back_to_menu())
        close = tk.Button(self.frame, text='Close', command=lambda: self.manager.quit_win())
        undo = tk.Button(self.frame, text='Undo', command=self.manager.undo)

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
                                                    command = partial(self.manager.pressed, x, y))
                elif not i % 2 == 0 and not y % 2 == 0:
                    self.boardGUI[x][y] = tk.Button(self.frame, highlightbackground='white', highlightthickness=4,
                                                    command = partial(self.manager.pressed, x, y))
                else:
                    self.boardGUI[x][y] = tk.Button(self.frame, highlightbackground='black', highlightthickness=4,
                                                    command = partial(self.manager.pressed, x, y))
                i = i + 1
                self.boardGUI[x][y].grid(row=y + 1, column=x)

        self.sync_board()

    # Resync the board with the GUIs
    def sync_board(self):
        board = self.manager.game.board

        highlights = self.set_highlights()

        # Restore board colour
        self._restore_board_colour()

        # Sync board with the board array on game
        for y in range(8):
            for x in range(8):
                image = PhotoImage(file=getattr(board[x][y], 'image'))
                if self.manager.game.turn == 'black':
                    gui_x = 7 - x
                    gui_y = 7 - y
                else:
                    gui_x = x
                    gui_y = y
                self.boardGUI[gui_x][gui_y].configure(image=image,
                                                      command=partial(self.manager.pressed, x, y))
                self.boardGUI[gui_x][gui_y].photo = image
                if highlights[x][y] == 'cyan':
                    self.boardGUI[gui_x][gui_y].configure(highlightbackground='cyan')

        # Update for non-interactive mode
        self.update()

        # Listen for pawn promotion, if pawn promoted initiate popup window
        if self.manager.is_pawn_promo_state() == 'ready':
            self.make_promo_popup()

        # Check gamestate for check and checkmates
        gamestate = self.manager.game.get_game_state()

        if self._is_new_turn() and gamestate.endswith('checkmate'):
            self.make_checkmated_popup()

        if self._is_new_turn() and gamestate.endswith('check'):
            self.make_checked_popup()

        self.turn = self.manager.game.turn 

        print(self.manager.game.get_game_state())

    # Checks if this is a fresh new turn
    def _is_new_turn(self):
        if self.turn != self.manager.game.turn:
            return True
        return False


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
        # Initiate highlights
        highlights = [[''] * 8 for i in range(8)]

        # Only in select mode
        if self.manager.game.moves != [] and self.manager.game.moves[-1].move_stage == 'selected':
            # highlight the board squares that are indicated by the game in cyan
            for elements in self.manager.game.get_current_poss_moves():
                highlights[elements[0]][elements[1]] = 'cyan'

        return highlights

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
    def make_promo_popup(self):
        # Disable the board
        self.window.disable()
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
            button = tk.Button(self.popup, padx=17, text=i, command=partial(self.manager.choose_pawn_promo, i))
            button.grid(row=2, column=c)
            c += 1

        # add closing handler
        self.popup.protocol("WM_DELETE_WINDOW", self.on_closing)

        # if in gamemode 1
        if self.manager.game_mode == 1:
            # put in loop
            self.popup.mainloop()

        # if not interactive
        else:
            self.popup.update()

    # Makes a popup frame for check
    def make_checked_popup(self):
        # Make popup window
        self.popup = tk.Tk()

        # configure and style
        tk.Label(self.popup, text='%s checked!' % self.manager.game.turn).pack()
        self.popup.geometry("315x50")
        self.popup.resizable(0, 0)
        button = tk.Button(self.popup, padx=17, text='Ok',
                           command=self.destroy_popup).pack()

    # Makes a popup frame for checkmate
    def make_checkmated_popup(self):
        # Make popup window
        self.popup = tk.Tk()

        # configure and style
        tk.Label(self.popup, text='%s checkmated!' % self.manager.game.turn).pack()
        self.popup.geometry("315x50")
        self.popup.resizable(0, 0)
        button = tk.Button(self.popup, padx=17, text='Main Menu',
                           command=self.manager.back_to_menu).pack()

    # handles popup manual closing event
    def on_closing(self):
        self.manager.choose_pawn_promo('Queen')
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


