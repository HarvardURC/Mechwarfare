
from threading import Thread, Lock, Event

import time

from botnet.logging import *

from enum import Enum

from TESTGAITS.RealAndAnimated.walking import *
import TESTGAITS.RealAndAnimated.settings as s
import math

Direction = Enum("Direction", "STOP FORWARD BACKWARD STRAFE_RIGHT STRAFE_LEFT TURN_RIGHT TURN_LEFT")

class MotorController:
    ### IMPLEMENT THE METHODS OF THIS CLASS TO ACTUALLY DRIVE THE ROBOT.
    ### speed will be a float in the range 0 < speed <= 1
    def __init__(self):
        ### Initialization Code
        pass

    def STOP(self, speed):
        print ("GO TO HOME POS: ",  stepsize)
        goToHomeFromAnyPosition()

    def FORWARD(self, stepsize):
        print ("walk forward at stepsize: ",  stepsize)
        walkingForward('F', 1, stepsize)

    def BACKWARD(self, stepsize):
        print ("walk backwards at stepsize: ",  stepsize)
        walkingForward('B', 1, stepsize)

    def STRAFE_RIGHT(self, stepsize):
        print ("walk right at stepsize: ",  stepsize)
        walkingForward('R', 1, stepsize)

    def STRAFE_LEFT(self, stepsize):
        print ("walk left at stepsize: ",  stepsize)
        walkingForward('L', 1, stepsize)

    def TURN_RIGHT(self, speed):
        # 10 degrees rotation for now
        # True implies clockwise
        print ("turn right at speed: ",  speed*MAX_SERVO_SPEED)
        rotate(20, True, speed*MAX_SERVO_SPEED)

    def TURN_LEFT(self, speed):
        # 10 degrees rotation for now
        print ("turn left at speed: ", speed)
        rotate(20, False, speed*MAX_SERVO_SPEED)

ZERO = (0, 0)
def nonzero(x):
    return (time.time(), x)
    
class MovementController(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.daemon = True # There may be a better way
        self._directions = dict(zip(Direction,[ZERO for i in Direction]))
        self._directions[Direction.STOP] = (1, 0)
        self.recalculate()
        self.motors = MotorController()

    def forward(self, val):
        self._directions[Direction.FORWARD] = ZERO
        self._directions[Direction.BACKWARD] = ZERO
        if val > 0:
            self._directions[Direction.FORWARD] = nonzero(val)
        elif val < 0:
            self._directions[Direction.BACKWARD] = nonzero(-val)
        self.recalculate()
            

    def strafe(self, val):
        self._directions[Direction.STRAFE_RIGHT] = ZERO
        self._directions[Direction.STRAFE_LEFT] = ZERO
        if val > 0:
            self._directions[Direction.STRAFE_RIGHT] = nonzero(val)
        elif val < 0:
            self._directions[Direction.STRAFE_LEFT] = nonzero(-val)
        self.recalculate()

    def left(self, val):
        if val:
            self._directions[Direction.TURN_LEFT] = nonzero(1)
        else:
            self._directions[Direction.TURN_LEFT] = ZERO
        self.recalculate()

    def right(self, val):
        if val:
            self._directions[Direction.TURN_RIGHT] = nonzero(1)
        else:
            self._directions[Direction.TURN_RIGHT] = ZERO
        self.recalculate()

    def __key(self, val):
        return (-val[1][1], -val[1][0])
        
    def recalculate(self):
        d = sorted(self._directions.items(), key=self.__key)[0]
        self._direction = d[0]
        self._speed = d[1][1]
        return d
        
    def run(self):
        self.stop = Event()
        while not self.stop.is_set():
            if self._speed != 0:
                getattr(self.motors, self._direction.name)(self._speed)
            else:
                time.sleep(0.1)
