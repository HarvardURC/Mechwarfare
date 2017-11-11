# UDS Client/Server code

server.py is the central routing server

simclient.py is the client for connecting to V-REP

controller.py is the client for sending servo instructions

clienttemplate.py is a template for client connections

hlsockets.py is a collection of objects that simplify network code


## Protocols:

0: SERVO(angle0, angle1, ..., anglen)
1: CONTROLLER(N/A)

## How to run simulation:

python3 server.py
start mech.ttt simulation
python3 simclient.py
python3 controller.py
