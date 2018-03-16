import math as m
import copy
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import collections as mc
import numpy as np
import macros
import helpers
from objs import leg_data
from objs import body_data


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
    e = helpers.rtod(m.asin((claw[1] - leg.trolen)/hyp) + m.acos((leg.tiblen**2 - leg.femlen**2 - hyp**2)/(-2 * leg.femlen * hyp)) - (m.pi/2))
    k = helpers.rtod(m.pi - m.acos((hyp**2 - leg.tiblen**2 - leg.femlen**2)/(-2 * leg.tiblen * leg.femlen)))
    return [h, e, -k]


# Body IK
# body_ik(legs: list of leg_data objects, claws: list of desired claw locations in floor plane,
#      pitch: desired pitch of robot, roll: desired roll of robot)
#   returns newclaws: list of desired claw positions in cylindrical coordinates in leg frame of rotated robot
def body_ik(body, claws, pitch, roll, height, heights):
    hclaws = copy.copy(claws)
    # (claws, pitch, roll, height) = body_ik_error_handler(body, claws, pitch, roll, height)
    for i in range(len(hclaws)):
        hclaws[i] = np.append(hclaws[i], -1 * height)
    pc, ps, rc, rs = m.cos(helpers.dtor(pitch)), m.sin(helpers.dtor(pitch)), m.cos(helpers.dtor(roll)), m.sin(helpers.dtor(roll))
    pitchm = np.matrix([[pc, 0, -ps], [0, 1, 0], [ps, 0, pc]])
    rollm = np.matrix([[1, 0, 0], [0, rc, -rs], [0, rs, rc]])
    rot = pitchm * rollm

    newclaws = []
    for i in range(len(body.legs)):
        vec = rot * body.legs[i].off[np.newaxis].T 
        newclaws.append(helpers.tocyl(hclaws[i] - np.squeeze(np.asarray(vec))))

    # Incorporate leg lifts after greater body_ik calculation
    lift_legs(newclaws, heights)

    return newclaws

def lift_legs(claws, heights):
    for i in range(len(claws)):
        if (heights[i] > 0):
            claws[i][2] = heights[i]
    
    

# # # # # # # # # # # # # # #
# # # # # # Other # # # # # #
# # # # # # # # # # # # # # #

# make_standard_bot()
#   creates a bot with equidistant claws at distance RAD from hip with macros.NUMLEGS legs (and sides)
def make_standard_bot(side=macros.SIDE, trolen=macros.TROLEN, femlen=macros.FEMLEN, tiblen=macros.TIBLEN, zdist=macros.ZDIST):
    claws = []
    legs = []
    poly_rad = side/(2 * m.sin(m.pi/macros.NUMLEGS))   # polygon radius
    for i in range(macros.NUMLEGS):
        # calculate unit multipliers
        x_unit = m.cos(helpers.dtor(macros.GAMMAS[i]))
        y_unit = m.sin(helpers.dtor(macros.GAMMAS[i]))

        # append appropriate data to claws and legs
        claws.append(np.array([(x_unit * (poly_rad + macros.DEFAULT_RADIUS)), (y_unit * (poly_rad + macros.DEFAULT_RADIUS))]))
        legs.append(leg_data(i, x_unit * poly_rad, y_unit * poly_rad, macros.GAMMAS[i], trolen, femlen, tiblen))

    # create a body with the legs
    body = body_data(legs, side, zdist, trolen, femlen, tiblen)

    return(claws, body)

# extract_angles(body: body_data object, claws: list of claw positions, pitch: desired pitch in degrees, roll: desired roll in degrees)
#   returns list of angles [h1, e1, k1, h2, e2, k2, h3, e3, k3, h4, e4, k4]
def extract_angles(body, claws, pitch, roll, height, heights=[0,0,0,0]):
    newclaws = body_ik(body, claws, pitch, roll, height, heights)
    ret_angles = []
    for i in range(len(body.legs)):
        ret_angles += leg_ik(body.legs[i], newclaws[i])
    return ret_angles

# # body_ik_error_handler(body: body_data object, claws: list of claws in floor frame, 
# #   pitch: desired pitch, roll: desired roll, height: 
# def body_ik_error_handler(body, claws, pitch, roll, height):
#     bigrad = 0;
#     for i in range(len(claws)):
#         claws[i] = helpers.torad(np.array([claws[i][0] - body.legs[i].off[0], claws[i][1] - body.legs[i].off[1]]))
#         claws[i][1] = min(max(0, claws[i][1]), body.legs[i].trolen + body.legs[i].femlen + body.legs[i].tiblen)
#         bigrad = max(bigrad, claws[i][1])
#         x, y = body.legs[i].off[0], body.legs[i].off[1]
#         claws[i][0] = (claws[i][0] + 360) % 360
#         if (x > 0):
#             if (y > 0):
#                 if ((claws[i][0] > 90 + body.hip_wiggle) and (claws[i][0] < 360 - body.hip_wiggle)):
#                     if (claws[i][0] < 225):
#                         claws[i][0] = 90 + body.hip_wiggle
#                     else:
#                         claws[i][0] = 360 - body.hip_wiggle
#             else:
#                 if ((claws[i][0] > body.hip_wiggle) and (claws[i][0] < 270 - body.hip_wiggle)):
#                     if (claws[i][0] < 135):
#                         claws[i][0] = body.hip_wiggle
#                     else:
#                         claws[i][0] = body.hip_wiggle
#         else: 
#             if (y > 0):
#                 if ((claws[i][0] > 180 + body.hip_wiggle) or (claws[i][0] < 90 - body.hip_wiggle)):
#                     if (claws[i][0] < 315):
#                         claws[i][0] = 180 + body.hip_wiggle
#                     else:
#                         claws[i][0] = 90 - body.hip_wiggle
#             else:
#                 if ((claws[i][0] > 270 + body.hip_wiggle) or (claws[i][0] < 180 - body.hip_wiggle)):
#                     if ((claws[i][0] < 180 - body.hip_wiggle) and (claws[i][0] > 45)):
#                         claws[i][0] = 180 - body.hip_wiggle
#                     else:
#                         claws[i][0] = 270 + body.hip_wiggle
#         claws[i] = helpers.fromrad(claws[i])
#         claws[i][0] = claws[i][0] + body.legs[i].off[0]
#         claws[i][1] = claws[i][1] + body.legs[i].off[1]

#     maxheight = m.sqrt(((body.femlen + body.tiblen) ** 2) - bigrad ** 2)
#     minheight = body.zdist
#     height = min(max(minheight, height), maxheight) 

#     pitch_range = 0
#     if (min(maxheight - height, height - minheight) < body.side/2):
#         pitch_range = min(macros.PITCH_BOUND, helpers.rtod(m.asin(min(maxheight - height, height - minheight) / (body.side/2))))
#     else:
#         pitch_range = macros.PITCH_BOUND
#     pitch = min(max(-1 * pitch_range, pitch), pitch_range)

#     temp = abs((body.side/2) * m.sin(helpers.dtor(pitch)))
#     roll_range = 0
#     if (min(maxheight - height, height - minheight) - temp < body.side/2):
#         roll_range = min(macros.ROLL_BOUND, helpers.rtod(m.asin(min(maxheight - height, height - minheight) / (body.side/2))))
#     else:
#         roll_range = macros.ROLL_BOUND
# #    roll_range = min(macros.ROLL_BOUND, helpers.rtod(m.asin((min(maxheight - height, height - minheight) - temp) / (body.side/2))))
#     roll = min(max(-1 * roll_range, roll), roll_range)
        
#     return(claws, pitch, roll, height)





# # # # TEST CODE

# claws, body = make_standard_bot()
# body.graphbody(claws, macros.DEFAULT_PITCH, macros.DEFAULT_ROLL, macros.DEFAULT_HEIGHT)
# print("Done")
