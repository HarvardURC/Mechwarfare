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
    
            # expect transmissions with the format:
            
            # (1 byte)  destination
            
            recv = conn.recv(1)
            if(len(recv) < 1):
                continue
            dest, = struct.unpack('B', recv)
            
            if(conns.get(dest, None)):
                conns[dest].close()
            conns[dest] = conn
        else:
        
            # expect transmissions with the format:

            # (1 byte)	destination
            # (4 bytes) packet size
            # (n bytes) packet
            
            try:
                recv = conn.recv(1)
                if(len(recv) < 1):
                    s.close()
                    continue
                dest, = struct.unpack('B', recv)
        
                recv = conn.recv(4)
                if(len(recv) < 4):
                    s.close()
                    continue
                plen, = struct.unpack('I', recv)
                
                packet = conn.recv(plen)
                if(len(packet) < plen):
                    print("malformed packet: " + str(packet))

                conns[dest].sendall(struct.pack('I', plen) + packet)
            except:
                s.close()

    todel = []
    for key in conns.keys():
        if(conns[key]._closed):
            todel.append(key)

    for key in todel:
        del conns[key]
