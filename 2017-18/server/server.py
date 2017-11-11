# server

from socket import socket, AF_UNIX, SOCK_STREAM
import pickle, struct, os, select

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

conns = {"uds" : uds}

# wait for connections forever
while True:
    # accept a connection
    readable, writeable, broken = select.select(conns.values(), [], conns.values())
    
    for s in readable:
        if s is uds:
            conn, client_addr = uds.accept()
            print("\nopening connection")
    
            # expect transmissions with the format:
            
            # (1 byte)  destination
            
            recv = conn.recv(1)
            if(len(recv) < 1):
                continue
            dest, = struct.unpack('B', recv)
            
            conns[dest] = conn
        else:
            # expect transmissions with the format:
            
            # (1 byte)	destination
            # (4 bytes) packet size
            # (n bytes) packet

            recv = conn.recv(1)
            if(len(recv) < 1):
                continue
            dest, = struct.unpack('B', recv)
            
            recv = conn.recv(4)
            if(len(recv) < 4):
                continue
            plen, = struct.unpack('I', recv)
            
            print("dest = " + str(dest))
            print("plen = " + str(plen))
            
            packet = conn.recv(plen)
            if(len(packet) < plen):
                print("malformed packet: " + str(packet))
            else:
                print(str(packet) + "\n")

            conns[dest].sendall(packet)

    for s in broken:
        if s is uds:
            print("you dun fuked up")
        else:
            print("closing connection")
            s.close()
