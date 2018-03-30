from flask import Flask, request, render_template
import json
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
from drivers_test import init_robot, update_robot


dt = 0.05
state = "hi"
body = init_robot()

def fucking_loop():
    global state
    if (state != "hi"):
        update_robot(body, state, dt)

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
sched.add_job(fucking_loop, 'interval', seconds=dt)
sched.start()

start_server()

#serverthread = Thread(target=start_server, daemon=True)
#serverthread.start()
