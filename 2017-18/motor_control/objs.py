import math as m
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import collections as mc
import numpy as np
import macros
import helpers


# General object classes
class leg_state:
    def __init__(self, id_num):
        self.x = macros.DEFSTATES[id_num][0]
        self.y = macros.DEFSTATES[id_num][1]
        self.z = macros.DEFSTATES[id_num][2]
        self.phase_offset = macros.DEFSTATES[id_num][3]
        self.home_x = macros.DEFSTATES[id_num][4]
        self.home_y = macros.DEFSTATES[id_num][5]

    def reset(self, x, y, z, phase_offset, home_x, home_y):
        self.x = x
        self.y = y
        self.z = z
        self.phase_offset = phase_offset
        self.home_x = home_x
        self.home_y = home_y

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









































# # TEST CODE

# # leg_data(x, y, z: cartesian offset of hip from body center, gamma: 0 position of hip servo)
# #   printleg
# #     prints leg offset and gamma
# #   graphleg(claw: desired claw location in cylindrical coordinates in leg frame)
# #     outputs graph of leg
# class leg_data:
#     def __init__(self, x, y, z, gamma, trolen=macros.TROLEN, femlen=macros.FEMLEN, tiblen=macros.TIBLEN):
#         self.off = np.array([x, y, z])
#         self.gamma = gamma
#         self.trolen = trolen
#         self.femlen = femlen
#         self.tiblen = tiblen

#     # prints leg offset and gamma
#     def printleg(self):
#         print('  Offset: ', self.off)
#         print('  Gamma: ', self.gamma)

#     # outputs graph of leg with 3 subcomponents:
#     #   projection onto (x, y) plane, projection onto (z, self.gamma) plane, and 3d render
#     def graphleg(self, claw):
#         ll = get_leglines(self, claw)

#         # Plot
#         mpl.rcParams['legend.fontsize'] = 10
#         fig = plt.figure(1)

#         axtop = fig.add_subplot(131)
#         axtop.plot(ll[0][0], ll[0][1], c='g') 
#         axtop.plot(ll[1][0], ll[1][1], c='y') 
#         axtop.plot(ll[2][0], ll[2][1], c='r') 
#         plt.show
#         axside = fig.add_subplot(132)
#         axside.plot(ll[0][0], ll[0][2], c='g') 
#         axside.plot(ll[1][0], ll[1][2], c='y') 
#         axside.plot(ll[2][0], ll[2][2], c='r') 
#         plt.show

#         ax3 = fig.add_subplot(133, projection='3d')
#         ax3.plot(ll[0][0], ll[0][1], ll[0][2], c='g')
#         ax3.plot(ll[1][0], ll[1][1], ll[1][2], c='y')
#         ax3.plot(ll[2][0], ll[2][1], ll[2][2], c='r')
#         plt.show()



# # body_data(legs: list of leg_data objects, side: length of body side, zdist: distance
# #   from elbow to bottom of body)
# #   printbody
# #     prints number of legs, sidelength, and calls printleg for each leg
# #   graphbody(claws: desired claw locations in cylindrical coordinates in leg frames, 
# #       pitch: desired pitch of body, roll: desired roll of body)
# #     outputs graph of body
# class body_data:
#     def __init__(self, legs, side, zdist=macros.ZDIST, trolen=macros.TROLEN, femlen=macros.FEMLEN, tiblen=macros.TIBLEN):
#         self.numlegs = len(legs)
#         self.legs = legs
#         self.side = side
#         self.zdist = zdist
#         self.trolen, self.femlen, self.tiblen = trolen, femlen, tiblen
#         self.hip_wiggle = m.asin((side/2)/(trolen + femlen + tiblen))

#     # prints number of legs, sidelength, and calls printleg for each leg
#     def printbody(self):
#         print("Number of legs: ", self.numlegs)
#         print("Sidelength: ", self.side)
#         for i in range(self.numlegs):
#             print("Leg", i)
#             self.legs[i].printleg()
#             print("\n")

#     # outputs graph of body in 3d space with legs
#     def graphbody(self, claws, pitch, roll, height):
#         print("removed due to dependency issues")
        # print("Pitch: ", pitch)
        # print("Roll: ", roll)
        # newclaws = ik.body_ik(self, claws, pitch, roll, height)
        # cclaws = []
        # for i in range(len(newclaws)):
        #     cclaws.append(helpers.fromcyl(newclaws[i]))
        #     cclaws[i] += self.legs[i].off

        # # Plot
        # mpl.rcParams['legend.fontsize'] = 10
        # fig = plt.figure().gca(projection='3d')
        
        # bl = get_bodylines(self)
        # fig.plot(bl[0][0], bl[0][1], bl[0][2], c='b')
        # fig.plot(bl[1][0], bl[1][1], bl[1][2], c='k')
        # fig.plot(bl[2][0], bl[2][1], bl[2][2], c='k')
        # fig.plot(bl[3][0], bl[3][1], bl[3][2], c='k')
        # for i in range(len(newclaws)):
        #     ll = change_frame(get_leglines(self.legs[i], newclaws[i]), self.legs[i].off)
        #     fig.plot(ll[0][0], ll[0][1], ll[0][2], c='g')
        #     fig.plot(ll[1][0], ll[1][1], ll[1][2], c='y')
        #     fig.plot(ll[2][0], ll[2][1], ll[2][2], c='r')
        # fig.text(cclaws[0][0], cclaws[0][1], cclaws[0][2], "0")
        # fig.text(cclaws[1][0], cclaws[1][1], cclaws[1][2], "1")
        # fig.text(cclaws[2][0], cclaws[2][1], cclaws[2][2], "2")
        # fig.text(cclaws[3][0], cclaws[3][1], cclaws[3][2], "3")
        # plt.xlabel('x')
        # plt.ylabel('y')

        # plt.show()

        # for i in range(len(newclaws)):
        #     print("Leg:", i)
        #     self.legs[i].printleg()
        #     self.legs[i].graphleg(newclaws[i])












# # # # # # # # # # # # # # # # # # # # 
# # # # FUNCTIONS FOR GRAPHING  # # # #
# # # # # # # # # # # # # # # # # # # # 

# # get_bodylines(body: body object)
# #   returns list of lists of lines which outline robot body 
# #   in the form [[x, x], [y, y], [z, z]] for graphing purposes
# def get_bodylines(body):
#     c = body.side/2
#     return [[[c, c], [-c, c], [0, 0]], 
#             [[c, -c], [c, c], [0, 0]], 
#             [[-c, -c], [c, -c], [0, 0]], 
#             [[-c, c], [-c, -c], [0, 0]]]

# # get_leglines(leg: leg_data object, claw: desired claw location in cylindrical coordinates in leg frame)
# #   returns list of lists of lines which outline leg segments
# #   in the form [[x, x], [y, y], [z, z]] for graphing purposes
# def get_leglines(leg, claw):
#     # Get data
#     angles = ik.leg_ik(leg, claw)
#     angles[0] += leg.gamma

#     # Define locations of joints in space; convert to cartesian
#     hipp = np.array([0, 0, 0])
#     elbowp = fromcyl(np.array([angles[0], leg.trolen, 0]))
#     kneep = fromcyl(np.array([angles[0], leg.trolen + leg.femlen * m.cos(dtor(angles[1])), leg.femlen * m.sin(dtor(angles[1]))]))
#     clawp = fromcyl(np.array([angles[0], claw[1], claw[2]]))

#     return [[[hipp[0], elbowp[0]], [hipp[1], elbowp[1]], [hipp[2], elbowp[2]]],
#             [[elbowp[0], kneep[0]], [elbowp[1], kneep[1]], [elbowp[2], kneep[2]]],
#             [[kneep[0], clawp[0]], [kneep[1], clawp[1]], [kneep[2], clawp[2]]]]

# # change_frame(lines: list of lines in graphing format, off: cartesian offset of frame lines are in)
# #   returns lines in non-offset frame
# def change_frame(lines, off):
#     for i in range(len(lines[0])):
#         for j in range(len(lines)):
#             lines[j][i][0] += off[i]
#             lines[j][i][1] += off[i]
#     return lines
