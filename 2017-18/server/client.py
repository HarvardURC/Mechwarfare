# client template

from socket import socket, AF_UNIX, SOCK_STREAM
from socket import error as sockerr
import pickle
import sys, os, random

# ----- UDS STUFF --------------------------------------------------

UDS_ADDR = b'./server'	# desired UDS path
UDS_BUF = 4096			# size of UDS buffer
PROTOCOL = 0            # SERVO(servo_id, angle)
params = [b'servo_id ', b'angle']

# create a unix domain socket
uds = socket(AF_UNIX, SOCK_STREAM)

# connect to the daemon, which should already exist
try:
    print("\nopening connection")
    uds.connect(UDS_ADDR)
except sockerr:
    print(sockerr)
    sys.exit(1)

# send and receive requests
try:
    msg = bytes(chr(PROTOCOL), 'utf-8') + b''.join([bytes(chr(len(param)), 'utf-8') + param for param in params])
    print("sending " + str(msg))
    uds.sendall(msg)
    print("success!")
    
    """
	p = uds.recv(1)
	
	# wasn't a valid request
	if not p:
		raise Exception("request failed")
	
	p = ord(p)

	# unpickle dictionary returned
	if p == 1:
		pickled = []
		while True:
			packet = uds.recv(UDS_BUF)
			if packet:
				pickled.append(packet)
			else:
				break
		pickled = b''.join(pickled)
		unpickled = pickle.loads(pickled)

		print("received " + str(unpickled))
    
    """

# close the connection
finally:
    print("closing connection\n")
    uds.close()



