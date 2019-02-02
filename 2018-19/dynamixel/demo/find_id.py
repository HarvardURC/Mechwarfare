# This script finds the ID of the single Dynamixel Servo connected
from helper import (getch, enable_torque, write_goal, read_pos, disable_torque)
from dynamixel_sdk import *
from shared_constants import *

def main():
    portHandler = PortHandler(DEVICENAME)

    packetHandler = PacketHandler(PROTOCOL_VERSION)

    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate")
        getch()
        quit()

    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate")
        getch()
        quit()

    for DXL_ID in range(0, 254):
        print("try ID: {}".format(DXL_ID))
        dxl_model_number, dxl_comm_result, dxl_error = packetHandler.ping(
            portHandler, DXL_ID)
        if dxl_comm_result == COMM_SUCCESS:
            print("Found ID: {}".format(DXL_ID))
            break

    # close port
    portHandler.closePort()


if __name__ == "__main__":
    main()
