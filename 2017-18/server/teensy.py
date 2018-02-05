# teensy to gait

from hlsockets import UDSClient
from time import sleep
import serial

client = hlsockets.UDSClient()
client.open(hlsockets.TEENSY)

ser = serial.Serial('/dev/cu.usbmodem3013661', 115200, timeout=1)

while True:
    msg = ser.readline()) # wow much data
    client.send(hlsockets.SERVO, msg)
    # in the future there might be GAIT
    # between TEENSY and SERVO

client.close()
