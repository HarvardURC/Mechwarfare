import math as m
import numpy as np
import ik
import gait_alg
import hlsockets
from time import sleep

# 0-2 are leg 1, 3-5 are leg 2, 6-8 are leg 3, 9-11 are leg4
# 0 -> hip, 1 -> elbow, 2 -> knee
angles = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
claws, body = ik.make_standard_bot()
HEIGHT = 13

# default position (robot laying on ground, splayed out): stands for time seconds
def reset(time=10):
    client.send(hlsockets.SERVO, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    sleep(time)

# given body, list of claw positions, pitch, and roll, stands at pitch and roll for time seconds
def stand(pitch=0, roll=0, height=12, time=10):
    angles = ik.extract_angles(body, claws, pitch, roll, height)
    client.send(hlsockets.SERVO, angles)
    sleep(time)

# stands on tippy toes
def tippytoes():
    angles = [0, -90, 0, 0, -90, 0, 0, -90, 0, 0, -90, 0]
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

def walk(vx, vy, omega, time=10):
    t = 0
    while (t < time):
        sleeptime, angles = gait_alg.timestep(body, vx, vy, omega, t)
        t += sleeptime
        client.send(hlsockets.SERVO, quick_fix_order(angles))
        sleep(sleeptime)

def test_leg_order():
    angles = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(4):
        ctr = 0
        angles[i * 3] = 10
        while (ctr < 6):
            client.send(hlsockets.SERVO, angles)
            angles[i * 3] = angles[i * 3] * -1
            sleep(.1)
            ctr = ctr + 1
        angles[i * 3] = 0

def quick_fix_order(angles):
    return(angles[3:] + angles[:3])


client = hlsockets.UDSClient()
client.open(hlsockets.CONTROLLER)
reset(2)
while True:
#    for i in range(8):
#        stand(height=i, time=.5)
    walk(0,0,15)
client.close()
