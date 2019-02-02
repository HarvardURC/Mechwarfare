# This script reads the current angle of Dynamixel Servo
from helper import (getch, enable_torque, write_goal, read_pos, disable_torque)
from dynamixel_sdk import *
from shared_constants import *

DXL_ID                      = 5 # Set this to the ID of the servo that we are controlling


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

    dxl_present_position = read_pos(packetHandler, portHandler, DXL_ID)
    print("current pos: {}".format(dxl_present_position))

    # close port
    portHandler.closePort()


if __name__ == "__main__":
    main()
