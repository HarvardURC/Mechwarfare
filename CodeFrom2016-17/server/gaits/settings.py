

# REAL MOVEMENT SETTINGS
HOME_LEG_POSITIONS = [[-45.0, 0.0, 0.0],[45.0, 0.0, 0.0],[-45.0, 0.0, 0.0],[45.0, 0.0, 0.0]]

TURRET_HOME_POSITIONS = [0,0]

TURRET_GEAR_RATIO = 3.0
TURRET_SERVO_BOUNDS = [(-150.0,150.0),(-10.0 * TURRET_GEAR_RATIO,10.0 * TURRET_GEAR_RATIO)]

IDEAL_SERVO_POSITIONS = [[45.0,0.0,0.0],[135.0, 0.0, 0.0],[225, 0.0, 0.0],[315, 0.0, 0.0]]

SERVO_BOUNDS = [(-75.0,75.0),(-80.0,80.0),(-125.0,125.0)]

GUN_PIN = 18

# constants
HOMEPOS_FOOTHEIGHT = -2.25

HOMEPOS = {"1": [3.0,3.0,HOMEPOS_FOOTHEIGHT],
           "2": [-3.0,3.0, HOMEPOS_FOOTHEIGHT],
           "3": [-3.0,-3.0,HOMEPOS_FOOTHEIGHT],
           "4": [3.0,-3.0,HOMEPOS_FOOTHEIGHT]}


# static lengths from robot model
L1_LENGTH = 2.51
L2_LENGTH = 2.45
HIPHORIZ_LENGTH = 1.75
HIPVERTUP_LENGTH = .75
BASE_WIDTH = 6.25
BASE_LENGTH = 6.25

FOOT_RADIUS = .74

# variables for robot walk gait
LIFTFOOTHEIGHT = .8
DRAG_INTERVALS = 5


global STEP_DELAY
STEP_DELAY = .2

STEP_SIZE = 1.5
MAX_SERVO_SPEED = 200.0

SPRAY_TIME_3 = .25
SPRAY_TIME_1 = .08
SPRAY_DELAY = 1.0
spray_time = SPRAY_TIME_3




# ANIMATION SETTINGS

# is animation tells walking.py whether to use animation functions or real functions. running animation.py sets this to True
import os

global isAnimation
isAnimation = True if os.environ.get("IS_ANIMATION", False) else False

global t_per_second 
t_per_second = 30

BASE_THICKNESS = 1.0
PANBOX_LENGTH = BASE_LENGTH/3.0
PANBOX_WIDTH = BASE_WIDTH/3.0
PANBOX_HEIGHT = BASE_THICKNESS*2.0
BARREL_LENGTH = 5.0



# degrees per second
ANIMATED_LEG_SERVO_SPEED = 200.0

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

global draggingLegs
draggingLegs = [False,False,False,False]

# made for individual legs so that we could average them together
global legBasePos 
legBasePos = [[0,0,-HOMEPOS_FOOTHEIGHT + BASE_THICKNESS/2.0 + FOOT_RADIUS],[0,0,-HOMEPOS_FOOTHEIGHT + BASE_THICKNESS/2.0 + FOOT_RADIUS],[0,0,-HOMEPOS_FOOTHEIGHT + BASE_THICKNESS/2.0 + FOOT_RADIUS],[0,0,-HOMEPOS_FOOTHEIGHT + BASE_THICKNESS/2.0 + FOOT_RADIUS]]

global BasePos 
BasePos = [0,0,-HOMEPOS_FOOTHEIGHT + BASE_THICKNESS/2.0 + FOOT_RADIUS]

global BaseOrientationAngle
BaseOrientationAngle = 0.0




