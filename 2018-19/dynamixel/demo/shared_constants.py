### Connection Specific Constants
# Protocal version
PROTOCOL_VERSION            = 1.0

# USB Connection
BAUDRATE                    = 57600  # Dynamixel default baudrate
DEVICENAME                  = '/dev/tty.usbserial-AI03QDGK' # '/dev/ttyUSB0'  # Check which port is being used on your controller
       # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*

### Servo Specific Constants
# Control table address
ADDR_DX_TORQUE_ENABLE       = 24
ADDR_DX_GOAL_POSITION       = 30
ADDR_DX_PRESENT_POSITION    = 36

# Data Byte Length
LEN_DX_GOAL_POSITION       = 4
LEN_DX_PRESENT_POSITION    = 4

TORQUE_ENABLE               = 1  # Value for enabling the torque
TORQUE_DISABLE              = 0  # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 0  # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 1023  # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 10  # Dynamixel moving status threshold

COMM_SUCCESS                = 0  # Communication Success result value
COMM_TX_FAIL                = -1001  # Communication Tx Failed

ESC_ASCII_VALUE             = 0x1b
