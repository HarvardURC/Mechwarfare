import os
from dynamixel_sdk import (DXL_LOBYTE, DXL_LOWORD, DXL_HIBYTE, DXL_HIWORD)
from shared_constants import *

# OS specifc implementation of getch()
if os.name == "nt":
    import msvcrt

    def getch():
        return msvcrt.getch().decode()
else:
    import sys
    import tty
    import termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


# Enable Dynamixel Torque
def enable_torque(packet_handler, port_handler, dxl_id):
    dxl_comm_result, dxl_error = packet_handler.write1ByteTxRx(port_handler, dxl_id, ADDR_DX_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
        return False
    elif dxl_error != 0:
        print("%s" % packet_handler.getRxPacketError(dxl_error))
        return False
    else:
        print("Dynamixel #{} has been successfully connected".format(dxl_id))
    return True


def write_goal(packet_handler, port_handler, dxl_id, goal_pos):
    dxl_comm_result, dxl_error = packet_handler.write4ByteTxRx(port_handler, dxl_id, ADDR_DX_GOAL_POSITION, goal_pos)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packet_handler.getRxPacketError(dxl_error))

# Read Current Position
def read_pos(packet_handler, port_handler, dxl_id):
    dxl_present_position, dxl_comm_result, dxl_error = packet_handler.read4ByteTxRx(port_handler, dxl_id, ADDR_DX_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
        return None
    elif dxl_error != 0:
        print("%s" % packet_handler.getRxPacketError(dxl_error))
        return None
    return dxl_present_position


# Allocate goal position value into byte array
def byte_array(goal):
    return [DXL_LOBYTE(DXL_LOWORD(goal)),
            DXL_HIBYTE(DXL_LOWORD(goal)),
            DXL_LOBYTE(DXL_HIWORD(goal)),
            DXL_HIBYTE(DXL_HIWORD(goal))]

# Add goal position value to the Syncwrite parameter storage
def add_goal_param(group_sync_write, dxl_id, param_goal):
    dxl_addparam_result = group_sync_write.addParam(dxl_id, param_goal)
    if dxl_addparam_result is not True:
        print("[ID:%03d] groupSyncWrite addparam failed" % dxl_id)
        return False
    return True


# Syncwrite goal position
def sync_write_goal(group_sync_write, packet_handler):
    dxl_comm_result = group_sync_write.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))


def clear_goal_param(group_sync_write):
        group_sync_write.clearParam()


# Disable Torque
def disable_torque(packet_handler, port_handler, dxl_id):
    dxl_comm_result, dxl_error = packet_handler.write1ByteTxRx(port_handler, dxl_id, ADDR_DX_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packet_handler.getRxPacketError(dxl_error))