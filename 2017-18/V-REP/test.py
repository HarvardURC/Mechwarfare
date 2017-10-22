"""
To begin looking for clients, call
simExtRemoteApiStart(19999)
from some threaded script in V-REP.

Python client remote API documentation:
http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm
"""

import vrep, sys

vrep.simxFinish(-1)     # close any existing connections
cID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if cID != -1:
    print("Connected to remote API server")
else:
    print("Connection failed")
    sys.exit(1)

err, lm = vrep.simxGetObjectHandle(cID, 'Pioneer_p3dx_leftMotor', vrep.simx_opmode_oneshot_wait)
if err != 0:
    print("'Pioneer_p3dx_leftMotor' couldn't be found")
    sys.exit(1)

err, rm = vrep.simxGetObjectHandle(cID, 'Pioneer_p3dx_rightMotor', vrep.simx_opmode_oneshot_wait)
if err != 0:
    print("'Pioneer_p3dx_rightMotor' couldn't be found")
    sys.exit(1)

while 1:
    vrep.simxSetJointTargetVelocity(cID, lm, 0.5, vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetVelocity(cID, rm, 0.5, vrep.simx_opmode_oneshot)
