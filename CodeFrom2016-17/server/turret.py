
from threading import Thread, Lock, Event

from botnet.logging import *
import math
import time, sys
import traceback as tb

from server.gaits.walking import *
import server.gaits.settings as s


def sign(x):
    if x > 0:
        return 1.
    elif x < 0:
        return -1.
    elif x == 0:
        return 0.
    else:
        return x


if not s.isAnimation:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)  
    GPIO.setup(s.GUN_PIN, GPIO.OUT, initial=GPIO.LOW)


# start by moving servo to 150
if not s.isAnimation:
    getattr(robot,"string").goal_position = 150
else:
    s.StringGoalPos = 150




class GunController(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.firing = False

    def changeTurretMode(self, isOn):
        if isOn:
            if not s.turretStepMode:
                # currently in continuous mode, so stop the turret by calling stopTurret which is for stopping the continuous mode turret 
                stopTurretServo(0)
                stopTurretServo(1)

                changeServoSpeeds(150, ["pan","tilt"])

            # change turret mode
            s.turretStepMode = not s.turretStepMode

    def manualReload(self, isOn):
        if isOn:
            s.pastBBcountBeforeReloading = s.BBcount
            getattr(robot,"string").goal_position = -150
            time.sleep(2)
            getattr(robot,"string").goal_position = 150


    def changeSprayTime(self, isOn):
        if isOn:
            s.autoFire = not s.autoFire

    ### THIS IS THE FUNCTION
    def fire(self, isOn):
        if isOn:
            debug("Started Firing")
            self.firing = True
        else:
            debug("Stopped firing")
            self.firing = False


    def run(self):
        self.stop = Event()
        s.BBcount = 0.0
        s.pastBBcountBeforeReloading = 0.0
        while not self.stop.is_set():
            if not s.isAnimation:
                # firing code, choose between auto and 3 burst
                if self.firing:
                    if s.autoFire:
                        GPIO.output(18,True)
                        time.sleep(.05)
                        s.BBcount += .05 * 12
                    # else do 3 spray
                    else:
                        GPIO.output(18,True)
                        time.sleep(s.spray_time)
                        GPIO.output(18,False)
                        time.sleep(s.SPRAY_DELAY)
                        s.BBcount += 3
                else:
                    GPIO.output(18,False)
                    time.sleep(.05)

                # reload code
                if s.BBcount > (s.pastBBcountBeforeReloading + s.BB_RELOAD_THRESHOLD):
                    print (s.BBcount, "hello")
                    moveStringMotor()
                    time.sleep(.05)

            else:
                # animation firing code, choose between auto and 3 burst
                if self.firing:
                    if s.autoFire:
                        s.isFiring = True
                        time.sleep(.05)
                        s.BBcount += .05 * 12
                    # else do 3 spray
                    else:
                        s.isFiring = True
                        time.sleep(s.spray_time)
                        s.isFiring = False
                        time.sleep(s.SPRAY_DELAY)
                        s.BBcount += 3
                else:
                    s.isFiring = False
                    time.sleep(.05)

                if s.BBcount > (s.pastBBcountBeforeReloading + s.BB_RELOAD_THRESHOLD):
                    moveStringMotor()
                    time.sleep(.05)



    def pan(self, val):
        """This function should turn on the pan motor at the specified speed,
           positive values are to the right, negative to the left. Zero is off.
           The input will range from -1 to +1. `pan` should return instantly."""

        debug("rotate pan at: ",  val)
        if not s.turretStepMode:
            # in continuous mode
            speed = sign(val) * pow(val,2.0) * s.MAX_SERVO_SPEED/2.0
            if speed == 0.0:
                stopTurretServo(0)
            elif speed < 0.0:
                changeServoSpeeds(-speed, ["pan"])
                moveTurretServo(0, getTurretBound(0,1))
            elif speed > 0.0:
                changeServoSpeeds(speed, ["pan"])
                moveTurretServo(0, getTurretBound(0,0))
        else:
            # in step mode
            moveTurretServo(0, getTurretServoAngle(0) - val * s.TURRET_MAX_STEP_ANGLE)

    def tilt(self, val):
        """This function should behave like the `pan` function, but for the
        tilt motor. It should return instantly."""

        debug("rotate tilt at: ", val)

        # tilt in continuous mode is different in animation versus real because theres a gear ratio
        if s.isAnimation:
            speed = -1* sign(val) * pow(val,2.0) * s.MAX_SERVO_SPEED/2.0
            # in continuous mode
            if not s.turretStepMode:
                if speed == 0.0:
                    stopTurretServo(1)
                elif speed < 0.0:
                    changeServoSpeeds(-speed, ["tilt"])
                    moveTurretServo(1,getTurretBound(1,0))
                elif speed > 0.0:
                    changeServoSpeeds(speed, ["tilt"])
                    moveTurretServo(1, getTurretBound(1,1))
            else:
                # in step mode
                moveTurretServo(1, getTurretServoAngle(1) - val * s.TURRET_MAX_STEP_ANGLE)
        else:
            # in continuous mode
            if not s.turretStepMode:
                speed = -1* sign(val) * pow(val,2.0) * s.MAX_SERVO_SPEED/2.0
                if speed == 0.0:
                    stopTurretServo(1)
                elif speed < 0.0:
                    changeServoSpeeds(-speed, ["tilt"])
                    moveTurretServo(1,getTurretBound(1,1))
                elif speed > 0.0:
                    changeServoSpeeds(speed, ["tilt"])
                    moveTurretServo(1, getTurretBound(1,0))
            else:
                # in step mode
                moveTurretServo(1, getTurretServoAngle(1) + val * s.TURRET_MAX_STEP_ANGLE)


    # is on deals with the fact that when you release the button, the value changes. 
    # This should probably be handled on the client side though

    def panHome(self, isOn):
        if isOn:
            print ("go to pan home")
            changeServoSpeeds(s.MAX_SERVO_SPEED, ['pan'])
            moveTurretServo(0,s.TURRET_HOME_POSITIONS[0])

    def tiltHome(self, isOn):
        if isOn:
            print ("go to tilt home")
            changeServoSpeeds(s.MAX_SERVO_SPEED, ['tilt'])
            moveTurretServo(1,s.TURRET_HOME_POSITIONS[1])

    def reload(self, isOn):
        if isOn:
            moveStringMotor()




