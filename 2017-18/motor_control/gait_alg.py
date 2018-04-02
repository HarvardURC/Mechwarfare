import numpy as np
import math as m
import copy
import macros
import objs
import ik
import helpers

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
        state.home_off_x = -1 * (-vx + state.yawhomes[1] * omega) * (macros.STRIDELENGTH * (1-lift_phase) / 2)
        state.home_off_y = -1 * (-vy - state.yawhomes[0] * omega) * (macros.STRIDELENGTH * (1-lift_phase) / 2)

        # Move it horizontally towards the home position
        state.x += calculate_step(state.x, state.yawhomes[0] + state.home_off_x, phase, lift_phase)
        state.y += calculate_step(state.y, state.yawhomes[1] + state.home_off_y, phase, lift_phase)

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



def timestep(body, vx, vy, omega, t, lift_phase=macros.LIFT_PHASE, pitch=macros.DEFAULT_PITCH, 
        roll=macros.DEFAULT_ROLL, height=macros.DEFAULT_HEIGHT, yaw=macros.DEFAULT_YAW):
    """Updates the states of every leg for a given robot body, given state and robot velocity"""

    xys = []
    zs = []
    yawc, yaws = m.cos(helpers.dtor(yaw)), m.sin(helpers.dtor(yaw))
    yawrot = [[yawc, -yaws], [yaws, yawc]]
    for i in range(len(body.legs)):
        body.legs[i].state.yawhomes = yawrot * [body.legs[i].state.home_x, body.legs[i].state.home_y]

    # if the robot should be stepping
    if ((m.sqrt(vx**2 + vy**2) > macros.MIN_V) or (omega > macros.MIN_OMEGA)):
        # Add to variables
        for i in range(len(body.legs)):
            update_leg(body.legs[i].state, vx, vy, helpers.dtor(omega), t, lift_phase)
            xys.append([body.legs[i].state.x, body.legs[i].state.y])
            zs.append(body.legs[i].state.z)

    # else, if the claws should be static
    else:
        for i in range(len(body.legs)):
            xys.append(body.legs[i].state.yawhomes)
            zs.append(0)

    t += macros.TIMESTEP

    # Return formatted array of angles
    return(macros.TIMESTEP, ik.extract_angles(body, xys, pitch, roll, height, zs))


