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
def stand(pitch=0, roll=0, height=8, time=10):
    client.send(hlsockets.SERVO, ik.extract_angles(body, claws, pitch, roll, height))
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
        client.send(hlsockets.SERVO, angles)
        sleep(sleeptime)


client = hlsockets.UDSClient()
client.open(hlsockets.CONTROLLER)
reset(2)
while True:
    reset(1)
    walk(1, 0, 20)
    reset(1)
client.close()


