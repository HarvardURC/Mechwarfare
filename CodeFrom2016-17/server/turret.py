
from threading import Thread, Lock, Event

from botnet.logging import *

import time, sys
import traceback as tb

from TESTGAITS.py3.realGaitsLeg3 import *

class GunController(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.firing = False

    ### THIS IS THE FUNCTION
    def fire(self):
        """This function should fire one round from the turret."""
        moveTurret(__import__("random").randint(0,150))
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

def pan(speed):
    """This function should turn on the pan motor at the specified speed,
       positive values are to the right, negative to the left. Zero is off.
       The input will range from -1 to +1. `pan` should return instantly."""
    raise NotImplementedError()

def tilt(speed):
    """This function should behave like the `pan` function, but for the tilt
       tilt motor. It should return instantly."""
    raise NotImplementedError()
