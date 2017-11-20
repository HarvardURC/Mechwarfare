# client template

import math as m
import numpy as np
import ik
import hlsockets
from time import sleep

# 0-2 are leg 1, 3-5 are leg 2, 6-8 are leg 3, 9-11 are leg4
# 0 -> hip, 1 -> elbow, 2 -> knee
angles = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
claws, body = ik.make_standard_bot()

# converts a list of angles from degrees to radians
def fix_angles(angles):
    for i in range(len(angles)):
        angles[i] = ik.dtor(angles[i])
    return angles

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
def stand(pitch=0, roll=0, time=10):
    angles = fix_angles(ik.extract_angles(body, claws, pitch, roll))
    maintain_pos(time, angles)

# stands on tippy toes
def tippytoes():
    angles = fix_angles([0, -90, 0, 0, -90, 0, 0, -90, 0, 0, -90, 0])
    for i in range(20):
        client.send(hlsockets.SERVO, angles)
        sleep(.025)
    reset(1)

# jumps a little bit
def jump():
    angles = fix_angles([0, -90, -90, 0, -90, -90, 0, -90, -90, 0, -90, -90])
    for i in range(20):
        client.send(hlsockets.SERVO, angles)
        sleep(.025)
    reset(1)

# does the robot boogie for time seconds
def wiggle(time=10):
    for j in range(time):
        for i in range(10):
            client.send(hlsockets.SERVO, fix_angles(ik.extract_angles(body, claws, 20, 0)))
            sleep(.025)
        for i in range(10):
            client.send(hlsockets.SERVO, fix_angles(ik.extract_angles(body, claws, -10, 20)))
            sleep(.025)
        for i in range(10):
            client.send(hlsockets.SERVO, fix_angles(ik.extract_angles(body, claws, 20, 0)))
            sleep(.025)
        for i in range(10):
            client.send(hlsockets.SERVO, fix_angles(ik.extract_angles(body, claws, -10, -20)))
            sleep(.025)
        

client = hlsockets.UDSClient()
client.open(hlsockets.CONTROLLER)
reset(2)
while True:
    tippytoes()
    jump()
client.close()


