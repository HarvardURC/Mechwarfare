
from botnet.logging import *

from .video import Video
from .turret import GunController
from .move import MovementController

import server.gaits.settings as s
import server.gaits.walking as w
import math
import asyncio
loop = asyncio.get_event_loop()

DEADZONE = 0.07

buttons = ["button_X", "button_A", "button_B", "button_Y", "button_LB", "button_RB", "button_LT", "button_RT", "button_back", "button_start", "button_toggleleft", "button_toggleright"]
d = dict(zip(buttons,range(len(buttons))))

def sign(x):
    if x > 0:
        return 1.
    elif x < 0:
        return -1.
    elif x == 0:
        return 0.
    else:
        return x

class Bot:
    def __init__(self):
        self.video = Video()
        self.move = MovementController()
        self.gun = GunController()
    
    def add_client(self, c, peer):
        self.protocol = c
        w.robot.network = c
        self.video.host = peer[0]
        try:
            self.move.start()
            self.gun.start()
        except RuntimeError as e:
            debug(e)
        loop.call_soon(self.send_pos, c)

    def send_pos(self, protocol):
        protocol.send_message("TILT", 0, w.robot.tilt.present_position)
        protocol.send_message("PANP", 0, w.robot.pan.present_position)
        loop.call_later(0.5, self.send_pos, protocol)
        
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
        #print ("id: ", id, "val: ", val)
        if id == d["button_RB"]:
            self.gun.fire(val)
        elif id == d["button_LT"]:
            self.move.left(val)
        elif id == d["button_RT"]:
            self.move.right(val)
        elif id == d["button_toggleleft"]:
            self.gun.panHome(val)
        elif id == d["button_toggleright"]:
            self.gun.tiltHome(val)
        elif id == d["button_LB"]:
            self.gun.changeSprayTime(val)
        elif id == d["button_X"]:
            if s.currentLegServoSpeed >= 11:
                w.changeServoSpeeds(s.currentLegServoSpeed - 10)
                print("BUTTONX", s.currentLegServoSpeed)
        elif id == d["button_B"]:
            if s.currentLegServoSpeed <= s.MAX_SERVO_SPEED - 10:
                w.changeServoSpeeds(s.currentLegServoSpeed + 10)
                print("BUTTONB", s.currentLegServoSpeed)
        elif id == d["button_A"]:
            self.gun.manualReload(val)
        elif id == d["button_Y"]:
            self.gun.changeTurretMode(val)
            
        


    def AXIS(self, id, val, enable_deadzone=True):
        #print ("id: ", id, "val: ", val)

        # make sure val is above a certain axis threshold
        if(abs(val) < DEADZONE):
            val = 0.0
        if id == 0: self.move.strafe(val*s.MAX_STEP_SIZE)
        elif id == 1: self.move.forward(-val*s.MAX_STEP_SIZE)
        elif id == 3: self.gun.tilt(val)
        elif id == 2: self.gun.pan(val)


    def JHAT(self, id, nil, val):
        if val[0]:
            w.moveTurretServo(0, w.getTurretServoAngle(0) - val[0] * 1.5)
        if val[1]:
            w.moveTurretServo(1, w.getTurretServoAngle(1) - val[1] * 1.5)
