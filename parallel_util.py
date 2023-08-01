import threading
import multiprocessing

def run_in_thread(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

def run_in_process(func):
    def wrapper(*args, **kwargs):
        process = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        process.start()
        return process
    return wrapper