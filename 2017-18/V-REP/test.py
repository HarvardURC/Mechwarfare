"""
To begin looking for clients, call
simExtRemoteApiStart(19999)
from some threaded script in V-REP.

Python client remote API documentation:
http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm
"""

import vrep, sys
from time import sleep
import hlsockets

# 0-2 are leg 1, 3-5 are leg 2, 6-8 are leg 3, 9-11 are leg4
joints = [
            "Leg1_BodyUpper", "Leg1_UpperMiddle", "Leg1_MiddleLower",
            "Leg2_BodyUpper", "Leg2_UpperMiddle", "Leg2_MiddleLower",
            "Leg3_BodyUpper", "Leg3_UpperMiddle", "Leg3_MiddleLower",
            "Leg4_BodyUpper", "Leg4_UpperMiddle", "Leg4_MiddleLower"
         ]

jds = { joint:None for joint in joints }
positions = { joint:0 for joint in joints }

# default offsets
offsets = {
            "Leg1_BodyUpper"    : 0,
            "Leg1_UpperMiddle"  : 0,
            "Leg1_MiddleLower"  : 0,
            "Leg2_BodyUpper"    : 0,
            "Leg2_UpperMiddle"  : 0,
            "Leg2_MiddleLower"  : 0,
            "Leg3_BodyUpper"    : 0,
            "Leg3_UpperMiddle"  : 0,
            "Leg3_MiddleLower"  : 0,
            "Leg4_BodyUpper"    : 0,
            "Leg4_UpperMiddle"  : 0,
            "Leg4_MiddleLower"  : 0
          }

vrep.simxFinish(-1)     # close any existing connections
cID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if cID != -1:
    print("Connected to remote API server")
else:
    print("Connection failed")
    sys.exit(1)

for joint in joints:
    err, jd = vrep.simxGetObjectHandle(cID, joint, vrep.simx_opmode_oneshot_wait)
    if err != 0:
        print(joint + " couldn't be found")
        sys.exit(1)
    jds[joint] = jd

client = hlsockets.UDSClient(0.03)
client.open(hlsockets.SERVO)
while 1:
    params = client.recv()
    if(params):
        for id, angle in enumerate(params):
            positions[joints[id]] = angle
    for joint in joints:
        vrep.simxSetJointPosition(cID, jds[joint], positions[joint] + offsets[joint], vrep.simx_opmode_oneshot)
client.close()

