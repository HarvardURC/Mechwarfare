import ik
import numpy as np
import math as m
import copy

RES = .02

# contains both data about leg and claw position
class gait_leg(ik.leg_data):
    def __init__(self, leg, claw, mode):
        leg_data.init(self, leg.x, leg.y, leg.z, leg.gamma)
        self.claw = claw
        self.mode = mode

# object to hold multiple legs and some body metadata
class gait_body:
    def __init__(self, legs, legmodes, side, zdist):
        self.legs = legs
        self.legmodes = legmodes
        self.side = side
        self.zdist = zdist

# given center, angular velocity, body (with legs & leg data), 
#   and timestep resolution, calculates the next claw locations
def timestep(vx, vy, omega, body, res=RES):
    # calculate where body needs to be 
        # curloc[x] - vx * res, curloc[y] - vy * res
        # calculate difference in hip location due to 
        #   rotation, incorporate that into new claw location as well

    # how to deal with legs in the air?
        # hard-code phasing, keep track of where in phase the 
        #   bot is, update correspondingly
        # hard-code length of beat
    
    # update body.legs[i].claw for all i
    
    # calculate angles for next claw locations and return
