import numpy as np
import math as m
import copy, macros, objs, ik, helpers
from time import time

def calculate_step(cur, goal, phase, endphase, timestep, stridelength, times={}):
    """Calculate the next step to reach a goal at a certain time"""

    # Timing value
    tv_cs = time()

    # Check if the end phase is very close or past
    if phase > endphase - macros.TOLERANCE:
        # If so, go to the goal right away
        return goal - cur

    times = helpers.dict_timer("GAT.calculate_step", times, time()-tv_cs)    

    # Otherwise, go at the speed that will reach the goal at the target time
    return (goal - cur) * timestep / (stridelength * (endphase - phase))


def update_leg(state, vx, vy, omega, t, lift_phase, timestep, stridelength, raisefrac, raiseh, times={}):
    """Updates the state of a leg at each timestep, given state and robot velocity"""

    # Timing value
    tv_ul = time()

    # The phase of the walking cycle is calculated
    phase = (t + state.phase_offset * stridelength) % stridelength

    # If the leg is being lifted
    if phase < lift_phase:
        state.home_offs[0] = -1 * (-vx + state.yawhomes[1] * omega) * (stridelength * (1-lift_phase) / 2)
        state.home_offs[1] = -1 * (-vy - state.yawhomes[0] * omega) * (stridelength * (1-lift_phase) / 2)

        # Move it horizontally towards the home position
        state.loc[0] += calculate_step(state.loc[0], state.yawhomes[0] + state.home_offs[0], phase, lift_phase, timestep, stridelength, times)
        state.loc[1] += calculate_step(state.loc[1], state.yawhomes[1] + state.home_offs[1], phase, lift_phase, timestep, stridelength, times)

        # If it's being lifted
        if phase < lift_phase * raisefrac:
            # Lift it
            state.loc[2] += calculate_step(state.loc[2], raiseh, phase, lift_phase * raisefrac, timestep, stridelength, times)
        # If it's being lowered,
        elif phase > lift_phase * (1 - raisefrac):
            # Lower it
            state.loc[2] += calculate_step(state.loc[2], 0, phase, lift_phase, timestep, stridelength, times)
    else:
        # Otherwise, move it horizontally based on robot velocity
        state.loc[0] += (-vx + state.loc[1] * omega) * timestep
        state.loc[1] += (-vy - state.loc[0] * omega) * timestep

    times = helpers.dict_timer("GAT.update_leg", times, time()-tv_ul)


def timestep(body, enable, return_home, vx, vy, omega, height, pitch, roll, yaw, t, home_wid, home_len, timestep, 
    stridelength, raisefrac, raiseh, lift_phase, phases, was_still):
    """Updates the states of every leg for a given robot body, given state and robot velocity"""

    # Timing value
    tv_timestep = time()

    timestep = macros.TIMESTEP

    # Update leg states
    for i in range(len(body.legs)):
        body.legs[i].state.phase_offset = phases[i]
        body.legs[i].state.homes[0] = body.legs[i].state.signs[0] * home_len
        body.legs[i].state.homes[1] = body.legs[i].state.signs[1] * home_wid

    # Variables to track change in state
    xys = []
    zs = []

    # Manage yawing
    yc, ys = m.cos(helpers.dtor(yaw)), m.sin(helpers.dtor(yaw))
    yawm = np.matrix([[yc, -ys], [ys, yc]])
    for i in range(len(body.legs)):
        body.legs[i].state.yawhomes = np.squeeze(np.asarray(yawm * body.legs[i].state.homes[np.newaxis].T))

#    yawc, yaws = m.cos(helpers.dtor(yaw)), m.sin(helpers.dtor(yaw))
#    for i in range(len(body.legs)):
#        home_x, home_y = body.legs[i].state.homes[0], body.legs[i].state.homes[1]
#        body.legs[i].state.yawhomes = [home_x * yawc - home_y * yaws, home_x * yaws + home_y * yawc]

    # If walking is enabled and the robot is at the minimum required velocity
    if (enable and ((m.sqrt(vx**2 + vy**2) >= macros.MIN_V) or (abs(omega) >= macros.MIN_OMEGA))):
        # If robot was still immediately before this timestep
        if (was_still):
            t = 0
        was_still = False
        # Update each leg
        for i in range(len(body.legs)):
            update_leg(body.legs[i].state, vx, vy, helpers.dtor(omega), t, lift_phase, timestep, stridelength, raisefrac, raiseh, times)
            xys.append([body.legs[i].state.loc[0], body.legs[i].state.loc[1]])
            zs.append(body.legs[i].state.loc[2])    

    # Else the claws should be static
    else:
        was_still = True
        for i in range(len(body.legs)):
            xys.append(body.legs[i].state.yawhomes)
            zs.append(0)

    # Increment timestep
    t += timestep

    times = helpers.dict_timer("GAT.timestep", times, time()-tv_timestep)

    ret_angles = ik.extract_angles(body, xys, pitch, roll, height, zs, times)

    # Return formatted array of angles
    return(timestep, ret_angles, t, was_still, times)

