

# REAL MOVEMENT SETTINGS
HOME_LEG_POSITIONS = [[-45.0, 0.0, 0.0],[45.0, 0.0, 0.0],[-45.0, 0.0, 0.0],[45.0, 0.0, 0.0]]


IDEAL_SERVO_POSITIONS = [[45.0,0.0,0.0],[135.0, 0.0, 0.0],[225, 0.0, 0.0],[315, 0.0, 0.0]]

SERVO_BOUNDS = [(-75.0,75.0),(-80.0,80.0),(-125.0,125.0)]

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

STEP_DELAY = .3



# ANIMATION SETTINGS
global ServoPos 
ServoPos = [[-45.0, 0.0, 0.0],[45.0, 0.0, 0.0],[-45.0, 0.0, 0.0],[45.0, 0.0, 0.0]]

global t

global t_per_second 
t_per_second = 30

BASE_THICKNESS = 1.0