
from botnet.logging import *

from .video import Video

class Bot:
    def __init__(self):
        self.video = Video()
    
    def add_client(self, c, peer):
        self.protocol = c

    def remove_client(self, c):
        self.video.kill()

    def VSTR(self, port, bitrate=None, options={}):
        self.video["port"] = port
        if bitrate:
            self.video["bitrate"] = bitrate * 1000000 # MBs
        self.video.update(options)
        self.video.run()
        self.protocol.send_message("VSTR", port)

    def QUIT(self, btn, val, msg):
        log(msg)
        log("Received QUIT from client. Quitting...")
        exit()
        
    def BUTN(self, id, val):
        pass
