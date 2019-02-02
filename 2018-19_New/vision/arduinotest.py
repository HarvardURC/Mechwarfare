import serial
import time
#port='/dev/ttyACM0'  #two ports here, port 1 Jevois port 2 arduino
port2='COM3'        # replace here
baud=115200         # baud rate for jevois
constbound=1000     # bounds for image--constbound is jevois struct, x and ybounds are pixel sizes
xbound=320.
ybound=260.
currpos=0           # which target variable is being set: 0: x set, 1: y set, 3: movement completed

#ser=serial.Serial(port, baud, timeout=0)
ser2=serial.Serial(port2, 9600, timeout=0)
dir=True
dir2=True

def spdstep(i, dir3):
    j=i
    tempdir=dir3
    #print(str(j)+ " j")
    if i>=255:
        j-=1
        tempdir=False
    if i<=0:
        j+=1
        tempdir=True
    elif tempdir:
        j+=1
    else:
        j-=1
    return j, tempdir
arr=[15, 0]
loop=0
time.sleep(1)
while loop<10000:
    arr[0], dir=spdstep(arr[0], dir)
    arr[1], dir2=spdstep(arr[1], dir2)
    ser2.write(arr)
    while(ser2.inWaiting()==0):
        pass
    #x=int.from_bytes(ser2.read(2), byteorder="big")
    y=int.from_bytes(ser2.read(), byteorder="big")
    if(-1!=y):
        #print(str(arr[0]) + " arr0")
        #print(str(x) + " x")
        print(str(arr[1]) + " arr1")
        print(str(y) + " y")
    loop+=1
