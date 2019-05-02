#
#  MACROS FOR ROBOTICS MOTOR FUNCTIONS
#
import math as m
import numpy as np
import helpers


# # # # # # # # # # # # 
# # GENERAL MACROS  # #
# # # # # # # # # # # #

# ROBOT DIMENSIONS
# Number of legs (If this is changed, changes will not propagate to DEFSTATES)
NUMLEGS = 4

# Lengths of leg segments (centimeters)
TROLEN = 2.54
FEMLEN = 6.16
TIBLEN = 14.08

# Distance between hip joint and bottom of robot (centimeters)
ZDIST = 2.86

# Angle values of 0 for hip servos (radians)
#   --assumes hip servos are 0'd with leg parallel
#     to line between robot center and hip
#   --assumes front two legs symmetric about x-axis (forward)
GAMMAS = []
for i in range(NUMLEGS):
    GAMMAS.append(i*(360/NUMLEGS) + (360/NUMLEGS)/2)

# Length of robot side (centimeters)
SIDE = 7.86


# DEFAULTS
# Default robot height (centimeters)
DEFAULT_HEIGHT = 12

# Default claw distance from hip (centimeters)
DEFAULT_RADIUS = 8

# Default pitch and roll values (degrees)
DEFAULT_PITCH = 0
DEFAULT_ROLL = 0

# Default yaw value
DEFAULT_YAW = 0

# Default home positions of legs in body frame
HOMES = []
poly_rad = SIDE/(2 * m.sin(m.pi/NUMLEGS))          # polygon radius
clawdist_from_center = poly_rad + DEFAULT_RADIUS   # claw distance from center of robot
for i in range(NUMLEGS):
    HOMES.append([clawdist_from_center * m.cos(helpers.dtor(GAMMAS[i])), 
        clawdist_from_center * m.sin(helpers.dtor(GAMMAS[i])), -1 * DEFAULT_HEIGHT])

# Default velocities for walking
DEFAULT_VX = 1
DEFAULT_VY = 0
DEFAULT_OMEGA = 40

DEFAULT_PAN = 0
DEFAULT_TILT = -30


# # # # # # # # # # # # #
# # # # IK MACROS # # # #
# # # # # # # # # # # # #

# Bounds on heights of claw
MAX_Z = 0
MIN_Z = -15



# # # # # # # # # # # #
# # # RADIO MACROS  # #
# # # # # # # # # # # #

# Bounds are absolute value bounds; maxes have corresponding mins elsewhere defined
# Bounds on pitch, roll, and yaw
PITCH_BOUND = 25
ROLL_BOUND = 25
YAW_BOUND = 20

PAN_BOUND = 45
TILT_BOUND_UPPER = 80
TILT_BOUND_LOWER = -60 

# Bounds on linear and angular velocities (minimums for movement below)
V_MAX = 50
OMEGA_MAX = 70


# # # # # # # # # # # # 
# # # GAIT MACROS # # #
# # # # # # # # # # # #

# BOUNDS ON ANGLES
SERVO_LIMITS = {"HIP_MIN": 95, "HIP_MAX": 185, "KNEE_MIN": 63, "KNEE_MAX": 212, "ELB_MIN": 9, "ELB_MAX": 135} 
# convert bounds in degrees to bounds in dynamixel units and cast to int
for k in SERVO_LIMITS.keys():
    SERVO_LIMITS[k] *= 1/.29
    SERVO_LIMITS[k] = int(SERVO_LIMITS[k])


# TIME CONTROLS
# Length of time step (seconds)
TIMESTEP = 0.02  

# Length of full stride (seconds)
STRIDELENGTH = 0.6

# Fraction of idle beat leg is being lifted/lowered
RAISEFRAC = 0.5  

# Maximum height foot is raised (centimeters)
RAISEH = 2
# Phase tolerance for moving to goal
TOLERANCE = 0.01 

# Fraction of stride that legs spend in the air
LIFT_PHASE = 1/float(NUMLEGS)

# Minimum velocities required for robot to walk
MIN_V = 2
MIN_OMEGA = 5

# List of default leg state information
phases = np.array([0, 0.5, 0, 0.5])
DEFSTATES = []
for i in range(NUMLEGS):
    DEFSTATES.append([
        float(HOMES[i][0]),   # current x position
        float(HOMES[i][1]),   # Current y position
        float(HOMES[i][2]),                   # Current z position
        phases[i],     # Phase offset
        float(HOMES[i][0]),   # Home x position
        float(HOMES[i][1])])   # Home y position
