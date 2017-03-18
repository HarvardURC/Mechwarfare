
from botnet.logging import *

from .video import Video
from .turret import GunController
from .move import MovementController

DEADZONE = 0.1

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
        except RuntimeError as e:
            debug(e)

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
        print ("id: ", id, "val: ", val)
        if id == 5:
            self.gun.fire(val)
        elif id == 6:
            self.move.left(val)
        elif id == 7:
            self.move.right(val)
        elif id == 10:
            self.gun.panHome(val)
        elif id == 11:
            self.gun.tiltHome(val)
        


    def AXIS(self, id, val, enable_deadzone=True):
        #print ("id: ", id, "val: ", val)

        # make sure val is above a certain axis threshold
        if(abs(val) < DEADZONE):
            val = 0.0
        if id == 0: self.move.strafe(val*200)
        elif id == 1: self.move.forward(-val*200)
        elif id == 3: self.gun.tilt(val*200)
        elif id == 2: self.gun.pan(val*200)

            
