# This Demo Turns a Single Servo back and forth between
# 0 and 300 Degrees (max range for DX 117)
from helper import (getch, enable_torque, write_goal, read_pos, disable_torque)
from dynamixel_sdk import *
from shared_constants import *

DXL_ID                      = 15 # Set this to the ID of the servo that we are controlling


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

    # Declare the goal positions
    goal_positions = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]

    index = 0
    while True:
        print("Press any key to continue! (or press ESC to quit!)")
        if getch() == chr(0x1b):
            break

        goal_pos = goal_positions[index]
        # Write goal position to the servo
        write_goal(packetHandler, portHandler, DXL_ID, goal_pos)

        # Execute until error within threshold
        while True:
            # Read present position
            dxl_present_position = read_pos(packetHandler, portHandler, DXL_ID)

            print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID, goal_pos, dxl_present_position))

            if abs(goal_pos - dxl_present_position) < DXL_MOVING_STATUS_THRESHOLD:
                break

        index = 1 - index  # Toggle index between 1 and 0

    disable_torque(packetHandler, portHandler, DXL_ID)

    # close port
    portHandler.closePort()


if __name__ == "__main__":
    main()
