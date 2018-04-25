import math as m
import numpy as np
import copy, macros, helpers
from objs import leg_data, body_data
from time import time


# IK functions

def fix_angles_2(theta):
    while(theta > 180):
        theta += -360
    while(theta < -180):
        theta += 360
    return(theta)

# Leg IK
# leg_ik(leg: leg_data object, claw: desired claw location in cylindrical coordinates in leg frame)
#   returns [h, e, k] list
# If inputs are invalid, returns a list of length 4
def leg_ik(leg, claw, times={}):
    
    # Timing value
    tv_leg_ik = time()

    # Constants
    hyp = ((claw[1] - leg.trolen)**2 + claw[2]**2)**.5

    try:
        # Inverse Kinematics
        h = claw[0] - leg.gamma
        e = helpers.rtod(m.asin((claw[1] - leg.trolen)/hyp) + m.acos((leg.tiblen**2 - leg.femlen**2 - hyp**2)/(-2 * leg.femlen * hyp)) - (m.pi/2)) - 90
        k = helpers.rtod(m.pi - m.acos((hyp**2 - leg.tiblen**2 - leg.femlen**2)/(-2 * leg.tiblen * leg.femlen))) - 180

        times = helpers.dict_timer("Ik.leg_ik", times, time()-tv_leg_ik)

        return np.array([fix_angles_2(h), fix_angles_2(e), fix_angles_2(k)])

    except:

        times = helpers.dict_timer("Ik.leg_ik", times, time()-tv_leg_ik)

        print("Invalid parameters.  Leg ik failed.")
        return np.array([0, 1, 2, 3])


# Body IK
# body_ik(legs: list of leg_data objects, claws: list of desired claw locations in floor plane,
#      pitch: desired pitch of robot, roll: desired roll of robot)
#   returns newclaws: list of desired claw positions in cylindrical coordinates in leg frame of rotated robot
def body_ik(body, claws, pitch, roll, height, zs, times={}):

    # Timing value
    tv_body_ik = time()
    
    # copy claws to prevent error propagation and add z coordinate
    hclaws = copy.copy(claws)
    for i in range(len(hclaws)):
        hclaws[i] = np.append(hclaws[i], -1 * height)

    # create rotation matrix
    pc, ps, rc, rs = m.cos(helpers.dtor(pitch)), m.sin(helpers.dtor(pitch)), m.cos(helpers.dtor(roll)), m.sin(helpers.dtor(roll))
    pitchm = np.matrix([[pc, 0, -ps], [0, 1, 0], [ps, 0, pc]])
    rollm = np.matrix([[1, 0, 0], [0, rc, -rs], [0, rs, rc]])
    rot = pitchm * rollm

    # put leg offsets through rotation and subtract difference
    newclaws = []
    for i in range(len(body.legs)):
        vec = rot * body.legs[i].off[np.newaxis].T 
        newclaws.append(helpers.tocyl(hclaws[i] - np.squeeze(np.asarray(vec))))

    # incorporate leg lifts
    for i in range(len(zs)):
        if (zs[i] > 0):
            newclaws[i][2] = -1*(height-zs[i])

    times = helpers.dict_timer("Ik.body_ik", times, time()-tv_body_ik) 

    return newclaws
    
    

# Other

# make_standard_bot()
#   creates a bot with equidistant claws at distance RAD from hip with macros.NUMLEGS legs (and sides)
def make_standard_bot(side=macros.SIDE, trolen=macros.TROLEN, femlen=macros.FEMLEN, tiblen=macros.TIBLEN, zdist=macros.ZDIST):

    # Timing value
    tv_msb = time()

    claws = []
    legs = []
    poly_rad = side/(2 * m.sin(m.pi/macros.NUMLEGS))   # polygon radius
    for i in range(macros.NUMLEGS):
        # calculate unit multipliers
        x_unit = m.cos(helpers.dtor(macros.GAMMAS[i]))
        y_unit = m.sin(helpers.dtor(macros.GAMMAS[i]))

        # append appropriate data to claws and legs
        claws.append([(x_unit * (poly_rad + macros.DEFAULT_RADIUS)), (y_unit * (poly_rad + macros.DEFAULT_RADIUS))])
        legs.append(leg_data(i, x_unit * poly_rad, y_unit * poly_rad, macros.GAMMAS[i], trolen, femlen, tiblen))
        if (i == 0):
            legs[i].state.signs = np.array([1, 1])
        elif (i == 1):
            legs[i].state.signs = np.array([-1, 1])
        elif (i == 2):
            legs[i].state.signs = np.array([-1, -1])
        else:
            legs[i].state.signs = np.array([1, -1])

    # create a body with the legs
    body = body_data(legs, side, zdist, trolen, femlen, tiblen)

    # Timing print
    print("Make_standard_bot time: ", (time() - tv_msb))

    return(claws, body)

# extract_angles(body: body_data object, claws: list of claw positions, pitch: desired pitch in degrees, roll: desired roll in degrees)
#   returns list of angles [h1, e1, k1, h2, e2, k2, h3, e3, k3, h4, e4, k4]
def extract_angles(body, claws, pitch=macros.DEFAULT_PITCH, roll=macros.DEFAULT_ROLL, height=macros.DEFAULT_HEIGHT, zs=[0,0,0,0], times={}):

    # Timing value
    tv_ea = time()

    # Returns np.array
#    newclaws = body_ik(body, claws, pitch, roll, height, zs, times)
#    ret_angles = np.array([])
#    for i in range(len(body.legs)):
#        ret_angles = np.append(ret_angles, (leg_ik(body.legs[i], newclaws[i], times)))

    # Returns list
    newclaws = body_ik(body, claws, pitch, roll, height, zs, times)
    ret_angles = []
    for i in range(len(body.legs)):
        ret_angles = ret_angles + leg_ik(body.legs[i], newclaws[i], times))


    times = helpers.dict_timer("Ik.extract_angles", times, time()-tv_ea)

    return ret_angles

## body_ik_error_handler(body: body_data object, claws: list of claws in floor frame, 
##   pitch: desired pitch, roll: desired roll, height: 
#def body_ik_error_handler(body, claws, pitch, roll, height, zs):
#    # variable for height
#    bigrad = 0
#
#    # check each claw location
#    for i in range(len(claws)):
#        xoff, yoff = body.legs[i].off[0], body.legs[i].off[1]
#
#        # convert claw to radial coordinates
#        claws[i] = helpers.torad(np.array([claws[i][0]-xoff, claws[i][1]-yoff]))
#
#        # bound radius 
#        claws[i][1] = helpers.bound(claws[i][1], 0, body.legs[i].trolen+body.legs[i].femlen+body.legs[i].tiblen)
#
#        # update bigrad
#        bigrad = max(bigrad, claws[i][1])
#
#        # bound theta
#        claws[i][0] = helpers.degreesmod(claws[i][0])
#        claws[i][0] = helpers.bound(claws[i][0], body.legs[i].gamma-body.hip_wiggle, body.legs[i].gamma+body.hip_wiggle)
#
#        # return to cartesian coordinates and add leg offset back in
#        claws[i] = helpers.fromrad(claws[i])
#        claws[i][0] = claws[i][0] + xoff
#        claws[i][1] = claws[i][1] + yoff
#
#    trlen, flen, tilen = body.trolen, body.femlen, body.tiblen
#
#    # bound height
#    maxheight, minheight = m.sqrt(((flen+tilen)**2) - (bigrad-trlen)**2), body.zdist
#    height = helpers.bound(height, minheight, maxheight)
#
#    # bound pitch
#    pitch = helpers.bound(pitch, macros.PITCH_BOUND, macros.PITCH_BOUND*-1)
#    # check if height affects possible pitch and rebound accordingly
#    heightzone = m.sin(abs(pitch)) * (body.side/2)
#    if (height > maxheight-heightzone or height-heightzone < minheight):
#        pitchsign = pitch/abs(pitch)
#        pitch = pitchsign*m.asin(heightzone/(body.side/2))
#
#    # bound roll
#    roll = helpers.bound(roll, macros.ROLL_BOUND, macros.ROLL_BOUND*-1)
#    # check if height and pitch affect possible pitch and rebound accordingly
#    heightzone = heightzone - (m.sin(abs(pitch)) * (body.side/2))
#    if (height > maxheight-heightzone or height-heightzone < minheight):
#        rollsign = roll/abs(roll)
#        roll = rollsign*m.asin(heightzone/(body.side/2))
#
#    # bound zs
#    for z in zs:
#        helpers.bound(z, macros.MIN_Z, macros.MAX_Z)
#
#    return(claws, pitch, roll, height, zs)
