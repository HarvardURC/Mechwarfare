import math as m
import numpy as np
import macros, helpers


# General object classes
class leg_state:
    def __init__(self, id_num):
        self.loc = np.array([macros.DEFSTATES[id_num][0], macros.DEFSTATES[id_num][1], macros.DEFSTATES[id_num][2]])
        self.phase_offset = macros.DEFSTATES[id_num][3]
        self.homes = np.array([macros.DEFSTATES[id_num][4], macros.DEFSTATES[id_num][5]])
        self.yawhomes = np.array([macros.DEFSTATES[id_num][4], macros.DEFSTATES[id_num][5]])
        self.home_offs = np.array([0, 0])
        self.signs = np.array([1, 1])

    def reset(self, x, y, z, phase_offset, home_x, home_y):
        self.loc = np.array([x, y, z])
        self.phase_offset = phase_offset
        self.homes = np.array([home_x, home_y])

class leg_data:
    def __init__(self, id_num, x, y, gamma, trolen=macros.TROLEN, femlen=macros.FEMLEN, tiblen=macros.TIBLEN):
        self.id_num = id_num
        self.off = np.array([x, y, 0])
        self.gamma = gamma
        self.trolen = trolen
        self.femlen = femlen
        self.tiblen = tiblen
        self.state = leg_state(id_num)
        self.state_is_def = "true"


class body_data:
    def __init__(self, legs, side=macros.SIDE, zdist=macros.ZDIST, trolen=macros.TROLEN, femlen=macros.FEMLEN, tiblen=macros.TIBLEN):
        self.numlegs = macros.NUMLEGS
        self.legs = legs
        self.side = side
        self.zdist = zdist
        self.trolen, self.femlen, self.tiblen = trolen, femlen, tiblen
        self.hip_wiggle = m.asin((side/2)/(trolen + femlen + tiblen))

