import ik
import numpy as np
import math as m
import copy

RES = .02
STRIDETIME = 1.4
BEATTIME = STRIDETIME/4
LIFTPUT = BEATTIME/10
HOME = np.array(["""DOTHIS"""])

# contains both data about leg and claw position
class gait_leg(ik.leg_data):
    def __init__(self, leg, claw, mode):
        leg_data.init(self, leg.x, leg.y, leg.z, leg.gamma)
        self.claw = claw
        self.mode = mode
        self.home_update_val = [0, 0]

# object to hold multiple legs and some body metadata
class gait_body:
    def __init__(self, legs, legmodes, side, zdist):
        self.legs = legs
        self.legmodes = legmodes
        self.side = side
        self.zdist = zdist
        self.beat = 1
        self.ctr = 0
        self.stridetime = STRIDETIME

# given center, angular velocity, body (with legs & leg data), 
#   and timestep resolution, calculates the next claw locations
def timestep(vx, vy, omega, pitch, roll, height, body):
    # update claw locations for each leg
        # calculate where body needs to be 
        # for each leg in ground mode: 
        #   hyp = m.sqrt(leg.x^2 + leg.y^2)
        #   convert angular velocity to x- and y- 
        #       velocities due to rotation for each hip
        #           let l be the line between the robot's center and the hip
        #           let theta_1 be the initial angle between l and the x axis
        #           let theta_2 be the angle between l and the x axis after rotation 
        #             of (omega * RES) radians
        #           the x- and y- velocity vector components of the rotation are now:
        #           x: cos(theta_2) - cos(theta_1)
        #           y: sin(theta_2) - sin(theta_1)
        #           we know theta_1 is -45, 45, 135, and -135 in order of legs (0-4)
        #   add those x- and y- velocities to normal 
        #       x- and y- velocities to create cumulative x- and y- velocities for both 
        #       translation and rotation
        #   add negative of cumulative x- and y- velocities to leg's associated claw location
    
        # for leg not in ground mode:
        #   where in beat is it?  beat should be split: (this is literally just me making something up)
        #      first .1 beat: lift
        #      middle .8 beat: move to home
        #      final .1 beat: put
        #   determine where in beat it is: 
        #     on each call of timestep within a single beat, increment body.ctr
        #     thus, at any given time, we are (body.ctr*RES)/BEATTIME through current beat
        #     based on that calculation, move claw accordingly
        #       up or down if in first or last .1 of beat
        #       towards home position otherwise
        #         by what amount? when beat changes to make this leg the 
        #           one being picked up: calculate difference between 
        #           pickup location and home in xy plane, find x and y vector 
        #           components, divide both by BEATTIME*.8, 
        #           store in body.legs[current_leg].home_update_val,
        #           move by this each time until last .1 of beat (when 
        #           the robot should be putting the leg down)
    
    # calculate angles for next claw locations and return
    #   ik.extract_angles(body, list of new claw locations, pitch, roll, height, list of z coordinates of claws)
