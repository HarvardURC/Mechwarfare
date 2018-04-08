#!/usr/bin/env python3.4

import sys

import asyncio

from botnet import settings, protocols
from botnet.logging import *
from botnet.auto import BroadcastServer

from server import Bot

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    bot = Bot()
    server = loop.run_until_complete(
        loop.create_server(lambda: protocols.ServerProtocol(bot),
                           settings.conf["server"].get("address", ""),
                           settings.conf["server"].get("port", 7832)))
    log("Started server...")
    bcast_server = BroadcastServer()
    bcast_server.init_broadcast()
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
