import serial
port='/dev/ttyACM0'
baud=115200
constbound=1000
ser=serial.Serial(port, baud, timeout=0)
numdat='notarget'
while True:
    if ser.inWaiting()>0:
        #print(ser.inWaiting())
        datastr=ser.read(ser.inWaiting())
        datastr=datastr.split()
        datastr=datastr[2]
        datastr=str(datastr, 'utf-8')
        datastr=datastr.split(',')
        numdat= [int(i) for i in datastr]
        x=numdat[0]
        #if abs(x)>constbound:
            #constbound=abs(x)
        x=160+(160*x)/constbound
        numdat[0]=x
        x=numdat[1]
        x=130+(130*x)/((260./320.)*constbound)
        numdat[1]=x
        print(numdat)
        
    #else:
        #numdat= [-1500, -1500]
