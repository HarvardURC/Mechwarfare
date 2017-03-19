
from threading import Thread, Lock, Event

from botnet.logging import *

import time, sys
import traceback as tb

from server.gaits.walking import *
import server.gaits.settings as s

if not s.isAnimation:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)  
    GPIO.setup(s.GUN_PIN, GPIO.OUT)


class GunController(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.firing = False

    ### THIS IS THE FUNCTION
    def fire(self, isOn):
        if isOn:
            debug("FIRING GUN POW POW")
            if not s.isAnimation:
                self.firing = True
                GPIO.output(s.GUN_PIN,True)
            else:
                self.firing = True
        else:
            debug("Stopped firing")
            if not s.isAnimation:
                GPIO.output(s.GUN_PIN,False)
                self.firing = False
            else:
                self.firing = False
                

    def run(self):
        self.stop = Event()
        while not self.stop.is_set():
            if not s.isAnimation:
                if self.firing:
                    moveAgitatorServo(10)
                    time.sleep(.5) 
                    moveAgitatorServo(0)
                    time.sleep(.5) 
                else:
                    time.sleep(.05)
            else:
                time.sleep(.05)

                   

    ### Ignore below for now
    # I stopped ignoring these Aaron :)

    def pan(self, speed):
        """This function should turn on the pan motor at the specified speed,
           positive values are to the right, negative to the left. Zero is off.
           The input will range from -1 to +1. `pan` should return instantly."""

        debug("rotate pan at speed: ",  speed)
        if speed == 0.0:
            moveTurretServo(0, getTurretServoAngle(0))
        elif speed < 0.0:
            changeServoSpeeds(-speed, ["pan"])
            moveTurretServo(0, getTurretBound(0,1))
        elif speed > 0.0:
            changeServoSpeeds(speed, ["pan"])
            moveTurretServo(0, getTurretBound(0,0))

    def tilt(self, speed):
        """This function should behave like the `pan` function, but for the
        tilt motor. It should return instantly."""

        debug("rotate tilt at speed: ", speed)
        if speed == 0.0:
            moveTurretServo(1,getTurretServoAngle(1))
        elif speed < 0.0:
            changeServoSpeeds(-speed, ["tilt"])
            moveTurretServo(1,getTurretBound(1,1))
        elif speed > 0.0:
            changeServoSpeeds(speed, ["tilt"])
            moveTurretServo(1, getTurretBound(1,0))

    # is on deals with the fact that when you release the button, the value changes. 
    # This should probably be handled on the client side though
    def tiltHome(self, isOn):
        if isOn:
            print ("go to tilt home")
            changeServoSpeeds(MAX_SERVO_SPEED, ['tilt'])
            moveTurretServo(1,0.0)

    def panHome(self, isOn):
        if isOn:
            print ("go to pan home")
            changeServoSpeeds(MAX_SERVO_SPEED, ['pan'])
            moveTurretServo(0,0.0)


