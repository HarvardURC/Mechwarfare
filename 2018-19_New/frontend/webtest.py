from flask import Flask, request, render_template
import json
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
from drivers_test import init_robot, update_robot
import serial
import macros
from time import time
import helpers

# Global variable to keep track of the state of the robot
state = {
    "enable":True,
    "gohome":False,
    "vx":0.,
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
    "useradio": True
}

body = init_robot()

try:
    ser = serial.Serial('/dev/ttyACM0', 38400, timeout=1) # opens serial port to communicate with teensy
except:
    ser = serial.Serial('/dev/ttyACM1', 38400, timeout=1)

offset = (990+2014)/2
controller_range = (2014-990)/2

def scale(num, max):
    # scale serial output based on the maximum
    return max * float(num - offset) / float(controller_range)

def fucking_loop():
    global state
    if state["enable"]:
        #tv_fl = time()
        update_robot(body, state, state["timestep"])
        #print("aaaaaa: ",time()-tv_fl)
        #print("vx: ", state["vx"])
        #print("vy: ", state["vy"])
        #print("omega: ", state["omega"])
        #print("pitch: ", state["pitch"])
        #print("roll: ", state["roll"])
        #print("yaw: ", state["yaw"])
        #print("\n\n")

def fucking_teensy_loop():
    global state
    if (bool(state["useradio"])):
    	if (ser.in_waiting > 0):
            msg = ser.readline().decode('utf-8')
            msg = [int(i) for i in msg.split(', ')]
            print(msg)
            state["vx"] = scale(msg[3], macros.V_MAX)          # forward/backward trans
            state["omega"] = scale(msg[4], macros.OMEGA_MAX)   # stationary rotate
            # msg[4] # fire
            state["vy"] = scale(msg[6], macros.V_MAX)          # left/right trans
            state["pitch"] = scale(msg[7], macros.PITCH_BOUND)
            state["roll"] = 0 #scale(msg[7], macros.ROLL_BOUND)
            state["yaw"] = scale(msg[2], macros.YAW_BOUND)
            state["enable"] = msg[8] > offset
        	# bool(msg[9]) # aim mode
        	# bool(msg[10]) # enable/disable

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

sched = BackgroundScheduler()
sched.add_job(fucking_loop, 'interval', seconds=state["timestep"])
sched.add_job(fucking_teensy_loop, 'interval', seconds=state["timestep"])
sched.start()

start_server()

#serverthread = Thread(target=start_server, daemon=True)
#serverthread.start()
