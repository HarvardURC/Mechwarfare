import numpy as np
import math as m
import copy
import macros
import objs
import ik
import helpers

# from matplotlib import pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D


# dt = 0.05  # Time step in seconds
# steplen = 1.  # Step time in seconds
# t = 0.  # Time in seconds
# raisefrac = 0.5  # Fraction of idle beat leg is being lifted/ lowered
# raiseh = 1.  # Maximum height foot is raised in cm
# tolerance = 0.01 # Phase tolerance for moving to goal
# simtime = 4. # Time in seconds to run the simulation


def calculate_step(cur, goal, phase, endphase):
    """Calculate the next step to reach a goal at a certain time"""

    # Check if the end phase is very close or past
    if phase > endphase - macros.TOLERANCE:
        # If so, go to the goal right away
        return goal - cur
    # Otherwise, go at the speed that will reach the goal at the target time
    return (goal - cur) * macros.TIMESTEP / (macros.STRIDELENGTH * (endphase - phase))


def update_leg(state, vx, vy, omega, t, phase_limit):
    """Updates the state of a leg at each timestep, given state and robot velocity"""

    # The phase of the walking cycle is calculated
    phase = (t + state.phase_offset * macros.STRIDELENGTH) % macros.STRIDELENGTH

    # If the leg is being lifted
    if phase < phase_limit:

        # Move it horizontally towards the home position
        state.x += calculate_step(state.x, state.home_x, phase, phase_limit)
        state.y += calculate_step(state.y, state.home_y, phase, phase_limit)

        # If it's being lifted
        if phase < phase_limit * macros.RAISEFRAC:
            # Lift it
            state.z += calculate_step(state.z, macros.RAISEH, phase, phase_limit * macros.RAISEFRAC)
        # If it's being lowered,
        elif phase > phase_limit * (1 - macros.RAISEFRAC):
            # Lower it
            state.z += calculate_step(state.z, 0, phase, phase_limit)
    else:
        # Otherwise, move it horizontally based on robot velocity
        state.x += (-vx + state.y * omega) * macros.TIMESTEP
        state.y += (-vy - state.x * omega) * macros.TIMESTEP


def timestep(body, vx, vy, omega, t, phase_limit=macros.PHASE_LIMIT):
    """Updates the states of every leg for a given robot body, given state and robot velocity"""

    # Error check phase_limit
    phase_limit = min(phase_limit, macros.MAX_PHASE_LIMIT)

    # Variables to assist with formatted return
    xys = []
    zs = []

    # Update each leg
    for i in range(len(body.legs)):
        update_leg(body.legs[i].state, vx, vy, helpers.dtor(omega), t, phase_limit)
        xys.append([body.legs[i].state.x, body.legs[i].state.y])
        zs.append(body.legs[i].state.z)

    t += macros.TIMESTEP

    # Return formatted array of angles
    return(macros.TIMESTEP, ik.extract_angles(body, xys, macros.DEFAULT_PITCH, macros.DEFAULT_ROLL, macros.DEFAULT_HEIGHT, zs))






# if _name_ == "_main_":
#     leg1state = [1., 1., 0., 0., 1., 1.]  # X, Y, Z, phase offset, home X, home Y
#     leg2state = [1., -1., 0., 0.25, 1., -1.]  # X, Y, Z, phase offset, home X, home Y
#     leg3state = [-1., -1., 0., 0.5, -1., -1.]  # X, Y, Z, phase offset, home X, home Y
#     leg4state = [-1., 1., 0., 0.75, -1., 1.]  # X, Y, Z, phase offset, home X, home Y

#     vx = 1
#     vy = 0
#     omega = 1

#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     plt.autoscale(enable=True, axis='both', tight=None)

#     for i in range(int(simtime/macros.TIMESTEP)+1):
#         update_leg(leg1state, vx, vy, omega)
#         ax.scatter(leg1state[0],leg1state[1],leg1state[2],c='b')

#         update_leg(leg2state, vx, vy, omega)
#         ax.scatter(leg2state[0], leg2state[1], leg2state[2], c='r')

#         update_leg(leg3state, vx, vy, omega)
#         ax.scatter(leg3state[0], leg3state[1], leg3state[2], c='g')

#         update_leg(leg4state, vx, vy, omega)
#         ax.scatter(leg4state[0], leg4state[1], leg4state[2], c='y')

#         t += macros.TIMESTEP

#     plt.show()


# # given center, angular velocity, body (with legs & leg data), 
# #   and timestep resolution, calculates the next claw locations
# def timestep(vx, vy, omega, pitch, roll, height, body):
#     # update claw locations for each leg
#         # calculate where body needs to be 
#         # for each leg in ground mode: 
#         #   hyp = m.sqrt(leg.x^2 + leg.y^2)
#         #   convert angular velocity to x- and y- 
#         #       velocities due to rotation for each hip
#         #           let l be the line between the robot's center and the hip
#         #           let theta_1 be the initial angle between l and the x axis
#         #           let theta_2 be the angle between l and the x axis after rotation 
#         #             of (omega * RES) radians
#         #           the x- and y- velocity vector components of the rotation are now:
#         #           x: cos(theta_2) - cos(theta_1)
#         #           y: sin(theta_2) - sin(theta_1)
#         #           we know theta_1 is -45, 45, 135, and -135 in order of legs (0-4)
#         #   add those x- and y- velocities to normal 
#         #       x- and y- velocities to create cumulative x- and y- velocities for both 
#         #       translation and rotation
#         #   add negative of cumulative x- and y- velocities to leg's associated claw location
#     rot_ang = ik.fromrad(omega * macros.RESOLUTION)
#     for i in range(len(body.legs)):
#         if (body.legs[i].mode != "up"):
#             t_1 = i * 90 + 45
#             t_2 = theta_1 - rot_ang
#             body.legs[i].claw[0] = body.legs[i].claw[0] - (vx + m.cos(t_2) - m.cos(t_1))
#             body.legs[i].claw[1] = body.legs[i].claw[1] - (vy + m.sin(t_2) - m.sin(t_1))
            
    
#         # for leg not in ground mode:
#         #   where in beat is it?  beat should be split: (this is literally just me making something up)
#         #      first .1 beat: lift
#         #      middle .8 beat: move to home
#         #      final .1 beat: put
#         #   determine where in beat it is: 
#         #     on each call of timestep within a single beat, increment body.ctr
#         #     thus, at any given time, we are (body.ctr*RES)/BEATTIME through current beat
#         #     based on that calculation, move claw accordingly
#         #       up or down if in first or last .1 of beat
#         #       towards home position otherwise
#         #         by what amount? when beat changes to make this leg the 
#         #           one being picked up: calculate difference between 
#         #           pickup location and home in xy plane, find x and y vector 
#         #           components, divide both by BEATTIME*.8, 
#         #           store in body.legs[current_leg].home_update_val,
#         #           move by this each time until last .1 of beat (when 
#         #           the robot should be putting the leg down)
#         else:
#             if (body.ctr == 0):
#                 body.legs[i].homeupd[0] = (body.legs[i].claw[0] - HOMES[i][0])/(BEATTIME/RES)
#                 body.legs[i].homeupd[1] = (body.legs[i].claw[1] - HOMES[i][0])/(BEATTIME/RES)
            
    
#     # calculate angles for next claw locations and return
#     #   ik.extract_angles(body, list of new claw locations, pitch, roll, height, list of z coordinates of claws)
