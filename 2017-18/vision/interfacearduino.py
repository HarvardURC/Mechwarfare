import serial
port='/dev/ttyACM0'  #two ports here, port 1 Jevois port 2 arduino
port2='/dev/ttyACM1' #replace here
baud=115200 #baud rate for jevois
constbound=1000  #bounds for image--constbound is jevois struct, x and ybounds are pixel sizes
xbound=320.
ybound=260.
currpos=0 #which target variable is being set: 0: x set, 1: y set, 3: movement completed
ser=serial.Serial(port, baud, timeout=0)
ser2=serial.Serial(port2, 9600, timeout=0)
numdat='notarget' #array of coordinates
while True:
    numdat = 'notarget' #reset to no target
    if ser.inWaiting()>0:
        #print(ser.inWaiting())
        datastr=ser.read(ser.inWaiting())  #read and process Jevois target data
        datastr=datastr.split()
        datastr=datastr[2:4]
        numdat= [int(float(i.decode('utf-8'))) for i in datastr]  #convert into bytes to send to arduino
        x=numdat[0]
        #if abs(x)>constbound:
            #constbound=abs(x)
        x=160+(160*x)/constbound
        x=int(x*255/xbound)
        numdat[0]=x
        x=numdat[1]
        x=130+(130*x)/((xbound/ybound)*constbound)
        x=int(x*255/ybound)
        numdat[1]=x
        print(numdat)
        if numdat!='notarget':
            #ser2.write(numdat)  #actually send the bytes to the arduino then wait after each for a receipt notification
            #while(ser2.inWaiting())==0:
            #    pass
            #ser.reset_input_buffer() #flush all data accumulated while movement was happening to avoid contamination
            ser2.write(numdat[0])  #actually send the bytes to the arduino then wait after each for a receipt notification
            #while(ser2.inWaiting())==0:
            #    pass
            #currpos=int(ser2.read(ser.inWaiting()))
            ser2.write(numdat[1])
            while (ser2.inWaiting()) == 0:
                pass
                '''while (ser2.inWaiting()) == 0:
                    pass
                currpos = int(ser2.read(ser.inWaiting()))'''
            ser.reset_input_buffer() #flush all data accumulated while movement was happening to avoid contamination
            ser2.reset_input_buffer()
            ser2.reset_output_buffer()

    #else:
        #numdat= [-1500, -1500]
