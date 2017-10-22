
from threading import Thread, Lock, Event

import time

from botnet.logging import *

from enum import Enum

from server.gaits.walking import *
import server.gaits.settings as s
import math
import time

# get foot heights
foot1pos = getDisplacementFromAngles(1, getCurrentAngles(1))
foot2pos = getDisplacementFromAngles(2, getCurrentAngles(2))
foot3pos = getDisplacementFromAngles(3, getCurrentAngles(3))
foot4pos = getDisplacementFromAngles(4, getCurrentAngles(4))
# stand up if legs are flat
if ((foot1pos[2] > -1.0) and (foot2pos[2] > -1.0) and (foot3pos[2] > -1.0) and (foot4pos[2]> -1.0)):
    moveAndDragMultFeet([1, 3, 2, 4],  [[1.5* s.HOMEPOS["1"][0],1.5*s.HOMEPOS["1"][1],0], [1.5*s.HOMEPOS["3"][0],1.5*s.HOMEPOS["3"][1],0], [1.5*s.HOMEPOS["2"][0],1.5*s.HOMEPOS["2"][1],0], [1.5*s.HOMEPOS["4"][0],1.5*s.HOMEPOS["4"][1],0]],[0,0,0,0])
    moveAndDragMultFeet([1, 3, 2, 4],  [[1.5* s.HOMEPOS["1"][0],1.5*s.HOMEPOS["1"][1],-2], [1.5*s.HOMEPOS["3"][0],1.5*s.HOMEPOS["3"][1],-2], [1.5*s.HOMEPOS["2"][0],1.5*s.HOMEPOS["2"][1],-2], [1.5*s.HOMEPOS["4"][0],1.5*s.HOMEPOS["4"][1],-2]], [0,0,0,0])
    moveAndDragMultFeet([1, 3],  [[s.HOMEPOS["1"][0],s.HOMEPOS["1"][1],-2], [s.HOMEPOS["3"][0],s.HOMEPOS["3"][1],-2]],[1,1])
    moveAndDragMultFeet([2, 4],  [[s.HOMEPOS["2"][0],s.HOMEPOS["2"][1],-2], [s.HOMEPOS["4"][0],s.HOMEPOS["4"][1],-2]], [1,1])

    moveAndDragMultFeet([1, 2, 3, 4],  [s.HOMEPOS["1"], s.HOMEPOS["2"], s.HOMEPOS["3"], s.HOMEPOS["4"]],[0,0,0,0])
    moveAndDragMultFeet([1, 3],  [s.HOMEPOS["1"], s.HOMEPOS["3"]],[1,1])
    moveAndDragMultFeet([2, 4],  [s.HOMEPOS["2"], s.HOMEPOS["4"]],[1,1])

Direction = Enum("Direction", "STOP FORWARD BACKWARD STRAFE_RIGHT STRAFE_LEFT TURN_RIGHT TURN_LEFT")

class MotorController:
    ### IMPLEMENT THE METHODS OF THIS CLASS TO ACTUALLY DRIVE THE ROBOT.
    ### speed will be a float in the range 0 < speed <= 1
    def __init__(self):
        ### Initialization Code
        pass

    def STOP(self, speed):
        goToHomeFromAnyPosition()

    def FORWARD(self, stepsize):
        walkingForward('F', 1, stepsize)

    def BACKWARD(self, stepsize):
        walkingForward('B', 1, stepsize)

    def STRAFE_RIGHT(self, stepsize):
        walkingForward('R', 1, stepsize)

    def STRAFE_LEFT(self, stepsize):
        walkingForward('L', 1, stepsize)

    def TURN_RIGHT(self, speed):
        # 10 degrees rotation for now
        # True implies clockwise
        rotate(10, True, speed*s.MAX_SERVO_SPEED)

    def TURN_LEFT(self, speed):
        # 10 degrees rotation for now
        rotate(10, False, speed*s.MAX_SERVO_SPEED)

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
        self._last_direction = Direction.STOP
        while not self.stop.is_set():
            if self._last_direction != self._direction:
                if self._last_direction != Direction.STOP:
                    goToHomeFromAnyPosition()
                self._last_direction = self._direction
            if self._speed != 0:
                getattr(self.motors, self._direction.name)(self._speed)
            else:
                time.sleep(0.1)
