import math as m
import numpy as np
import ik, macros, hlsockets, helpers
import gait_alg_test as gait_alg
from time import sleep, time

# 0-2 are leg 1, 3-5 are leg 2, 6-8 are leg 3, 9-11 are leg4
# 0 -> hip, 1 -> elbow, 2 -> knee
angles = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
claws, body = ik.make_standard_bot()
HEIGHT = 13
t = 0
times = {}
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

def check_angles(angles):
    for i in range(len(angles)):
        # if it's an hip
        if (i % 3 == 0):
            if (angles[i] < macros.HIP_MIN):
                print("a")
                angles[i] = macros.HIP_MIN
            elif (angles[i] > macros.HIP_MAX):
                angles[i] = macros.HIP_MAX
                print("b")
        # if it's a knee
        elif (i % 3 == 1):
            if (angles[i] < macros.KNEE_MIN):
                print("c")
                angles[i] = macros.KNEE_MIN
            elif (angles[i] > macros.KNEE_MAX):
                angles[i] = macros.KNEE_MAX
                print("d")
        # if it's an elbow
        else:
            if (angles[i] < macros.ELB_MIN):
                angles[i] = macros.ELB_MIN
                print("e")
            elif (angles[i] > macros.ELB_MAX):
                angles[i] = macros.ELB_MAX
                print("f")
    return angles

ctr = 1
num_iters = 100

client = hlsockets.UDSClient()
client.open(hlsockets.CONTROLLER)
while True:

    tv_update_robot = time()

    vx = 0
    vy = 0
    omega = 0
    height = 8
    pitch = 0
    roll = 0
    yaw = 20 * m.sin(t)
    home_wid = 9
    home_len = 9

    sleeptime, angles, t, was_still, times = gait_alg.timestep(body, vx, vy, omega, height, pitch, roll, yaw, t, home_wid, home_len, was_still, times)

    times = helpers.dict_timer("Cont.update_robot", times, time()-tv_update_robot)
    
    if (len(angles) == 12):
        tv_servosend = time()
        client.send(hlsockets.SERVO, quick_fix_angles(angles))
        times = helpers.dict_timer("Cont.servosend", times, time()-tv_servosend)

    sleep(sleeptime)

    # if (ctr > num_iters):
    #     ctr = 0
    #     for k in times.keys():
    #         print(k, "time: ", times[k]/num_iters)
    #         times[k]=0
    #     print("\n")

    ctr += 1

client.close()



