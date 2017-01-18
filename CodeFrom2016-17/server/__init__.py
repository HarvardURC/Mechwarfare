
from botnet.logging import *

from .video import Video

class Bot:
    def __init__(self):
        self.video = Video()
    
    def add_client(self, c, peer):
        self.video["peer"] = peer
        self.protocol = c

    def remove_client(self, c):
        self.video.kill()

    def VSTR(self, port, bitrate=None, **kwargs):
        self.video.kill()
        self.video["port"] = port
        if bitrate:
            self.video["bitrate"] = bitrate * 1000000 # MBs
        self.video.update(kwargs)
        self.video.run()
        
    def BUTN(self, id, val):
        pass
