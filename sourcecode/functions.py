import ctypes
from colorama import Fore, Style, init # type: ignore

def is_admin(): # Does the program have admin rights ?
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def print_color(message: str, color: Fore, title: str=None): # type: ignore
    init(convert=True)
    if title is None:
        print(color + message + Style.RESET_ALL)
    else:
        print(color + "[" + title + "] " + message + Style.RESET_ALL)