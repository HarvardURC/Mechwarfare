"""
To begin looking for clients, call
simExtRemoteApiStart(19999)
from some threaded script in V-REP.

Python client remote API documentation:
http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm
"""

import vrep, sys
from time import sleep

joints = {
            "Body_Leg1Upper": None, "Leg1Upper_Leg1Middle": None, "Leg1Middle_Leg1Lower": None,
            "Body_Leg2Upper": None, "Leg2Upper_Leg2Middle": None, "Leg2Middle_Leg2Lower": None,
            "Body_Leg3Upper": None, "Leg3Upper_Leg3Middle": None, "Leg3Middle_Leg3Lower": None,
            "Body_Leg4Upper": None, "Leg4Upper_Leg4Middle": None, "Leg4Middle_Leg4Lower": None
         }

vrep.simxFinish(-1)     # close any existing connections
cID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if cID != -1:
    print("Connected to remote API server")
else:
    print("Connection failed")
    sys.exit(1)

for joint in joints.keys():
    err, jd = vrep.simxGetObjectHandle(cID, joint, vrep.simx_opmode_oneshot_wait)
    if err != 0:
        print(joint + " couldn't be found")
        sys.exit(1)
    joints[joint] = jd

while 1:
    for jd in joints.values():
        vrep.simxSetJointPosition(cID, jd, 0, vrep.simx_opmode_oneshot)

