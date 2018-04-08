# REAL MOVEMENT SETTINGS
HOME_LEG_POSITIONS = [[-45.0, 0.0, 0.0],[45.0, 0.0, 0.0],[-45.0, 0.0, 0.0],[45.0, 0.0, 0.0]]

TURRET_HOME_POSITIONS = [0,-5]

TURRET_GEAR_RATIO = 3.0
TURRET_SERVO_BOUNDS = [(-150.0,150.0),(-10.0 * TURRET_GEAR_RATIO,7.5 * TURRET_GEAR_RATIO)]

IDEAL_SERVO_POSITIONS = [[45.0,0.0,0.0],[135.0, 0.0, 0.0],[225, 0.0, 0.0],[315, 0.0, 0.0]]

SERVO_BOUNDS = [(-75.0,75.0),(-80.0,80.0),(-130.0,130.0)]

GUN_PIN = 18

# static lengths from robot model
L1_LENGTH = 2.51
L2_LENGTH = 3.95
HIPHORIZ_LENGTH = 1.75
HIPVERTUP_LENGTH = .75
BASE_WIDTH = 6.25
BASE_LENGTH = 6.25

FOOT_RADIUS = .74

# constants
#HOMEPOS_FOOTHEIGHT = -2.25
alpha = 45

HOMEPOS_FOOTHEIGHT = -.5 + (HIPVERTUP_LENGTH-L2_LENGTH)

HOMELEN = -.2+  (HIPHORIZ_LENGTH + L1_LENGTH) / 1.414


HOMEPOS = {"1": [HOMELEN,HOMELEN,HOMEPOS_FOOTHEIGHT],
           "2": [-HOMELEN,HOMELEN, HOMEPOS_FOOTHEIGHT],
           "3": [-HOMELEN,-HOMELEN,HOMEPOS_FOOTHEIGHT],
           "4": [HOMELEN,-HOMELEN,HOMEPOS_FOOTHEIGHT]}




# variables for robot walk gait
LIFTFOOTHEIGHT = .45
DRAG_INTERVALS = 5


global STEP_DELAY
STEP_DELAY = .2

global currentLegServoSpeed
currentLegServoSpeed = 200.0

MAX_STEP_SIZE = 1.0
MAX_SERVO_SPEED = 200.0

# 3 round burst, 1 round burst, auto
SPRAY_TIME_3 = .25
SPRAY_TIME_1 = .08
SPRAY_DELAY = 1.0
spray_time = SPRAY_TIME_3

global autoFire
autoFire = True


global StringMotorMovingBack
StringMotorMovingBack = False

global BBcount
BBcount = 0.0
global pastBBcountBeforeReloading 
pastBBcountBeforeReloading  = 0.0
global saveBBcount
saveBBcount = 0.0

BB_RELOAD_THRESHOLD = 40


global turretStepMode
turretStepMode = False

TURRET_MAX_STEP_ANGLE = 2.0

# ANIMATION SETTINGS

# is animation tells walking.py whether to use animation functions or real functions. running animation.py sets this to True
import os

global isAnimation
isAnimation = True if os.environ.get("IS_ANIMATION", False) else False

global animationSlowMo
animationSlowMo = 1

global t_per_second 
t_per_second = 30

BASE_THICKNESS = 1.0
PANBOX_LENGTH = BASE_LENGTH/3.0
PANBOX_WIDTH = BASE_WIDTH/3.0
PANBOX_HEIGHT = BASE_THICKNESS*2.0
BARREL_LENGTH = 5.0



global isFiring 
isFiring = False

# pan speed then tilt speed
ANIMATED_TURRET_SERVO_SPEED = [100.0,100.0]
SERVO_UPDATE_DELAY = .01

global ServoPos 
ServoPos = [[-45.0, 0.0, 0.0],[45.0, 0.0, 0.0],[-45.0, 0.0, 0.0],[45.0, 0.0, 0.0]]

global servoGoalPos
servoGoalPos = [[-45.0, 0.0, 0.0],[45.0, 0.0, 0.0],[-45.0, 0.0, 0.0],[45.0, 0.0, 0.0]]

# turret servo current pos and goal pos
global TurretPos
TurretPos = [0.0, 0.0]
global turretServoGoalPos
turretServoGoalPos = [0.0, 0.0]

global StringServoPos
StringServoPos = 150.0
global StringGoalPos
StringGoalPos = 150.0

global draggingLegs
draggingLegs = [False,False,False,False]

# made for individual legs so that we could average them together
global legBasePos 
legBasePos = [[0,0,-HOMEPOS_FOOTHEIGHT + BASE_THICKNESS/2.0 + FOOT_RADIUS],[0,0,-HOMEPOS_FOOTHEIGHT + BASE_THICKNESS/2.0 + FOOT_RADIUS],[0,0,-HOMEPOS_FOOTHEIGHT + BASE_THICKNESS/2.0 + FOOT_RADIUS],[0,0,-HOMEPOS_FOOTHEIGHT + BASE_THICKNESS/2.0 + FOOT_RADIUS]]

global BasePos 
BasePos = [0,0,-HOMEPOS_FOOTHEIGHT + BASE_THICKNESS/2.0 + FOOT_RADIUS]

global BaseOrientationAngle
BaseOrientationAngle = 0.0




