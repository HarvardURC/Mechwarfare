import numpy as np
import math as m
import copy
import macros
import objs
import ik
import helpers

#from matplotlib import pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D


# dt = 0.05  # Time step in seconds
# steplen = 1.  # Step time in seconds
# tick = 0.  # Time in seconds
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


def update_leg(state, vx, vy, omega, t, lift_phase):
    """Updates the state of a leg at each timestep, given state and robot velocity"""

    # The phase of the walking cycle is calculated
    phase = (t + state.phase_offset * macros.STRIDELENGTH) % macros.STRIDELENGTH

    # If the leg is being lifted
    if phase < lift_phase:
        state.home_off_x = -1 * (-vx + state.home_y * omega) * (macros.STRIDELENGTH * (1-lift_phase) / 2)
        state.home_off_y = -1 * (-vy - state.home_x * omega) * (macros.STRIDELENGTH * (1-lift_phase) / 2)

        # Move it horizontally towards the home position
        state.x += calculate_step(state.x, state.home_x + state.home_off_x, phase, lift_phase)
        state.y += calculate_step(state.y, state.home_y + state.home_off_y, phase, lift_phase)

        # If it's being lifted
        if phase < lift_phase * macros.RAISEFRAC:
            # Lift it
            state.z += calculate_step(state.z, macros.RAISEH, phase, lift_phase * macros.RAISEFRAC)
        # If it's being lowered,
        elif phase > lift_phase * (1 - macros.RAISEFRAC):
            # Lower it
            state.z += calculate_step(state.z, 0, phase, lift_phase)
    else:
        # Otherwise, move it horizontally based on robot velocity
        state.x += (-vx + state.y * omega) * macros.TIMESTEP
        state.y += (-vy - state.x * omega) * macros.TIMESTEP



def timestep(body, vx, vy, omega, t, lift_phase=macros.LIFT_PHASE):
    """Updates the states of every leg for a given robot body, given state and robot velocity"""

    # Variables to assist with formatted return
    xys = []
    zs = []

    # Update each leg
    for i in range(len(body.legs)):
        update_leg(body.legs[i].state, vx, vy, helpers.dtor(omega), t, lift_phase)
        xys.append([body.legs[i].state.x, body.legs[i].state.y])
        zs.append(body.legs[i].state.z)

    t += macros.TIMESTEP


    # Return formatted array of angles
    return(macros.TIMESTEP, ik.extract_angles(body, xys, macros.DEFAULT_PITCH, macros.DEFAULT_ROLL, macros.DEFAULT_HEIGHT, zs))



def caldoescode():
    leg1state = objs.leg_state(0)
    leg2state = objs.leg_state(0)
    leg3state = objs.leg_state(0)
    leg4state = objs.leg_state(0)
    leg1state.reset(1., 1., 0., 0., 1., 1.)      # X, Y, Z, phase offset, home X, home Y
    leg2state.reset(1., -1., 0., 0.25, 1., -1.)  # X, Y, Z, phase offset, home X, home Y
    leg3state.reset(-1., -1., 0., 0.5, -1., -1.) # X, Y, Z, phase offset, home X, home Y
    leg4state.reset(-1., 1., 0., 0.75, -1., 1.)  # X, Y, Z, phase offset, home X, home Y

    vx = 1
    vy = 0
    omega = 1

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.autoscale(enable=True, axis='both', tight=None)

    tick = 0
    simtime = 4

    for i in range(int(simtime/macros.TIMESTEP)+1):
        update_leg(leg1state, vx, vy, omega, tick, macros.LIFT_PHASE)
        ax.scatter(leg1state.x,leg1state.y,leg1state.z,c='b')

        update_leg(leg2state, vx, vy, omega, tick, macros.LIFT_PHASE)
        ax.scatter(leg2state.x, leg2state.y, leg2state.z, c='r')

        update_leg(leg3state, vx, vy, omega, tick, macros.LIFT_PHASE)
        ax.scatter(leg3state.x, leg3state.y, leg3state.z, c='g')

        update_leg(leg4state, vx, vy, omega, tick, macros.LIFT_PHASE)
        ax.scatter(leg4state.x, leg4state.y, leg4state.z, c='y')

        tick += macros.TIMESTEP

    plt.show()


#caldoescode()


