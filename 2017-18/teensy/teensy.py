import serial
ser = serial.Serial('/dev/cu.usbmodem3013661', 115200, timeout=1)

print(ser.readline()) # wow much data
