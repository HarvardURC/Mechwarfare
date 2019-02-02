# This Demo Turns a single servo to a specific position
from helper import (getch, enable_torque, write_goal, read_pos, disable_torque)
from dynamixel_sdk import *
from shared_constants import *

DXL_ID                      = 5  # Set this to the ID of the servo that we are controlling


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

    # Enable Dynamixel Torque
    if not enable_torque(packetHandler, portHandler, DXL_ID):
        quit()

    goal_pos = 405  # Make sure this pos/angle does not destroy anything
    write_goal(packetHandler, portHandler, DXL_ID, goal_pos)
    while True:
        # Read present position
        dxl_present_position = read_pos(packetHandler, portHandler, DXL_ID)

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (
            DXL_ID, goal_pos, dxl_present_position))

        if abs(goal_pos - dxl_present_position) < DXL_MOVING_STATUS_THRESHOLD:
            break

    input("Press Enter to disable ")

    disable_torque(packetHandler, portHandler, DXL_ID)

    # close port
    portHandler.closePort()


if __name__ == "__main__":
    main()
