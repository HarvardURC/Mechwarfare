from flask import Flask, request, render_template
import json
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
from drivers_test import init_robot, update_robot
import serial
import macros


dt = 0.05
state = "hi"
body = init_robot()

ser = serial.Serial('/dev/ttyACM0', 38400, timeout=1)
offset = 1020
controller_range = 500

def scale(num, max):
    # scale serial output based on the maximum
    return max * float(num - offset) / float(controller_range)

def fucking_loop():
    global state
    print(state)
    if (state != "hi"):
        update_robot(body, state, dt)
        print("vx: ", state["vx"])
        print("vy: ", state["vy"])
        print("omega: ", state["omega"])
        print("pitch: ", state["pitch"])
        print("roll: ", state["roll"])
        print("yaw: ", state["yaw"])    

def fucking_teensy_loop():
    global state
    print("aaaa")
    if (state != "hi"):
        if (bool(current_state["useradio"])):
            msg = ser.readline() # data might get backlogged here
                                 # but if you move it out, it'll error if serial isn't plugged in
            msg = [int(i) for i in msg.split(',')]

            state["vx"] = scale(msg[2], macros.V_MAX)          # forward/backward trans
            state["omega"] = scale(msg[3], macros.OMEGA_MAX)   # stationary rotate
            # msg[4] # fire
            state["vy"] = scale(msg[5], macros.V_MAX)          # left/right trans
            state["pitch"] = scale(msg[6], macros.PITCH_BOUND)
            state["roll"] = scale(msg[7], macros.ROLL_BOUND)
            state["yaw"] = scale(msg[8], macros.YAW_BOUND)
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
    print("hiaaaaaa")
    global state
    state = json.loads(request.data.decode('utf-8'))
    return ""

sched = BackgroundScheduler()
sched.add_job(fucking_loop, 'interval', seconds=dt)
sched.add_job(fucking_teensy_loop, 'interval', seconds=dt)
sched.start()

start_server()

#serverthread = Thread(target=start_server, daemon=True)
#serverthread.start()
