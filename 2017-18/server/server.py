# server

from socket import socket, AF_UNIX, SOCK_STREAM
import pickle
import os

# ----- UDS STUFF --------------------------------------------------

UDS_ADDR = b'./server'	# desired UDS path
QUEUE_MAX = 8			# maximum number of waiting connections

# make sure we're starting fresh
try:
    os.unlink(UDS_ADDR)
except OSError:
    if os.path.exists(UDS_ADDR):
        raise Exception("UDS exists but can't be unlinked...")

# create a unix domain socket
uds = socket(AF_UNIX, SOCK_STREAM)
uds.bind(UDS_ADDR)
uds.listen(QUEUE_MAX)

# wait for connections forever
while True:
    # accept a connection
    conn, client_addr = uds.accept()
    print("\nopening connection")
    
    # expect transmissions with the format:
    
    # (1 byte)	number of parameters
    # (1 byte)	len(first parameter)
    # (n bytes)	first parameter
    # (1 byte)	len(second parameter)
    # (m bytes)	second parameter
    # etc.
    
    protocol = ord(conn.recv(1))
    print("protocol = " + str(protocol))
    
    # 0 = SERVO(servo_id, angle)
    nparams = [2, None, None]
    p = nparams[protocol]
    params = [0] * p
    print("nparams = " + str(p))

    for i in range(p):
        n = ord(conn.recv(1))
        params[i] = conn.recv(n)
        
        print("received " + str(params[i]))

    print("closing connection")
    conn.close()
