import math as m
import copy
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
# all references in leg frame use cylindrical coordinates: (theta, r, z) 
# the z-axis is orthogonal to the body, positive being up
# theta is measured from the body frame's x-axis (see below), counter-clockwise
# r is the distance from the z axis
#
#
# BODY FRAME
# (0, 0, 0) is the center of the body projected onto the floor
# x axis points forward
# y axis points to the right
# z axis points positively up, orthogonal to body
#
#
# HALF FRAME
# (0, 0) is the center of the body projected onto the floor
# x axis points forward
# y axis points to the right
#
#
# BODY STATE:   
# pitch: rotation around y-axis
# roll: rotaion around x-axis
# height: distance from floor to center of bottom body
#
#
#
# # # # # # # # # # # # #
# # GLOBAL VARIABLES  # #
# # # # # # # # # # # # # 
# 
# global_trolen: length of trochanter
# global_femlen: length of femur
# global_tiblen: length of tibia 
#
#                                      knee
#                                      /   \
#     \                            femur   tibia
#      \                             /       \
#       \                           /         \
# BODY   hip-----trochanter------elbow         \
#       /                                       \
#      /                                         \
#     /                                          claw
#
#
# PITCH, ROLL, SIDE, GAMMAS, RAD, HEIGHT: default values
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
#
# GRAPHING FUNCTIONS
# get_bodylines: finds lines outlining plane representing body in cartesian coordinates (for graphing)
# get_leglines: fines lines outlining leg segments in cartesian coordinates *IN LEG FRAME* (for graphing)
# change_frame: change the frame of leglines to be plotted with body
#
#
# IK HELPER FUNCTIONS
# body_ik_cascade: ensures variables are in acceptable range in cascade order as follows
#    height, pitch, roll
# leg_ik_cascade: ensures variables are in acceptable range in cascade order as follows
#    radius, angle
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
#     trolen, femlen, tiblen (lengths of leg components)
#     
#   methods: 
#     printleg: prints offset and gamma
#     graphleg: outputs graph of leg
#       inputs:  
#         claw (np.array containing desired claw location in leg frame)
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
#         claws (list of np.arrays containing desired claw locations in half frame)
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
#     list [h, e, k]
#       h is the angle of the hip relative to x-axis of body frame
#       e is the angle of the elbow from trochanter
#       k is the angle of the knee from femur
#
# body_ik
#   inputs:
#     body: body_data object (contains information about legs)
#     claws: list of np.arrays (contain claw locations in half frame)
#     pitch: angle, in degrees, of desired pitch
#     roll: angle, in degrees, of desired roll
#     height: shortest distance from floor to centroid of elbows
#   outputs:
#     newclaws: list of claw positions relative to new coordinate 
#       systems of legs
#
#
#
# # # # # # # # # # # # #
# # # # # Other # # # # #
# # # # # # # # # # # # #
#
# make_standard_bot
#   inputs:
#     (all optional, defaults to global defaults) side, trolen, femlen, tiblen
#   outputs:
#     makes a robot with equidistant claws
#
# extract_angles
#   inputs: body, claws, pitch, roll, height
#   outputs: returns a list of angles [h1, e1, k1, h2, e2, k2, h3, e3, k3, h4, e4, k4]





# # # # # # # # # # # # # # #
# # # # # Globals # # # # # #
# # # # # # # # # # # # # # #

# lengths of trochanter, femur, and tibia
global_trolen = 2.54
global_femlen = 6.16
global_tiblen = 14.08

# Pitch must be in +- PBOUND; roll must be in +- RBOUND
PBOUND, RBOUND = 15, 15

# PITCH, ROLL: default pitch and roll
PITCH, ROLL = 0, 15

# distance from elbow to bottom of body
ZDIST = 2.86

# SIDE: length of test robot body's side
SIDE = 7.62

# GAMMAS: list containing default gamma values for 4 legs
GAMMAS = [315., 45., 135., 225.]

# RAD, HEIGHT: default claw distance from hip in XY plane and Z axis, respectively
RAD, HEIGHT = 12, 8








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
    return np.array([rtod(m.atan2(point[1], point[0])), ((point[0]**2 + point[1]**2) ** .5), point[2]])

# fromcyl(point: np.array of cylindrical coordinates)
#   converts point from cylindrical to cartesian)
def fromcyl(point):
    return np.array([point[1] * m.cos(dtor(point[0])), point[1] * m.sin(dtor(point[0])), point[2]])

# torad(point: np.array of 2d cartesian coordinates)
#   converts from cartesian to radial
def torad(point):
    return np.array([rtod(m.atan2(point[1], point[0])), ((point[0]**2 + point[1]**2) ** .5)])

# fromrad(point: np.array of radial coordinates)
#   converts to cylindrical coordinates
def fromrad(point):
    return np.array([point[1] * m.cos(dtor(point[0])), point[1] * m.sin(dtor(point[0]))])

# get_bodylines(body: body object)
#   returns list of lists of lines which outline robot body 
#   in the form [[x, x], [y, y], [z, z]] for graphing purposes
def get_bodylines(body):
    c = body.side/2
    return [[[c, c], [-c, c], [0, 0]], 
            [[c, -c], [c, c], [0, 0]], 
            [[-c, -c], [c, -c], [0, 0]], 
            [[-c, c], [-c, -c], [0, 0]]]

# get_leglines(leg: leg_data object, claw: desired claw location in cylindrical coordinates in leg frame)
#   returns list of lists of lines which outline leg segments
#   in the form [[x, x], [y, y], [z, z]] for graphing purposes
def get_leglines(leg, claw):
    # Get data
    angles = leg_ik(leg, claw)
    angles[0] += leg.gamma

    # Define locations of joints in space; convert to cartesian
    hipp = np.array([0, 0, 0])
    elbowp = fromcyl(np.array([angles[0], leg.trolen, 0]))
    kneep = fromcyl(np.array([angles[0], leg.trolen + leg.femlen * m.cos(dtor(angles[1])), leg.femlen * m.sin(dtor(angles[1]))]))
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

# body_ik_error_handler(body: body_data object, claws: list of claws in floor frame, 
#   pitch: desired pitch, roll: desired roll, height: 
def body_ik_error_handler(body, claws, pitch, roll, height):
    bigrad = 0;
    for i in range(len(claws)):
        claws[i] = torad(np.array([claws[i][0] - body.legs[i].off[0], claws[i][1] - body.legs[i].off[1]]))
        claws[i][1] = min(max(0, claws[i][1]), body.legs[i].trolen + body.legs[i].femlen + body.legs[i].tiblen)
        bigrad = max(bigrad, claws[i][1])
        x, y = body.legs[i].off[0], body.legs[i].off[1]
        claws[i][0] = (claws[i][0] + 360) % 360
        if (x > 0):
            if (y > 0):
                if ((claws[i][0] > 90 + body.hip_wiggle) and (claws[i][0] < 360 - body.hip_wiggle)):
                    if (claws[i][0] < 225):
                        claws[i][0] = 90 + body.hip_wiggle
                    else:
                        claws[i][0] = 360 - body.hip_wiggle
            else:
                if ((claws[i][0] > body.hip_wiggle) and (claws[i][0] < 270 - body.hip_wiggle)):
                    if (claws[i][0] < 135):
                        claws[i][0] = body.hip_wiggle
                    else:
                        claws[i][0] = body.hip_wiggle
        else: 
            if (y > 0):
                if ((claws[i][0] > 180 + body.hip_wiggle) or (claws[i][0] < 90 - body.hip_wiggle)):
                    if (claws[i][0] < 315):
                        claws[i][0] = 180 + body.hip_wiggle
                    else:
                        claws[i][0] = 90 - body.hip_wiggle
            else:
                if ((claws[i][0] > 270 + body.hip_wiggle) or (claws[i][0] < 180 - body.hip_wiggle)):
                    if ((claws[i][0] < 180 - body.hip_wiggle) and (claws[i][0] > 45)):
                        claws[i][0] = 180 - body.hip_wiggle
                    else:
                        claws[i][0] = 270 + body.hip_wiggle
        claws[i] = fromrad(claws[i])
        claws[i][0] = claws[i][0] + body.legs[i].off[0]
        claws[i][1] = claws[i][1] + body.legs[i].off[1]

    maxheight = m.sqrt(((body.femlen + body.tiblen) ** 2) - bigrad ** 2)
    minheight = body.zdist
    height = min(max(minheight, height), maxheight) 

    pitch_range = min(PBOUND, rtod(m.asin(min(maxheight - height, height - minheight) / (body.side/2))))
    pitch = min(max(-1 * pitch_range, pitch), pitch_range)

    temp = abs((body.side/2) * m.sin(dtor(pitch)))
    roll_range = min(RBOUND, rtod(m.asin((min(maxheight - height, height - minheight) - temp) / (body.side/2))))
    roll = min(max(-1 * roll_range, roll), roll_range)
        
    return(claws, pitch, roll, height)





# # # # # # # # # # # # # # #
# # # # IK functions  # # # #
# # # # # # # # # # # # # # #

# Leg IK
# leg_ik(leg: leg_data object, claw: desired claw location in cylindrical coordinates in leg frame)
#   returns [h, e, k] list
#     h is hip angle from body frame's x-axis
#     e is elbow angle from trochanter
#     k is knee angle from femur
def leg_ik(leg, claw):
    # Constants
    hyp = ((claw[1] - leg.trolen)**2 + claw[2]**2)**.5

    # Inverse Kinematics
    h = claw[0] - leg.gamma
    e = rtod(m.asin((claw[1] - leg.trolen)/hyp) + m.acos((leg.tiblen**2 - leg.femlen**2 - hyp**2)/(-2 * leg.femlen * hyp)) - (m.pi/2))
    k = rtod(m.pi - m.acos((hyp**2 - leg.tiblen**2 - leg.femlen**2)/(-2 * leg.tiblen * leg.femlen)))
    return [h, e, -k]


# Body IK
# body_ik(legs: list of leg_data objects, claws: list of desired claw locations in floor plane,
#      pitch: desired pitch of robot, roll: desired roll of robot)
#   returns newclaws: list of desired claw positions in cylindrical coordinates in leg frame of rotated robot
def body_ik(body, claws, pitch, roll, height):
    hclaws = copy.copy(claws)
    (claws, pitch, roll, height) = body_ik_error_handler(body, claws, pitch, roll, height)
    for i in range(len(hclaws)):
        hclaws[i] = np.append(hclaws[i], -1 * height)
    pc, ps, rc, rs = m.cos(dtor(pitch)), m.sin(dtor(pitch)), m.cos(dtor(roll)), m.sin(dtor(roll))
    pitchm = np.matrix([[pc, 0, -ps], [0, 1, 0], [ps, 0, pc]])
    rollm = np.matrix([[1, 0, 0], [0, rc, -rs], [0, rs, rc]])
    rot = pitchm * rollm

    newclaws = []
    for i in range(len(body.legs)):
        vec = rot * body.legs[i].off[np.newaxis].T 
        newclaws.append(tocyl(hclaws[i] - np.squeeze(np.asarray(vec))))

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
    def __init__(self, x, y, z, gamma, trolen=global_trolen, femlen=global_femlen, tiblen=global_tiblen):
        self.off = np.array([x, y, z])
        self.gamma = gamma
        self.trolen = trolen
        self.femlen = femlen
        self.tiblen = tiblen

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



# body_data(legs: list of leg_data objects, side: length of body side, zdist: distance
#   from elbow to bottom of body)
#   printbody
#     prints number of legs, sidelength, and calls printleg for each leg
#   graphbody(claws: desired claw locations in cylindrical coordinates in leg frames, 
#       pitch: desired pitch of body, roll: desired roll of body)
#     outputs graph of body
class body_data:
    def __init__(self, legs, side, zdist=ZDIST, trolen=global_trolen, femlen=global_femlen, tiblen=global_tiblen):
        self.numlegs = len(legs)
        self.legs = legs
        self.side = side
        self.zdist = zdist
        self.trolen, self.femlen, self.tiblen = trolen, femlen, tiblen
        self.hip_wiggle = m.asin((side/2)/(trolen + femlen + tiblen))

    # prints number of legs, sidelength, and calls printleg for each leg
    def printbody(self):
        print("Number of legs: ", self.numlegs)
        print("Sidelength: ", self.side)
        for i in range(self.numlegs):
            print("Leg", i)
            self.legs[i].printleg()
            print("\n")

    # outputs graph of body in 3d space with legs
    def graphbody(self, claws, pitch, roll, height):
        print("Pitch: ", pitch)
        print("Roll: ", roll)
        newclaws = body_ik(self, claws, pitch, roll, height)
        cclaws = []
        for i in range(len(newclaws)):
            cclaws.append(fromcyl(newclaws[i]))
            cclaws[i] += self.legs[i].off

        # Plot
        mpl.rcParams['legend.fontsize'] = 10
        fig = plt.figure().gca(projection='3d')
        
        bl = get_bodylines(self)
        fig.plot(bl[0][0], bl[0][1], bl[0][2], c='b')
        fig.plot(bl[1][0], bl[1][1], bl[1][2], c='k')
        fig.plot(bl[2][0], bl[2][1], bl[2][2], c='k')
        fig.plot(bl[3][0], bl[3][1], bl[3][2], c='k')
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



# # # # # # # # # # # # # # #
# # # # # # Other # # # # # #
# # # # # # # # # # # # # # #

# make_standard_bot()
#   creates a bot with equidistant claws at distance RAD from hip
def make_standard_bot(side=SIDE, trolen=global_trolen, femlen=global_femlen, tiblen=global_tiblen, zdist=ZDIST):
    s = side/2
    claws = []
    xc = s + RAD * m.cos(dtor(45))
    yc = s + RAD * m.cos(dtor(45))
    claws.append(np.array([xc, -yc]))
    claws.append(np.array([xc, yc]))
    claws.append(np.array([-xc, yc]))
    claws.append(np.array([-xc, -yc]))
    print(claws)

    legs = []
    legs.append(leg_data(s, -s, 0, GAMMAS[0], trolen, femlen, tiblen))
    legs.append(leg_data(s, s, 0, GAMMAS[1], trolen, femlen, tiblen))
    legs.append(leg_data(-s, s, 0, GAMMAS[2], trolen, femlen, tiblen))
    legs.append(leg_data(-s, -s, 0, GAMMAS[3], trolen, femlen, tiblen))

    body = body_data(legs, side, zdist, trolen, femlen, tiblen)

    return(claws, body)

# extract_angles(body: body_data object, claws: list of claw positions, pitch: desired pitch in degrees, roll: desired roll in degrees)
#   returns list of angles [h1, e1, k1, h2, e2, k2, h3, e3, k3, h4, e4, k4]
def extract_angles(body, claws, pitch, roll, height):
    newclaws = body_ik(body, claws, pitch, roll, height)
    ret_angles = []
    for i in range(len(body.legs)):
        ret_angles += leg_ik(body.legs[i], newclaws[i])
    return ret_angles








# Test Code
# Takes in 0, 1, or 2 command line arguments
#   If no command line arguments: use default PITCH and ROLL values
#   If 1 command line argument: make it PITCH value, use default ROLL value
#   If 2 command line arguments: make first PITCH value, make second ROLL value
#if (len(sys.argv) > 1):
#    PITCH = float(sys.argv[1])
#    if (len(sys.argv) > 2):
#        ROLL = float(sys.argv[2])
#
#claws, body = make_standard_bot()
#body.graphbody(claws, PITCH, ROLL, HEIGHT) 
#print("Done")
