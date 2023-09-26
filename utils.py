from enum import Enum
import threading
import multiprocessing

class ChessEnum(Enum):
    @classmethod
    def get_by_key(cls, key, value):
        # NOTE: For loop not ideal but fast enough for small enums
        for member in cls:
            if member.value[key] == value:
                return member
        raise KeyError(f"No member with value {value}")

    @classmethod
    def get_by_value(cls, value):
        # NOTE: For loop not ideal but fast enough for small enums
        for member in cls:
            if member.value == value:
                return member
        raise KeyError(f"No member with value {value}")

LOCK = threading.Lock()

def run_in_thread(func): # pragma: no cover
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

def run_in_process(func): # pragma: no cover
    def wrapper(*args, **kwargs):
        process = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        process.start()
        return process
    return wrapper

def run_synchronously(func): # pragma: no cover
    def wrapper(*args, **kwargs):
        LOCK.acquire()
        func(*args, **kwargs)
        LOCK.release()
    return wrapper
