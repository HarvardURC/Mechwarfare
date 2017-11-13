import math as m
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import collections as mc
import numpy as np
import sys

# # # # # # # # # # # # # 
# # # # GEOMETRY  # # # #
# # # # # # # # # # # # #
#
# LEG FRAME
# (0, 0, 0) is the hip
#
# all references in leg frame use cylindrical coordinates: (theta, r, z) 
#
# the z-axis is orthogonal to the body, positive being up
# 
# theta is measured from the body frame's x-axis (see below), counter-clockwise
#
# r is the distance from the z axis
#
#
#
# BODY FRAME
# (0, 0, 0) is the center of the body projected onto the floor
#
# x axis points positively directly forward
#
# y axis points positively to the right
#
# z axis points positively up
#
# all axes are at all time orthogonal to the robot's body; frame shifts 
# as robot moves
#
# BODY STATE:   
# pitch: rotation around y-axis
# roll: rotaion around x-axis
#
#
#
# # # # # # # # # # # # #
# # GLOBAL VARIABLES  # #
# # # # # # # # # # # # # 
# 
# trolen: length of trochanter
# femlen: length of femur
# tiblen: length of tibia
#
# see engineering journal for nomenclature details
#
#
#
# # # # # # # # # # # # #
# # HELPER FUNCTIONS  # #
# # # # # # # # # # # # #
#
# dtor: converts degrees to radians
# rtod: converts radians to degrees
#
# tocyl: converts cartesian to cylindrical
# fromcyl: converts cylindrical to cartesian, assumes input angles in degrees
#
# get_bodylines: finds lines outlining plane representing body in cartesian coordinates (for graphing)
# get_leglines: fines lines outlining leg segments in cartesian coordinates *IN LEG FRAME* (for graphing)
#
#
#
# # # # # # # # # # # # #
# # # # CLASSES # # # # #
# # # # # # # # # # # # #
#
# leg_data is a class for containing data about a leg
#   inputs: 
#     x, y, z (offset of hip from center of robot)
#     gamma (offset of 0 position of servo from x-axis in degrees)
#     
#   methods: 
#     printleg: prints offset and gamma
#     graphleg: outputs graph of leg
#       inputs: 
#         claw (np.array containing desired claw location)
#
#
# body_data is a class for containing data about a robot
#   inputs:
#     legs (list of leg_data objects)
#     side (length of robot side)
#
#   methods:
#     printbody: prints list of legs and side length
#     graphbody: outputs graph of body and legs 
#       inputs: 
#         claws (list of np.arrays containing desired claw locations)
#         pitch (desired pitch of robot body)
#         roll (desired roll of robot body)
#
#
#
# # # # # # # # # # # # #
# # # IK Functions  # # #
# # # # # # # # # # # # #
#
# leg_ik
#   inputs:
#     leg: leg_data object (contains angle offset information)
#     claw: np.array (contains desired claw location)
#   outputs:
#     tuple (h, e, k)
#       h is the angle of the hip relative to x-axis of body frame
#       e is the angle of the elbow from trochanter
#       k is the angle of the knee from femur
#
# body_ik
#   inputs:
#     body: body_data object (contains information about legs)
#     claws: list of np.arrays (contain vectors describing claw 
#          locations relative to center of robot)
#     pitch: angle, in degrees, of desired pitch
#     roll: angle, in degrees, of desired roll
#   outputs:
#     newclaws: list of claw positions relative to new coordinate 
#       systems of legs
#
#
#
# # # # # # # # # # # # #
# # # Functionality # # #
# # # # # # # # # # # # #
#
# python ik.py [first] [second]
# If no optional command line arguments are given, run body_ik 
#   with default PITCH and ROLL values.
# If 1 optional command line argument [first] is given, run body_ik
#   with PITCH=first and default ROLL value
# If two optional command line arguments [first] and [second] are given, 
#   run body_ik with PITCH=first and ROLL=second




# # # # # # # # # # # # # # #
# # # # # Globals # # # # # #
# # # # # # # # # # # # # # #

# trolen: length of trochanter
trolen = 2.54

# femlen: length of femur
femlen = 6.16

# tiblen: length of tibia
tiblen = 14.08

# PITCH: default pitch
PITCH = 0

# ROLL: default roll
ROLL = 0

# SIDE: length of test robot body's side
SIDE = 7.62

# GAMMAS: list containing default gamma values for 4 legs
GAMMAS = [315, 45, 135, 225]




# # # # # # # # # # # # # # #
# # # Helper Functions  # # #
# # # # # # # # # # # # # # #

# rtod(x: number in radians)
#   converts x from radians to degrees
def rtod(x):
    return (x * 180 / m.pi)

# dtor(x: number in degrees)
#   converts x from degrees to radians
def dtor(x):
    return (x * m.pi / 180)

# tocyl(point: np.array of 3d cartesian coordinates)
#   converts point from cartesian to cylindrical
def tocyl(point):
    return np.array([rtod(m.atan2(-point[1], point[0])), ((point[0]**2 + point[1]**2) ** .5), point[2]])

# fromcyl(point: np.array of cylindrical coordinates)
#   converts point from cylindrical to cartesian)
def fromcyl(point):
    return np.array([point[1] * m.cos(dtor(point[0])), -point[1] * m.sin(dtor(point[0])), point[2]])

# get_bodylines(body: body object)
#   returns list of lists of lines which outline robot body 
#   in the form [[x, x], [y, y], [z, z]] for graphing purposes
def get_bodylines(body):
    c = body.side/2
    return [[[c, -c], [c, c], [0, 0]], 
            [[-c, -c], [c, -c], [0, 0]], 
            [[-c, c], [-c, -c], [0, 0]], 
            [[c, c], [-c, c], [0, 0]]]

# get_leglines(leg: leg_data object, claw: desired claw location in cylindrical coordinates in leg frame)
#   returns list of lists of lines which outline leg segments
#   in the form [[x, x], [y, y], [z, z]] for graphing purposes
def get_leglines(leg, claw):
    # Get data
    angles = leg_ik(leg, claw)

    # Define locations of joints in space; convert to cartesian
    hipp = np.array([0, 0, 0])
    elbowp = fromcyl(np.array([angles[0], trolen, 0]))
    kneep = fromcyl(np.array([angles[0], trolen + femlen * m.cos(dtor(angles[1])), femlen * m.sin(dtor(angles[1]))]))
    clawp = fromcyl(np.array([angles[0], claw[1], claw[2]]))

    return [[[hipp[0], elbowp[0]], [hipp[1], elbowp[1]], [hipp[2], elbowp[2]]],
            [[elbowp[0], kneep[0]], [elbowp[1], kneep[1]], [elbowp[2], kneep[2]]],
            [[kneep[0], clawp[0]], [kneep[1], clawp[1]], [kneep[2], clawp[2]]]]

# change_frame(lines: list of lines in graphing format, off: cartesian offset of frame lines are in)
#   returns lines in non-offset frame
def change_frame(lines, off):
    for i in range(len(lines[0])):
        for j in range(len(lines)):
            lines[j][i][0] += off[i]
            lines[j][i][1] += off[i]
    return lines
            




# # # # # # # # # # # # # # #
# # # # IK functions  # # # #
# # # # # # # # # # # # # # #

# Leg IK
# leg_ik(leg: leg_data object, claw: desired claw location in cylindrical coordinates in leg frame)
#   returns (h, e, k) tuple
#     h is hip angle from body frame's x-axis
#     e is elbow angle from trochanter
#     k is knee angle from femur
def leg_ik(leg, claw):
    # Constants
    hyp = ((claw[1] - trolen)**2 + claw[2]**2)**.5

    # Inverse Kinematics
    h = claw[0]
    e = rtod(m.asin((claw[1] - trolen)/hyp) + m.acos((tiblen**2 - femlen**2 - hyp**2)/(-2 * femlen * hyp)) - (m.pi/2))
    k = rtod(m.pi - m.acos((hyp**2 - tiblen**2 - femlen**2)/(-2 * tiblen * femlen)))
    return (h, e, k)


# Body IK
# body_ik(legs: list of leg_data objects, claws: list of desired claw locations in cylindrical coordinates in leg frame,
#      pitch: desired pitch of robot, roll: desired roll of robot)
#   returns newclaws: list of desired claw positions in cylindrical coordinates in leg frame of rotated robot
def body_ik(body, claws, pitch, roll):
    pc, ps = m.cos(dtor(pitch)), m.sin(dtor(pitch))
    rc, rs = m.cos(dtor(roll)), m.sin(dtor(roll))
    pitchm = np.matrix([[pc, 0, -ps], [0, 1, 0], [ps, 0, pc]])
    rollm = np.matrix([[1, 0, 0], [0, rc, rs], [0, -rs, rc]])
    rot = pitchm * rollm

    newclaws = []
    for i in range(len(body.legs)):
        vec = rot * body.legs[i].off[np.newaxis].T 
        newclaws.append(tocyl(fromcyl(claws[i]) - np.squeeze(np.asarray(vec))))

    return newclaws
    



# # # # # # # # # # # # # # #
# # # # # Classes # # # # # #
# # # # # # # # # # # # # # #

# leg_data(x, y, z: cartesian offset of hip from body center, gamma: 0 position of hip servo)
#   printleg
#     prints leg offset and gamma
#   graphleg(claw: desired claw location in cylindrical coordinates in leg frame)
#     outputs graph of leg
class leg_data:
    def __init__(self, x, y, z, gamma):
        self.off = np.array([x, y, z])
        self.gamma = gamma

    # prints leg offset and gamma
    def printleg(self):
        print('  Offset: ', self.off)
        print('  Gamma: ', self.gamma)

    # outputs graph of leg with 3 subcomponents:
    #   projection onto (x, y) plane, projection onto (z, self.gamma) plane, and 3d render
    def graphleg(self, claw):
        ll = get_leglines(self, claw)

        # Plot
        mpl.rcParams['legend.fontsize'] = 10
        fig = plt.figure(1)

        axtop = fig.add_subplot(131)
        axtop.plot(ll[0][0], ll[0][1], c='g') 
        axtop.plot(ll[1][0], ll[1][1], c='y') 
        axtop.plot(ll[2][0], ll[2][1], c='r') 
        plt.show
        axside = fig.add_subplot(132)
        axside.plot(ll[0][0], ll[0][2], c='g') 
        axside.plot(ll[1][0], ll[1][2], c='y') 
        axside.plot(ll[2][0], ll[2][2], c='r') 
        plt.show

        ax3 = fig.add_subplot(133, projection='3d')
        ax3.plot(ll[0][0], ll[0][1], ll[0][2], c='g')
        ax3.plot(ll[1][0], ll[1][1], ll[1][2], c='y')
        ax3.plot(ll[2][0], ll[2][1], ll[2][2], c='r')
        plt.show()



# body(legs: list of leg_data objects, side: length of body side)
#   printbody
#     prints number of legs, sidelength, and calls printleg for each leg
#   graphbody(claws: desired claw locations in cylindrical coordinates in leg frames, 
#       pitch: desired pitch of body, roll: desired roll of body)
#     outputs graph of body
class body_data:
    def __init__(self, legs, side):
        self.numlegs = len(legs)
        self.legs = []
        for i in range(self.numlegs):
            self.legs.append(legs[i])
        self.side = side

    # prints number of legs, sidelength, and calls printleg for each leg
    def printbody(self):
        print("Number of legs: ", self.numlegs)
        print("Sidelength: ", self.side)
        for i in range(self.numlegs):
            print("Leg", i)
            self.legs[i].printleg()
            print("\n")

    # outputs graph of body in 3d space with legs
    def graphbody(self, claws, pitch, roll):
        print("Pitch: ", pitch)
        print("Roll: ", roll)
        newclaws = body_ik(self, claws, pitch, roll)
        cclaws = []
        for i in range(len(newclaws)):
            cclaws.append(fromcyl(newclaws[i]))
            cclaws[i] += self.legs[i].off

        # Plot
        mpl.rcParams['legend.fontsize'] = 10
        fig = plt.figure().gca(projection='3d')
        
        bl = get_bodylines(self)
        fig.plot(bl[0][0], bl[0][1], bl[0][2], c='k')
        fig.plot(bl[1][0], bl[1][1], bl[1][2], c='k')
        fig.plot(bl[2][0], bl[2][1], bl[2][2], c='k')
        fig.plot(bl[3][0], bl[3][1], bl[3][2], c='b')
        for i in range(len(newclaws)):
            ll = change_frame(get_leglines(self.legs[i], newclaws[i]), self.legs[i].off)
            fig.plot(ll[0][0], ll[0][1], ll[0][2], c='g')
            fig.plot(ll[1][0], ll[1][1], ll[1][2], c='y')
            fig.plot(ll[2][0], ll[2][1], ll[2][2], c='r')
        fig.text(cclaws[0][0], cclaws[0][1], cclaws[0][2], "0")
        fig.text(cclaws[1][0], cclaws[1][1], cclaws[1][2], "1")
        fig.text(cclaws[2][0], cclaws[2][1], cclaws[2][2], "2")
        fig.text(cclaws[3][0], cclaws[3][1], cclaws[3][2], "3")
        plt.xlabel('x')
        plt.ylabel('y')

        plt.show()

        for i in range(len(newclaws)):
            print("Leg:", i)
            self.legs[i].printleg()
            self.legs[i].graphleg(newclaws[i])









# Test Code
# Takes in 0, 1, or 2 command line arguments
#   If no command line arguments: use default PITCH and ROLL values
#   If 1 command line argument: make it PITCH value, use default ROLL value
#   If 2 command line arguments: make first PITCH value, make second ROLL value
if (len(sys.argv) > 1):
    PITCH = float(sys.argv[1])
    if (len(sys.argv) > 2):
        ROLL = float(sys.argv[2])

legs = []
s = SIDE/2
legs.append(leg_data(s, s, 0, GAMMAS[0]))
legs.append(leg_data(s, -s, 0, GAMMAS[1]))
legs.append(leg_data(-s, -s, 0, GAMMAS[2]))
legs.append(leg_data(-s, s, 0, GAMMAS[3]))

distance = (s**2 + s**2)**.5
claws = []
claws.append(np.array([315, 12 + distance, -8]))
claws.append(np.array([45, 20 + distance, -8]))
claws.append(np.array([135, 12 + distance, -8]))
claws.append(np.array([225, 12 + distance, -8]))

robot = body_data(legs, SIDE)
robot.graphbody(claws, PITCH, ROLL)
print("Done")
