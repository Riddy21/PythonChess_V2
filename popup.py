import tkinter as tk
from tkinter import messagebox
from functools import partial

import multiprocessing

def _popup_decorator(popup, q, **kwargs):
    tk.Tk().withdraw()
    q.put(popup(**kwargs))

def draw_popup(popup, **kwargs):
    q = multiprocessing.Queue()
    popup_process = multiprocessing.Process(
            target=_popup_decorator,
            args=(popup,q),
            kwargs=kwargs
            )
    popup_process.start()
    try:
        popup_process.join()
    except KeyboardInterrupt:
        popup_process.terminate()
        raise KeyboardInterrupt

    return q.get()

def askyesno(**kwargs):
    return draw_popup(messagebox.askyesno, **kwargs)

def _make_promo_popup(options=[], default=None):
    value = [default]
    def on_click(text, value):
        popup.destroy()
        value[0] = text
        popup.quit()

    # Make popup window
    popup = tk.Tk()

    # configure and style
    popup.title("Promotion")
    width = popup.winfo_screenwidth()
    height = popup.winfo_screenheight()
    popup.geometry("315x50+%d+%d" % (width/2-315/2, height/2-50/2))
    popup.resizable(0, 0)
    tk.Label(popup, text='Choose Piece').grid(row=1, columnspan=2, column=1)
    for i, text in enumerate(options):
        # Command is partial because needs to be current i
        button = tk.Button(popup, padx=17, text=text, command=partial(on_click, text, value))
        button.grid(row=2, column=i)

    popup.mainloop()

    return value[0]

def askchoice(**kwargs):    # Makes a popup frame for paw promotion

    return draw_popup(_make_promo_popup, **kwargs)
