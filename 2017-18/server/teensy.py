# teensy to gait

from hlsockets import UDSClient
from time import sleep
import serial

client = hlsockets.UDSClient()
client.open(hlsockets.TEENSY)

ser = serial.Serial('/dev/cu.usbmodem3013661', 115200, timeout=1)

offset = 1000

while True:
    msg = ser.readline() # wow much data
    msg = [int(i)-1000 for i in msg.split(',')]
    client.send(hlsockets.GAIT, msg)
    # in the future there might be GAIT
    # between TEENSY and SERVO

client.close()
