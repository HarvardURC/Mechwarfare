from flask import Flask, request, render_template
import json
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
from drivers_test import init_robot, update_robot
import serial
import macros
from time import time, sleep
import helpers

# Global variable to keep track of the state of the robot
state = {
    "enable":True,
    "gohome":False,
    "vx":0.,
    "pan":0.,
    "tilt":-45., #this was previously -30 for manual control
    "vy":0.,
    "vz":0.,
    "omega":0.,
    "height":macros.DEFAULT_HEIGHT,
    "pitch":macros.DEFAULT_PITCH,
    "roll":macros.DEFAULT_ROLL,
    "yaw":macros.DEFAULT_YAW,
    "homewidth":12.0,
    "homelength":9.0,
    "timestep":macros.TIMESTEP,
    "teensytime":0.01,
    "stridelength":macros.STRIDELENGTH,
    "raisefrac":macros.RAISEFRAC,
    "raiseh":macros.RAISEH,
    "liftphase":macros.LIFT_PHASE,
    "phasefl":macros.phases[0],
    "phasebl":macros.phases[1],
    "phasebr":macros.phases[2],
    "phasefr":macros.phases[3],
    "useradio":True,
    "usestable":False
}
manual_tilt=False

# Initiate robot
body = init_robot()

# Serial port from the teensy

try:
    ser = serial.Serial('/dev/ttyACM0', 38400, timeout=1) # 38400 opens serial port to communicate with teensy
except:
    print("serial failed")
    ser = serial.Serial('/dev/ttyACM2', 38400, timeout=1)
    
## Serial port from the JeVois
try:
    serJ = serial.Serial('/dev/ttyACM1', 115200, timeout=1)
except:
    serJ = serial.Serial('/dev/ttyACM3',115200, timeout=1)

# Offset average for values from teensy
OFFSET = (990+2014)/2
CONTROLLER_RANGE = (2014-990)/2

def scale(num, max):
    '''
     Takes:
         num: controller input number
         max: max value of output
     Returns:
         controller input scaled between 0 and max
    '''
    return max * float(num - OFFSET) / float(CONTROLLER_RANGE)

def update_robot_loop():
    '''Update robot if 'enable' is toggled on
    '''
    global state
    if(state["enable"]):
        update_robot(body, state, state["timestep"])


def read_message_loop():
    '''Read message from teensy, decode and scale inputs and update the state
    '''
    global state
    if (bool(state["useradio"])):
#        print("In useradio")
        ser.write("a\n".encode()) # Need to send message to read message from teensy (Don't know why, but worthwhile to find out)
#            print("wrote")
#        sleep(0.001)
        if (ser.in_waiting > 0):
#                print("can serial")
            msg = ser.readline().decode('utf-8')
#                print(msg)
            msg = msg[:-2]
#            print(msg)
            msg = [int(i) for i in msg.split(',')]
#            print(msg)
            state["vx"] = scale(msg[3], macros.V_MAX)          # forward/backward trans
            #state["omega"] = scale(msg[4], macros.OMEGA_MAX) 
            state["omega"] = scale(1500, macros.OMEGA_MAX)   # stationary rotate
            # msg[4] # fire
            state["vy"] = scale(msg[6], macros.V_MAX)          # left/right trans
            #state["pitch"] = scale(msg[7], macros.PITCH_BOUND) #wire pulled out
            state["pitch"] = scale(1500, macros.OMEGA_MAX)
            state["roll"] = 0 #scale(msg[7], macros.ROLL_BOUND)
            state["yaw"] = scale(msg[5], macros.YAW_BOUND)
            
            if manual_tilt: # Manual Control
                if (msg[2] > 1600 and state["pan"] < macros.PAN_BOUND): 
                    state["pan"] = float(state["pan"] + 2)
                elif (msg[2] < 1400 and state["pan"] > -macros.PAN_BOUND): 
                    state["pan"] = float(state["pan"] - 2)
                if (msg[1] > 1600 and state["tilt"] < macros.TILT_BOUND_UPPER):
                    state["tilt"] = float(state["tilt"] + 2)
                elif (msg[1] < 1400 and state["tilt"] > macros.TILT_BOUND_LOWER):
                    state["tilt"] = float(state["tilt"] - 2)
            # Automatic Control using JeVois
            # Parse the JeVois line
#        print(serJ.in_waiting)
        if not manual_tilt and serJ.in_waiting > 0:
#            print("in_waiting")
            msgStable = serJ.readline().decode('utf-8')
            msgStable = [int(i) for i in msgStable[4:].split(' ')]
            print(msgStable)
            # Track marker                                                                                                                                                                                                                                 
            if(msgStable[1] > 5):
                state["pan"] = float(state["pan"] + 2)
            elif(msgStable[1] < -5 and msg):
                state["pan"] = float(state["pan"] - 2)
            if (msgStable[2] < -50):
                state["tilt"] = float(state["tilt"] + 0.1)
                print("tilt up")
            elif (msgStable[2] > 50):
                state["tilt"] = float(state["tilt"] - 0.1)
                print("tilt down")

def start_server():
    global app
    app.run()

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("slidey.html")

@app.route('/handler', methods=['POST'])
def slidey():
    global state
    state = json.loads(request.data.decode('utf-8'))
    return ""                                                                                                                                                                                                                                                

# Run update robot and read message at the same time
sched = BackgroundScheduler()
sched.add_job(update_robot_loop, 'interval', seconds=state["timestep"])
sched.add_job(read_message_loop, 'interval', seconds=state["teensytime"])                                                            
sched.start()

start_server() # This was giving error


                                                                              