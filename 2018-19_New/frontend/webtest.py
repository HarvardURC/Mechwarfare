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
    "pan" : 0.,
    "tilt" : 0., 
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
    "stridelength":macros.STRIDELENGTH,
    "raisefrac":macros.RAISEFRAC,
    "raiseh":macros.RAISEH,
    "liftphase":macros.LIFT_PHASE,
    "phasefl":macros.phases[0],
    "phasebl":macros.phases[1],
    "phasebr":macros.phases[2],
    "phasefr":macros.phases[3],
    "useradio": True,
    "usestable" : False
}

body = init_robot()

try:
    ser = serial.Serial('/dev/ttyACM0', 38400, timeout=1) # opens serial port to communicate with teensy
except:
    print("except")
    ser = serial.Serial('/dev/ttyACM1', 38400, timeout=1)
    
#try:
#    serJ = serial.Serial('/dev/tty/ACM2', 38400, timeout=1)
#except:
#    serJ = serial.Serial('/dev/tty/ACM3',38400, timeout=1)

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
    global state
    if state["enable"]:
        #tv_fl = time()
#        print("Update Robot")
        update_robot(body, state, state["timestep"])
        #print("aaaaaa: ",time()-tv_fl)
        #print("vx: ", state["vx"])
        #print("vy: ", state["vy"])
        #print("omega: ", state["omega"])
        #print("pitch: ", state["pitch"])
        #print("roll: ", state["roll"])
        #print("yaw: ", state["yaw"])
        #print("\n\n")

def read_message_loop():
    global state
#    print("Loop is running")
    if (bool(state["useradio"])):
#        print("Inside of state")
        ser.write("a\n".encode())
        #sleep(0.001)
        if (ser.in_waiting > 0):
            msg = ser.readline().decode('utf-8')
            #msgStable = serJ.readline().decode('utf-8')
            #msgStable = [int(i) for i in msgStable.split(',')]
#            print("Inside of teensy loop")
#            print(msg)
            msg = msg[:-2]
            msg = [int(i) for i in msg.split(',')]
#            print(msg)
            state["vx"] = scale(msg[3], macros.V_MAX)          # forward/backward trans
            #state["omega"] = scale(msg[4], macros.OMEGA_MAX) 
            state["omega"] = scale(1500, macros.OMEGA_MAX)   # stationary rotate
            # msg[4] # fire
            state["vy"] = scale( msg[6], macros.V_MAX)          # left/right trans
            #state["pitch"] = scale(msg[7], macros.PITCH_BOUND) #wire pulled out
            state["pitch"] = scale(1500, macros.OMEGA_MAX)
            state["roll"] = 0 #scale(msg[7], macros.ROLL_BOUND)
            state["yaw"] = scale(msg[5], macros.YAW_BOUND)
            
            # Switch case for manual
            #if (!state["usestable"]):
            if (msg[2] > 1600 and state["pan"] < macros.PAN_BOUND): 
                state["pan"] = float(state["pan"] + 2)
            elif (msg[2] < 1400 and state["pan"] > -macros.PAN_BOUND): 
                state["pan"] = float(state["pan"] - 2)
            if (msg[1] > 1600 and state["tilt"] < macros.TILT_BOUND):
                state["tilt"] = float(state["tilt"] + 2)
            elif (msg[1] < 1400 and state["tilt"] > -macros.TILT_BOUND):
                state["tilt"] = float(state["tilt"] - 2)
            # Switch case for automatic
            #else:
            #    if(msgStable[0] and state["pan"] < macros.PAN_BOUND):
#                    state["pan"] = float(state["pan"] + 2)
#                elif(!msgStable[0] and state["pan"] > -macros.PAN_BOUND) :
#                    state["pan"] = float(state["pan"] - 2)
#                if (msgStable and state["tilt"] < macros.TILT_BOUND):
#                    state["tilt"] = float(state["tilt"] + 2)
#                elif 
            
            
            #state["pan"] = scale(msg[4], macros.PAN_BOUND)
           # state["enable"] = msg[8] > OFFSET
            # bool(msg[9]) # aim mode
            # bool(msg[10]) # enable/disable

def start_server():
    global app
    print("In start server")
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
                         
sched = BackgroundScheduler()
sched.add_job(update_robot_loop, 'interval', seconds=state["timestep"])
sched.add_job(read_message_loop, 'interval', seconds=state["timestep"])                                                            
sched.start()

while True:
    sleep(0.01)

#start_server()

#serverthread = Thread(target=start_server, daemon=True)
#serverthread.start()
                                                                              