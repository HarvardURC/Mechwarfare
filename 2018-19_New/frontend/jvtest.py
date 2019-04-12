import serial

# Serial port from the JeVois
try:
    serJ = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
except:
    serJ = serial.Serial('/dev/ttyACM3',115200, timeout=1)

while(True):
    msgStable = serJ.readline().decode('utf-8')
    if len(msgStable)>1:
        msgStable = [int(i) for i in msgStable.split(' ')[2:4]]
        print("Message JeVois:", msgStable)