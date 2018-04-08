from .logging import *
from .settings import conf

from socket import *

from collections import defaultdict

import asyncio

import json

import netifaces

class BroadcastServer:
    def init_broadcast(self):
        self._bcast_socket = socket(AF_INET, SOCK_DGRAM)
        self._bcast_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._bcast_loop = asyncio.get_event_loop()
        self._bcast_loop.call_soon(self.broadcast_presence)
        
    def broadcast_presence(self):
        self._bcast_loop.call_later(1, self.broadcast_presence)
        self._bcast_socket.sendto((self._bcast_info()+"\n").encode(),
                                  ("255.255.255.255",
                                   conf["server"]["bcast_port"]))

    def _bcast_info(self):
        server = conf["server"].copy()
        if not server["address"]:
            ip = "127.0.0.1"
            iface = [i for i in netifaces.interfaces() if
                     i.startswith("e") or i.startswith("w")]
            for i in iface:
                addresses = netifaces.ifaddresses(i)
                if addresses.get(netifaces.AF_INET, False):
                    ip = addresses[netifaces.AF_INET][0]["addr"]
            server["address"] = ip
        if not server["hostname"]:
            server["hostname"] = gethostname()
        return json.dumps(server)

class AutoClient:
    def __init__(self, cb=None):
        self._bcast_socket = socket(AF_INET, SOCK_DGRAM)
        self._bcast_socket.bind(("",conf["server"]["bcast_port"]))
        self.servers = {}
        self._data = defaultdict(bytes)
        self._loop = asyncio.get_event_loop()
        self._cb = cb
        self.reset()

    def reset(self):
        self._loop.call_soon(self.receive)
        self.get_server = asyncio.Future()
        
    def receive(self):
        data, addr = self._bcast_socket.recvfrom(1024)
        if data:
            self._data[addr] += data
            if b"\n" in self._data[addr]:
                obj = None
                for i in self._data[addr].decode().split("\n"):
                    try:
                        obj = json.loads(i)
                        self.servers[obj["address"]] = obj
                    except ValueError as err:
                        pass
                if obj:
                    self.get_server.set_result(obj)
                    if self._cb:
                        self._cb(obj)
        if not self.get_server.done():
            self._loop.call_soon(self.receive)

    def get_port(self, addr):
        return self.servers[addr]["port"]
                    
__all__ = ["BroadcastServer", "AutoClient"]
