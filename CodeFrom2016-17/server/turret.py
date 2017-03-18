
from threading import Thread, Lock, Event

from botnet.logging import *

import time, sys
import traceback as tb

from TESTGAITS.RealAndAnimated.walking import *

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  
GPIO.setup(16, GPIO.OUT)


class GunController(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.firing = False

    ### THIS IS THE FUNCTION
    def fire(self, isOn):
        if isOn:
            print ("FIRING GUN POW POW")
            GPIO.output(16,True)
        else:
            print ("Stopped firing")
            GPIO.output(16,False)

    def run(self):
        self.stop = Event()
        while not self.stop.is_set():
            # why did Aaron put this here? We want the gun to fire on automatic
            '''
            if self.firing:
                try:
                    self.fire()
                except Exception:
                    tb.print_exc(file=sys.stdout)
                    time.sleep(1) # Don't retry instantly on failure
            else:
            '''
            time.sleep(0.05)    

    ### Ignore below for now
    # I stopped ignoring these Aaron :)

    def pan(self, speed):
        """This function should turn on the pan motor at the specified speed,
           positive values are to the right, negative to the left. Zero is off.
           The input will range from -1 to +1. `pan` should return instantly."""

        print ("rotate pan at speed: ",  speed*200)

        if speed*200 > 5.0:
            rotatePan(5, True, speed*200)
        elif speed*200 < -5.0:
            rotatePan(5, False, -speed*200)

    def tilt(self, speed):
        """This function should behave like the `pan` function, but for the tilt
        tilt motor. It should return instantly."""

        print ("rotate tilt at speed: ", speed*200)
        if speed*200 > 5.0:
            rotateTilt(5, False, speed*200)
        elif speed*200 < -5.0:
            rotateTilt(5, True, -speed*200)

    # is on deals with the fact that when you release the button, the value changes. 
    # This should probably be handled on the client side though
    def tiltHome(self, isOn):
        if isOn:
            print ("go to tilt home")
            changeServoSpeeds(100.0, ['tilt'])
            moveTilt(0.0)

    def panHome(self, isOn):
        if isOn:
            print ("go to pan home")
            changeServoSpeeds(100.0, ['pan'])
            movePan(0.0)


