# server

from socket import socket, AF_UNIX, SOCK_STREAM
import pickle, struct, os

# ----- UDS STUFF --------------------------------------------------

UDS_ADDR = b'./server'	# desired UDS path
QUEUE_MAX = 256			# maximum number of waiting connections

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
    
    # (1 byte)	destination
    # (4 bytes) packet size
    # (1 byte)  number of parameters
    # (2 bytes)	len(first parameter)
    # (n bytes)	first parameter
    # (2 bytes)	len(second parameter)
    # (m bytes)	second parameter
    # etc.
    
    dest, = struct.unpack('B', conn.recv(1))
    
    dest, = struct.unpack('B', conn.recv(1))
    plen, = struct.unpack('I', conn.recv(4))
    print("dest = " + str(dest))
    print("plen = " + str(plen))
    #packet = conn.recv(plen)
    #print(packet)
    
    nparams, = struct.unpack('B', conn.recv(1))
    params = [0] * nparams
    print("nparams = " + str(nparams))

    # receive parameters
    for i in range(nparams):
        n, = struct.unpack('H', conn.recv(2))
        params[i] = conn.recv(n)
        
        print("received " + str(params[i]))

    print("closing connection")
    conn.close()
