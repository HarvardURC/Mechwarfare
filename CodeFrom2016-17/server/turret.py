
from threading import Thread, Lock, Event

from botnet.logging import *

import time, sys
import traceback as tb

from TESTGAITS.RealAndAnimated.walking import *

class GunController(Thread):
    def __init__(self, *args, **kwargs):
        super(GunController, self).__init__(*args, **kwargs)
        self.firing = False

    ### THIS IS THE FUNCTION
    def fire(self):
        """This function should fire one round from the turret."""

        print ("FIRING GUN POW POW")
        time.sleep(0.5)

    def run(self):
        self.stop = Event()
        while not self.stop.is_set():
            if self.firing:
                try:
                    self.fire()
                except Exception:
                    tb.print_exc(file=sys.stdout)
                    time.sleep(1) # Don't retry instantly on failure
            else:
                time.sleep(0.1)    

    ### Ignore below for now
    # I stopped ignoring these Aaron :)

    def pan(self, speed):
        """This function should turn on the pan motor at the specified speed,
           positive values are to the right, negative to the left. Zero is off.
           The input will range from -1 to +1. `pan` should return instantly."""

        print ("rotate pan at speed: ",  speed)
        rotatePan(5, True, speed)

    def tilt(self, speed):
        """This function should behave like the `pan` function, but for the tilt
        tilt motor. It should return instantly."""

        print ("rotate tilt at speed: ", speed)
        #raise NotImplementedError()

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


