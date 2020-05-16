
import tkinter as tk

# Create another window with menu
# Passes back game window
def create_game():
    # Creates window and passes back to user
    window = tk.Tk()
    game_GUI = GUI(window)
    return game_GUI

def loop(*GUIs):
    # loop through all windows and loop them
    for gui in GUIs:
        gui.window.mainloop()

# Main Page class
class GUI():
    # Constructor  with reference to root
    def __init__(self,window):
        # Create window
        self.window = window

        # Setup window
        self.window.title("Chess")
        self.window.geometry("500x500")
        self.window.resizable(0, 0)

        # Create a frame and pack with interface
        self.frame = tk.Frame(self.window)
        self.title = tk.Label(self.frame, pady=85, text="Ridvan's Chess")
        self.oneP = tk.Button(self.frame, text="One Player", padx=220, pady=50, command=self._goto_1p)
        self.twoP = tk.Button(self.frame, text='Two Player', padx=220, pady=50, command=self._goto_2p)
        self.close = tk.Button(self.frame, text='Close', padx=230, pady=20, command=self._quit)
        self.title.grid(row=0)
        self.oneP.grid(row=1)
        self.twoP.grid(row=2)
        self.close.grid(row=3)
        self.frame.pack()

    # Function for Quitting
    def _quit(self):
        self.window.quit()

    # Function for Starting in 1 Player
    def _goto_1p(self):
        self.frame.destroy()
        self._create_board(1)

    # Function for Starting in 2 Player
    def _goto_2p(self):
        self.frame.destroy()
        self._create_board(2)

    def sync_board(self):
        for x in range(8):
            for y in range(8):
                #elf.board[x][y].config(image=Main.piece[x][y].getImage())
                self.board[x][y].grid(row=y + 1, column=x)

    def _create_board(self,mode):
        self.frame = tk.Frame(self.window)
        self.frame.pack()

        # 1P or 2P screen setup
        if (mode == 1):
            self.player1 = tk.Label(self.frame, text='You')
            self.player2 = tk.Label(self.frame, text='CPU')

        else:
            self.player1 = tk.Label(self.frame, text='Player 1')
            self.player2 = tk.Label(self.frame, text='Player 2')

        # bottom buttons
        self.home = tk.Button(self.frame, text='Home', command=self._back_to_menu)
        self.close = tk.Button(self.frame, text='Close', command=self._quit)
        self.undo = tk.Button(self.frame, text='Undo')

        self.player1.grid(columnspan=2, row=0, column=0)
        self.player2.grid(columnspan=2, row=0, column=6)
        self.home.grid(columnspan=2, row=9, column=0)
        self.close.grid(columnspan=2, row=9, column=6)
        self.undo.grid(columnspan=2, row=9, column=3)
        self.board = [[0 for col in range(8)] for row in range(8)]
        i = 0

        # Create Board as series of buttons and save to 2D array
        for y in range(8):
            for x in range(8):
                if (i % 2 == 0 and y % 2 == 0):
                    self.board[x][y] = tk.Button(self.frame, bg='white', padx=7)
                elif (not i % 2 == 0 and not y % 2 == 0):
                    self.board[x][y] = tk.Button(self.frame, bg='white', padx=7)
                else:
                    self.board[x][y] = tk.Button(self.frame, bg='grey', padx=7)
                i = i + 1

        self.sync_board()

    def _back_to_menu(self):
        self.frame.destroy()
        self.__init__(self.window)