# higher level sockets

from socket import socket, AF_UNIX, SOCK_STREAM, timeout
from socket import error as sockerr
import pickle, struct, os, sys

UDS_ADDR = b'./server'
UDS_BUF = 4096

SERVO = 0
CONTROLLER = 1
TEENSY = 2

class UDSClient:

    # create a new unix domain socket client
    def __init__(self, timeout=None):
        self.conn = socket(AF_UNIX, SOCK_STREAM)
        if timeout != None:
            self.conn.settimeout(timeout)
    
    # receive messages sent to 'dest' (0-255)
    def open(self, dest):
        try:
            self.conn.connect(UDS_ADDR)
            self.conn.sendall(struct.pack('B', dest))
        except sockerr:
            print(sockerr)
            sys.exit(1)

    # send a message with list of parameters 'params' to 'dest' (0-255)
    
    # (1 byte)	destination
    # (4 bytes) packet size
    # (n bytes) pickled object
    # etc.
    def send(self, dest, params):
        msg = pickle.dumps(params)
        msg = struct.pack('B', dest) + struct.pack('I', len(msg)) + msg
        self.conn.sendall(msg)

    # receive and parse a message with the format:
    
    # (4 bytes) packet size
    # (n bytes) pickled object
    # etc.
    def recv(self):
        try:
            ret = self.conn.recv(4)
        except timeout:
            return None
        
        plen, = struct.unpack('I', ret)
        packet = self.conn.recv(plen)
        
        params = pickle.loads(packet)

        return params

    def close(self):
        self.conn.close()
        self.conn = None
