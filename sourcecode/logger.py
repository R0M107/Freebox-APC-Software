from datetime import datetime
from colorama import Fore # type: ignore
from functions import print_color

class Logger():
    def __init__(self):
        now = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
        filename = "logs-" + now + ".txt"
        filepath = "./logs/"
        
        self.file = open(filepath + filename, 'w+')
        
    def write(self, message: str, color: Fore, title: str=None): # type: ignore
        if not message or message is None:
            raise ValueError("Invalid log message")
        
        now = datetime.today().strftime('%H:%M:%S %d-%m-%Y')

        if title is not None:
            self.file.write("[" + now + "] [" + title + "] " + message + "\n")
            print_color(message, color, title)
        else:
            self.file.write("[" + now + "] " + message + "\n")
            print_color(message, color)
