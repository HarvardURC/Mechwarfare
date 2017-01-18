
from botnet.logging import *

class Client:
    def fatal(self, message):
        log(message)
        log("Quitting...")
        exit()
