from tkthread import tk, TkThread
import threading, time
def main():
    root = tk.Tk()  # create the root window
    tkt = TkThread(root)  # make the thread-safe callable

    def run(func):
        threading.Thread(target=func).start()

    run(lambda: tkt(root.wm_title, 'SUCCESS'))
    run(lambda: tkt(root.wm_title, 'SUeCCESS'))
    root.update()
    time.sleep(2)  # _tkinter.c:WaitForMainloop fails
    root.mainloop()