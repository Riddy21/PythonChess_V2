import tkinter as tk

#Main Page class
class MenuGUI():
    #Constructor  with reference to root
    def __init__(self, window):
        #Init variables
        self.window = window

        #Setup window
        self.window.title("Chess")
        self.window.geometry("500x500")
        self.window.resizable(0,0)

        #Create a frame and pack with interface
        self.titleFrame = tk.Frame(self.window)
        self.title = tk.Label(self.titleFrame, pady=85, text="Ridvan's Chess")
        self.oneP = tk.Button(self.titleFrame, text="One Player", padx=220, pady=50, command=self._create_1p)
        self.twoP = tk.Button(self.titleFrame, text='Two Player', padx=220, pady=50, command=self._create_2p)
        self.close = tk.Button(self.titleFrame, text='Close', padx=230, pady=20, command=self._quit)
        self.title.grid(row=0)
        self.oneP.grid(row=1)
        self.twoP.grid(row=2)
        self.close.grid(row=3)
        self.titleFrame.pack()


    #Function for Quitting
    def _quit(self):
        self.window.quit()

    #Function for Starting in 1 Player
    def _create_1p(self):
        pass

    #Function for Starting in 2 Player
    def _create_2p(self):
        pass