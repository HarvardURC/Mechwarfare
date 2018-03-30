import os
import ik
import gait_alg_test
import ctypes
from math import sin,cos
from time import sleep, time

current_state = dict()

# begin asynchronous bullshit
from flask import Flask, request, render_template
import json
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("slidey.html")

@app.route('/handler', methods=['POST'])
def slidey():
    current_state = json.loads(request.data)
    return""

app.run()
# end asynchronous bullshit

# random setup stuff
if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

os.sys.path.append('../dynamixel_functions_py')             # Path setting

import dynamixel_functions as dynamixel                     # Uses Dynamixel SDK library

DEVICENAME          = "/dev/ttyUSB0".encode('utf-8')
BAUDRATE            = 57600
PROTOCOL_VERSION    = 1

ADDR_MX_TORQUE_ENABLE       = 24                            # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION       = 30
ADDR_MX_PRESENT_POSITION    = 36

LEN_MX_GOAL_POSITION        = 2

TORQUE_ENABLE               = 1                             # Value for enabling the torque
TORQUE_DISABLE              = 0                             # Value for disabling the torque

DXL_MOVING_STATUS_THRESHOLD = 10                            # Dynamixel moving status threshold

ESC_ASCII_VALUE             = 0x1b

COMM_SUCCESS                = 0                             # Communication Success result value
COMM_TX_FAIL                = -1001                         # Communication Tx Failed

# will be updated at runtime
IDS = None
PORT_NUM = None
GROUP_NUM = None

# home position of the servos
HOME = 512


# takes a list of id numbers as a parameter and default offsets (same dimension)
# returns -1 on failure
def init_motors(ids_list, offsets):
    global PORT_NUM, GROUP_NUM, IDS

    IDS = ids_list
    
    PORT_NUM = dynamixel.portHandler(DEVICENAME)
    print(PORT_NUM)
    # initialize PacketHandler structs
    dynamixel.packetHandler()
    
    GROUP_NUM = dynamixel.groupSyncWrite(PORT_NUM, PROTOCOL_VERSION, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION)

    # open port
    if not dynamixel.openPort(PORT_NUM):
        print("Failed to open port!")
        return -1

    # set port baudrate
    if not dynamixel.setBaudRate(PORT_NUM, BAUDRATE):
        print("Failed to change the baudrate!")
        return

    # enable dynamixel torque

    for DXL_ID in IDS:
        dynamixel.write1ByteTxRx(PORT_NUM, PROTOCOL_VERSION, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(PORT_NUM, PROTOCOL_VERSION)
        dxl_error = dynamixel.getLastRxPacketError(PORT_NUM, PROTOCOL_VERSION)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
            return -1
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))
            return -1


# returns -1 on failure (?)
def deinit_motors():
    # disable dynamixel torque

    for DXL_ID in IDS:
        dynamixel.write1ByteTxRx(PORT_NUM, PROTOCOL_VERSION, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
        dxl_comm_result = dynamixel.getTxRxResult(PORT_NUM, PROTOCOL_VERSION)
        dxl_error = dynamixel.getLastRxPacketError(PORT_NUM, PROTOCOL_VERSION)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
            return -1
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))
            return -1

    # close port
    dynamixel.closePort(PORT_NUM)


# takes a list of target positions
# - pos_list must have the same dimension as ids_list from init_motors()
# returns -1 on failure and prints error
def set_target_positions(pos_list):

    if(len(pos_list) != len(IDS)):
        print("pos_list doesn't have the same dimension as ids_list")
        return -1

    for i in range(len(pos_list)):
        # write goal position
        
        dxl_addparam_result = ctypes.c_ubyte(dynamixel.groupSyncWriteAddParam(GROUP_NUM, IDS[i], pos_list[i] + HOME, LEN_MX_GOAL_POSITION)).value
        if dxl_addparam_result != 1:
            print(dx1_addparam_result)
        
        """dynamixel.write2ByteTxRx(PORT_NUM, PROTOCOL_VERSION, IDS[i], ADDR_MX_GOAL_POSITION, pos_list[i] + HOME)
        dxl_comm_result = dynamixel.getLastTxRxResult(PORT_NUM, PROTOCOL_VERSION)
        dxl_error = dynamixel.getLastRxPacketError(PORT_NUM, PROTOCOL_VERSION)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
            return -1
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))
            return -1"""

    dynamixel.groupSyncWriteTxPacket(GROUP_NUM)
    """if dynamixel.getLastTxRxResult(PORT_NUM, PROTOCOL_VERSION) != COMM_SUCCESS:
        dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(PORT_NUM, PROTOCOL_VERSION))"""

    dynamixel.groupSyncWriteClearParam(GROUP_NUM)

def deg_to_dyn(angles):
    for i in range(len(angles)):
        angles[i] *= 1/.29
        angles[i] = int(angles[i])
    return(angles)

def walk(vx, vy, omega, time=10):
    t = 0
    while (t < time):
        sleeptime, angles = gait_alg.timestep(body, vx, vy, omega, t)
        t += sleeptime
        err = set_target_positions(deg_to_dyn(angles))
        print(angles)
        sleep(sleeptime)


err = init_motors([3,4,5, 6,7,8, 9,10,11, 12,13,14], [512]*12) 
print("initiated motors")
claws, body = ik.make_standard_bot()
angles = ik.extract_angles(body, claws, 0, 0, 12)
angles = deg_to_dyn(angles)
t = 0
while(1):
    # read state
    enable = current_state[enable]
    vx = current_state[vx]
    vy = current_state[vy]
    omega = current_state[omega]
    height = current_state[height]
    pitch = current_state[pitch]
    roll = current_state[roll]
    home_wid = current_state[home_width]
    home_len = current_state[home_length]
    timestep = current_state[timestep]
    stridelength = current_state[stridelength]
    raisefrac = current_state[raisefrac]
    raiseh = current_state[raiseh]
    lift_phase = current_state[lift_phase]
    phase0 = current_state[phase0]
    phase1 = current_state[phase1]
    phase2 = current_state[phase2]
    phase3 = current_state[phase3]
    return_home = current_state[return_home]


#    enable = 1
#    vx = 0
#    vy = 0
#    omega = 0
#    height = 12
#    pitch = 0
#    roll = 0
#    home_wid = 9
#    home_len = 9
#    timestep = .02
#    stridelength = 1
#    raisefrac = .5
#    raiseh = 2
#    lift_phase = .25
#    phase0 = 0
#    phase1 = .5
#    phase2 = 0
#    phase3 = .5
#    return_home = 0


    # call timestep function
    sleeptime, angles = gait_alg_test.timestep(body, enable, return_home, vx, vy, omega, 
        height, pitch, roll, t, home_wid, home_len, timestep, stridelength, raisefrac, 
        raiseh, lift_phase, [phase0, phase1, phase2, phase3])

    # update servos accordingly: error check is that when given impossible values IK returns array of angles of incorrect length
    if (enable and len(angles) == 12):
        err = set_target_positions(deg_to_dyn(angles))
        t += sleeptime
    sleep(sleeptime)
