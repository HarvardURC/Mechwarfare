# This Demo Turns 3 Servos back and forth independently
# Either daisy-chained or separately plugged
from helper import (getch, enable_torque, add_goal_param, sync_write_goal,
                    clear_goal_param, read_pos, byte_array, disable_torque)
from dynamixel_sdk import *
from shared_constants import *


DXL_ID1                     = 0 # First Servo ID
DXL_ID2                     = 1 # Second Servo ID
DXL_ID3                     = 2 # Third Servo ID


def main():
    portHandler = PortHandler(DEVICENAME)

    packetHandler = PacketHandler(PROTOCOL_VERSION)

    # Initialize GroupSyncWrite instance
    groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, ADDR_DX_GOAL_POSITION, LEN_DX_GOAL_POSITION)

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

    success1 = enable_torque(packetHandler, portHandler, DXL_ID1)
    success2 = enable_torque(packetHandler, portHandler, DXL_ID2)
    success3 = enable_torque(packetHandler, portHandler, DXL_ID3)
    if not (success1 and success2 and success3):
        quit()

    goal_positions = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]
    index = 0
    while True:
        print("Press any key to continue! (or press ESC to quit!)")
        if getch() == chr(0x1b):
            break

        # Allocate goal position value into byte array
        goal_pos1 = goal_positions[index]
        param_goal1 = byte_array(goal_pos1)
        goal_pos2 = goal_positions[index] // 2 # Half range
        param_goal2 = byte_array(goal_pos2)
        goal_pos3 = goal_positions[index] // 3 # One thirds range
        param_goal3 = byte_array(goal_pos3)

        # Add goals to group sync write
        add_goal_param(groupSyncWrite, DXL_ID1, param_goal1)
        add_goal_param(groupSyncWrite, DXL_ID2, param_goal2)
        add_goal_param(groupSyncWrite, DXL_ID3, param_goal3)
        sync_write_goal(groupSyncWrite, packetHandler)
        clear_goal_param(groupSyncWrite)


        # Execute until error within threshold
        while True:
            # Read present position
            dxl_present_pos1 = read_pos(packetHandler, portHandler, DXL_ID1)
            dxl_present_pos2 = read_pos(packetHandler, portHandler, DXL_ID2)
            dxl_present_pos3 = read_pos(packetHandler, portHandler, DXL_ID3)

            print("[ID:%03d] GoalPos:%03d  PresPos:%03d\n"
                  "[ID:%03d] GoalPos:%03d  PresPos:%03d\n"
                  "[ID:%03d] GoalPos:%03d  PresPos:%03d\n"
                  % (DXL_ID1, goal_pos1, dxl_present_pos1,
                        DXL_ID2, goal_pos2, dxl_present_pos2,
                        DXL_ID2, goal_pos3, dxl_present_pos3))

            if abs(goal_pos1 - dxl_present_pos1) < DXL_MOVING_STATUS_THRESHOLD and \
               abs(goal_pos2 - dxl_present_pos2) < DXL_MOVING_STATUS_THRESHOLD and \
               abs(goal_pos3 - dxl_present_pos3) < DXL_MOVING_STATUS_THRESHOLD:
                break

        index = 1 - index # Toggle index between 1 and 0

    disable_torque(packetHandler, portHandler, DXL_ID1)
    disable_torque(packetHandler, portHandler, DXL_ID2)
    disable_torque(packetHandler, portHandler, DXL_ID3)

    # Close Port
    portHandler.closePort()

if __name__ == "__main__":
    main()