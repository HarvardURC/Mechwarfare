# higher level sockets

from socket import socket, AF_UNIX, SOCK_STREAM
from socket import error as sockerr
import pickle, struct, os, sys

UDS_ADDR = b'./server'
UDS_BUF = 4096

# 0 = SERVO(servo_id, angle)

class UDSClient:

    # create a new unix domain socket client
    def __init__(self):
        self.conn = socket(AF_UNIX, SOCK_STREAM)
    
    # receive messages sent to 'dest' (0-255)
    def open(self, dest):
        try:
            print("\nopening connection")
            self.conn.connect(UDS_ADDR)
            self.conn.sendall(struct.pack('B', dest))
        except sockerr:
            print(sockerr)
            sys.exit(1)

    # send a message with list of parameters 'params' to 'dest' (0-255)
    def send(self, dest, params):
        msg = struct.pack('B', len(params)) + b''.join([struct.pack('H', len(param)) + param for param in params])
        msg = struct.pack('B', dest) + struct.pack('I', len(msg)) + msg
        print("sending " + str(msg))
        self.conn.sendall(msg)
        print("success!")

    # receive a message
    # returns a list of parameters
    def recv(self):
        nparams, = struct.unpack('B', self.conn.recv(1))
        params = [0] * nparams
        print("nparams = " + str(nparams))

        # receive parameters
        for i in range(nparams):
            n, = struct.unpack('H', self.conn.recv(2))
            params[i] = self.conn.recv(n)
            
            print("received " + str(params[i]))
        return params

    def close(self):
        self.conn.close()
        self.conn = None
