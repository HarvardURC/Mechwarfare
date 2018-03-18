import os

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

TORQUE_ENABLE               = 1                             # Value for enabling the torque
TORQUE_DISABLE              = 0                             # Value for disabling the torque

DXL_MOVING_STATUS_THRESHOLD = 10                            # Dynamixel moving status threshold

ESC_ASCII_VALUE             = 0x1b

COMM_SUCCESS                = 0                             # Communication Success result value
COMM_TX_FAIL                = -1001                         # Communication Tx Failed

# will be updated at runtime
IDS = None
PORT_NUM = None


# takes a list of id numbers as a parameter and default offsets (same dimension)
# returns -1 on failure
def init_motors(ids_list, offsets):
    global PORT_NUM, IDS

    IDS = ids_list
    
    PORT_NUM = dynamixel.portHandler(DEVICENAME)

    # initialize PacketHandler structs
    dynamixel.packetHandler()

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
        dxl_comm_result = dynamixel.getLastTxRxResult(PORT_NUM, PROTOCOL_VERSION)
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
        
        dynamixel.write2ByteTxRx(PORT_NUM, PROTOCOL_VERSION, IDS[i], ADDR_MX_GOAL_POSITION, pos_list[i])
        dxl_comm_result = dynamixel.getLastTxRxResult(PORT_NUM, PROTOCOL_VERSION)
        dxl_error = dynamixel.getLastRxPacketError(PORT_NUM, PROTOCOL_VERSION)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
            return -1
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))
            return -1


from time import sleep

err = init_motors([3,4,5, 6,7,8, 9,10,11, 12,13,14], [0,90,90, 0,90,90, 0,90,90, 0,90,90])
err = set_target_positions([300,300,300, 300,300,300, 300,300,300, 300,300,300])
sleep(1)
err = set_target_positions([400,400,400, 400,400,400, 400,400,400, 400,400,400])
sleep(1)
err = set_target_positions([500,500,500, 500,500,500, 500,500,500, 500,500,500])
sleep(1)
err = deinit_motors()
