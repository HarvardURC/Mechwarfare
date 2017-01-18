from asyncio import Protocol

import pickle

from struct import Struct

from .errors import *
from .logging import *
from .auto import BroadcastServer

HEADER_STRUCT = Struct("!BH4sHd")

class BotProtocol(Protocol):
    __version__  = 1

    def __init__(self):
        self.header = b''
        self.data = b''

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        while len(data):
            while len(data) and len(self.header) < HEADER_STRUCT.size:
                self.header += data[0:1]
                data = data[1:]
            version, self.length, self.comm, self.cid, self.double = HEADER_STRUCT.unpack(self.header)
            if version != self.__version__:
                raise NetworkError("Protocol version mismatch: need {}, got {}".format(
                    self.__version__, version))
            while len(data) and (len(self.data) < self.length):
                bytes_needed = self.length - len(self.data)
                self.data += data[:bytes_needed]
                data = data[bytes_needed:]
            if len(self.data) == self.length:
                try:
                    self.on_message(self.comm.decode(), self.cid, self.double, self.data)
                except Exception as err:
                    last_exception()
                finally:
                    self.data = b''
                    self.header = b''

    def send_message(self, comm, cid=0, double=0, data=b""):
        if len(comm) > 4:
            raise CommandError("Command too long!")
        header = HEADER_STRUCT.pack(self.__version__, len(data), comm.encode(),cid, double)
        self.transport.write(header + data)

    def on_message(self, command, cid, double, data):
        debug(command, cid, double, data)
        data = (data,) if data else tuple()
        try:
            func = getattr(self.receiver, command)
        except AttributeError:
            warn("Unknown command received:", command)
        else:
            func(cid, double, *data)

class ServerProtocol(BotProtocol):
    def __init__(self, bot):
        super().__init__()
        self.receiver = bot

    def connection_made(self, transport):
        super().connection_made(transport)
        peername = transport.get_extra_info("peername")
        self.receiver.add_client(self, peername)
        debug("Connection from {}".format(peername))

    def connection_lost(self, exc):
        self.receiver.remove_client(self)

class ClientProtocol(BotProtocol):
    def __init__(self, client):
        super().__init__()
        self.receiver = client

    def connection_made(self, transport):
        super().connection_made(transport)
        client.connected(self)
        debug("Connected to {}".format(transport.get_extra_info("peername")))

    def connection_lost(self, exc):
        self.client.fatal("Lost Connection!")
