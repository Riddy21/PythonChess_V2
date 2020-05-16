import tkinter as tk
from GUI_Menu import MenuGUI

def main():
    #Creating new GUI root
    window = tk.Tk()
    MenuGUI(window)

    # Loop window
    window.mainloop()

if __name__ == '__main__':
    main()