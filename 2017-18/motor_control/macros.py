#
#
#
#
#  MACROS FOR ROBOTICS MOTOR FUNCTIONS
#
#
#
#
import math as m
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




# # # # # # # # # # # # #
# # # # IK MACROS # # # #
# # # # # # # # # # # # #

# BOUNDS
# Bounds on pitch and roll: must fall within +/- these values (degrees)
PITCH_BOUND = 10
ROLL_BOUND = 10

# Bounds on heights of claw
MAX_Z = 0
MIN_Z = -15




# # # # # # # # # # # # 
# # # GAIT MACROS # # #
# # # # # # # # # # # #

# BOUNDS ON ANGLES


# TIME CONTROLS
# Length of time step (seconds)
TIMESTEP = 0.02  

# Length of full stride (seconds)
STRIDELENGTH = 0.5

# Fraction of idle beat leg is being lifted/lowered
RAISEFRAC = 0.5  

# Maximum height foot is raised (centimeters)
RAISEH = 2
# Phase tolerance for moving to goal
TOLERANCE = 0.01 

# Fraction of stride that legs spend in the air
LIFT_PHASE = 1/float(NUMLEGS)

# List of default leg state information
phases = [0, 0.5, 0, 0.5]
DEFSTATES = []
for i in range(NUMLEGS):
	DEFSTATES.append([
		float(HOMES[i][0]),   # current x position
		float(HOMES[i][1]),   # Current y position
		float(HOMES[i][2]),                   # Current z position
		phases[i],     # Phase offset
		float(HOMES[i][0]),   # Home x position
		float(HOMES[i][1])])   # Home y position
