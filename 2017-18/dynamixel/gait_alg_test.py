import numpy as np
import math as m
import copy
import macros
import objs
import ik
import helpers


def calculate_step(cur, goal, phase, endphase, timestep, stridelength):
    """Calculate the next step to reach a goal at a certain time"""

    # Check if the end phase is very close or past
    if phase > endphase - macros.TOLERANCE:
        # If so, go to the goal right away
        return goal - cur
    # Otherwise, go at the speed that will reach the goal at the target time
    return (goal - cur) * timestep / (stridelength * (endphase - phase))


def update_leg(state, vx, vy, omega, t, lift_phase, timestep, stridelength, raisefrac, raiseh):
    """Updates the state of a leg at each timestep, given state and robot velocity"""

    # The phase of the walking cycle is calculated
    phase = (t + state.phase_offset * stridelength) % stridelength

    # If the leg is being lifted
    if phase < lift_phase:
        state.home_off_x = -1 * (-vx + state.home_y * omega) * (stridelength * (1-lift_phase) / 2)
        state.home_off_y = -1 * (-vy - state.home_x * omega) * (stridelength * (1-lift_phase) / 2)

        # Move it horizontally towards the home position
        state.x += calculate_step(state.x, state.home_x + state.home_off_x, phase, lift_phase, timestep, stridelength)
        state.y += calculate_step(state.y, state.home_y + state.home_off_y, phase, lift_phase, timestep, stridelength)

        # If it's being lifted
        if phase < lift_phase * raisefrac:
            # Lift it
            state.z += calculate_step(state.z, raiseh, phase, lift_phase * raisefrac, timestep, stridelength)
        # If it's being lowered,
        elif phase > lift_phase * (1 - raisefrac):
            # Lower it
            state.z += calculate_step(state.z, 0, phase, lift_phase, timestep, stridelength)
    else:
        # Otherwise, move it horizontally based on robot velocity
        state.x += (-vx + state.y * omega) * timestep
        state.y += (-vy - state.x * omega) * timestep



def timestep(body, enable, return_home, vx, vy, omega, height, pitch, roll, yaw, t, home_wid, home_len, timestep, 
    stridelength, raisefrac, raiseh, lift_phase, phases):
    """Updates the states of every leg for a given robot body, given state and robot velocity"""

    # Update leg states
    for i in range(len(body.legs)):
        body.legs[i].state.phase_offset = phases[i]
        body.legs[i].state.home_x = body.legs[i].state.xsign * home_len
        body.legs[i].state.home_y = body.legs[i].state.ysign * home_wid

    # Variables to track change in state
    xys = []
    zs = []
    yawc, yaws = m.cos(helpers.dtor(yaw)), m.sin(helpers.dtor(yaw))
    yawrot = [[yawc, -yaws], [yaws, yawc]]
    for i in range(len(body.legs)):
        body.legs[i].state.yawhomes = yawrot * [body.legs[i].state.home_x, body.legs[i].state.home_y]

    # If walking is enabled and the robot is at the minimum required velocity
    if (enable and ((m.sqrt(vx**2 + vy**2) > macros.MIN_V) or (omega > macros.MIN_OMEGA))):
        # Update each leg
        for i in range(len(body.legs)):
            update_leg(body.legs[i].state, vx, vy, helpers.dtor(omega), t, lift_phase, timestep, stridelength, raisefrac, raiseh)
            xys.append([body.legs[i].state.x, body.legs[i].state.y])
            zs.append(body.legs[i].state.z)    

    # Else the claws should be static
    else:
        for i in range(len(body.legs)):
            xys.append(body.legs[i].state.yawhomes)
            zs.append(0)

    # pretty sure this line is unnecessary; should be handled on the other side of the function call
    t += macros.TIMESTEP

    # Return formatted array of angles
    return(macros.TIMESTEP, ik.extract_angles(body, xys, pitch, roll, height, zs))

