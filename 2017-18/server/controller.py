import math as m
import numpy as np
import ik
import gait_alg_test as gait_alg
import hlsockets
from time import sleep

# 0-2 are leg 1, 3-5 are leg 2, 6-8 are leg 3, 9-11 are leg4
# 0 -> hip, 1 -> elbow, 2 -> knee
angles = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
claws, body = ik.make_standard_bot()
HEIGHT = 13
t = 0
was_still = True

# default position (robot laying on ground, splayed out): stands for time seconds
def reset(time=10):
    client.send(hlsockets.SERVO, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    sleep(time)

def walk(vx, vy, omega, height=12, pitch=0, roll=0, yaw=0, time=10):
    t = 0
    while (t < time):
        sleeptime, angles = gait_alg.timestep(body, vx, vy, omega, height, pitch, roll, yaw, t)
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

def quick_fix_angles(angles):
    for i in range(len(angles)):
        if (i % 3 == 1):
            angles[i] = angles[i]*-1
    return angles

client = hlsockets.UDSClient()
client.open(hlsockets.CONTROLLER)
reset(2)
while True:
    vx = 0
    vy = 0
    omega = 5 * m.sin(.2 * t)
    height = 8
    pitch = 0
    roll = 0
    yaw = 0
    home_wid = 9
    home_len = 9

    if (t < 4):
        vx = 6
    elif (t < 8):
        vx = 0
    else:
        vx = 6

    sleeptime, angles, t, was_still = gait_alg.timestep(body, vx, vy, omega, height, pitch, roll, yaw, t, home_wid, home_len, was_still)
    if (len(angles) == 12):
        print(t)
        print("\n")
        client.send(hlsockets.SERVO, quick_fix_angles(quick_fix_order(angles)))
    sleep(sleeptime)
client.close()



