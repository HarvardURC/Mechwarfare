import math as m
import numpy as np
import ik
import gait
import hlsockets
from time import sleep

# 0-2 are leg 1, 3-5 are leg 2, 6-8 are leg 3, 9-11 are leg4
# 0 -> hip, 1 -> elbow, 2 -> knee
angles = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
claws, body = ik.make_standard_bot()
HEIGHT = 13

# given a list of angles and a time, maintains angle positions for time seconds
def maintain_pos(time, angles):
    for i in range(40 * int(time)):
        client.send(hlsockets.SERVO, angles)
        sleep(.025)

# default position (robot laying on ground, splayed out): stands for time seconds
def reset(time=10):
    angles = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    maintain_pos(time, angles)

# given body, list of claw positions, pitch, and roll, stands at pitch and roll for time seconds
def stand(pitch=0, roll=0, height=8, time=10):
    angles = ik.extract_angles(body, claws, pitch, roll, height)
    maintain_pos(time, angles)

# stands on tippy toes
def tippytoes():
    angles = [0, -90, 0, 0, -90, 0, 0, -90, 0, 0, -90, 0]
    for i in range(20):
        client.send(hlsockets.SERVO, angles)
        sleep(.025)
    reset(1)

# jumps a little bit
def jump():
    angles = [0, -90, -90, 0, -90, -90, 0, -90, -90, 0, -90, -90]
    for i in range(20):
        client.send(hlsockets.SERVO, angles)
        sleep(.025)
    reset(1)

# does the robot boogie for time seconds
def wiggle(time=10):
    for j in range(time):
        for i in range(10):
            client.send(hlsockets.SERVO, ik.extract_angles(body, claws, 20, 0, HEIGHT))
            sleep(.025)
        for i in range(10):
            client.send(hlsockets.SERVO, ik.extract_angles(body, claws, -10, 20, HEIGHT))
            sleep(.025)
        for i in range(10):
            client.send(hlsockets.SERVO, ik.extract_angles(body, claws, 20, 0, HEIGHT))
            sleep(.025)
        for i in range(10):
            client.send(hlsockets.SERVO, ik.extract_angles(body, claws, -10, -20, HEIGHT))
            sleep(.025)

def walk(cycles=10, pitch=0, roll=0, height=HEIGHT):
    # loop through cycles
    for i in range(cycles):
        points = gait.create_points()
        print(len(points), len(points[0]), len(points[1]), len(points[2])) 
        print(len(points[0][0]), len(points[0][1]), len(points[0][2]))
        print(len(points[1][0]), len(points[1][1]), len(points[1][2]))
        print(len(points[2][0]), len(points[2][1]), len(points[2][2]))
        print(len(points[3][0]), len(points[3][1]), len(points[3][2]))
        # loop through timepoints in each cycle
        for j in range(len(points[i][0])):
            cs = []
            heights = []
            # loop through legs
            for k in range(len(points)):
                cs.append(np.array([points[k][0][j], points[k][1][j]]))
                heights.append(points[k][2][j])
            client.send(hlsockets.SERVO, ik.extract_angles(body, cs, pitch, roll, height, heights))


client = hlsockets.UDSClient()
client.open(hlsockets.CONTROLLER)
reset(2)
while True:
    reset(2)
    walk()
    reset()
client.close()


