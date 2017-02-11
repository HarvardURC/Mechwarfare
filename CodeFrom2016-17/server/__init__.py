
from botnet.logging import *

from .video import Video
from .turret import GunController, pan, tilt
from .move import MovementController

class Bot:
    def __init__(self):
        self.video = Video()
        self.move = MovementController()
        self.gun = GunController()
    
    def add_client(self, c, peer):
        self.protocol = c
        try:
            self.move.start()
            self.gun.start()
        except RuntimeError:
            pass

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
        self.move.stop.set()
        self.gun.stop.set()
        log(msg)
        log("Received QUIT from client. Quitting...")
        exit()
        
    def BUTN(self, id, val):
        if id == 1:
            self.gun.firing = val
        elif id == 6:
            self.move.right(val)
        elif id == 7:
            self.move.left(val)

    def AXIS(self, id, val):
        if id == 0: self.move.strafe(val)
        elif id == 1: self.move.forward(-val)
        elif id == 3: pan(val)
        elif id == 2: tilt(val)
            
