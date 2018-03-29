from flask import Flask, request, render_template
import json
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("slidey.html")

@app.route('/handler', methods=['POST'])
def slidey():
	x = json.loads(request.data)
	print(x) #THIS IS THE OUTPUT DICTIONARY
	return ""

app.run()