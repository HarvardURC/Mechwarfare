#!/usr/bin/env python3

import sys, os

from botnet.settings import Configuration
from botnet.auto import AutoClient
from botnet.logging import *
from botnet.protocols import ClientProtocol

conf = Configuration()
conf.load(os.environ.get("SETTINGS","settings.json"))

import asyncio

loop = asyncio.get_event_loop()

from client import Client
from client.joystick import Joystick
    
def autoconf(conf):
    log("Searching for server...")
    auto = AutoClient()
    conf["server"] = loop.run_until_complete(auto.get_server)
    log("done")
    conf.save()

if __name__ == "__main__":
    if "--search" in sys.argv or "-s" in sys.argv or not conf["server"].get("address"):
        autoconf(conf)

    client = Client(conf["server"].get("address"))
        
    log("Connecting to {}:{}...".format(conf["server"].get("address"),
                                                conf["server"].get("port")))
    coro = loop.create_connection(lambda: ClientProtocol(client),
                                  conf["server"].get("address"), conf["server"].get("port"))
    socket, protocol = loop.run_until_complete(coro)
    joystick = Joystick(protocol)
    log("Connected.")
    loop.run_forever()
