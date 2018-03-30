from flask import Flask, request, render_template
import json
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler


dt = 0.05
state = "hi"

def update_robot():
	global state
	print(state)

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
sched.add_job(update_robot, 'interval', seconds=dt)
sched.start()

start_server()

#serverthread = Thread(target=start_server, daemon=True)
#serverthread.start()
