# UDS Client/Server code

The general architecture of our robot is a central forwarding server that connects various `UDSClient`s (you can think of these as [microservices](https://en.wikipedia.org/wiki/Microservices)). These are modular components that communicate over Unix domain sockets (a form of interprocess communication), so that each component can be developed in parallel, the failure of one component does not immediately cause others to fail (at worst, they will block waiting for its output), and we can easily swap out different components with the same interface but different functionality (most notably, connecting to physical servos vs. connecting to virtual servos in a V-REP simulation). 

There is obviously overhead involved in serializing Python objects over a socket (and funnelling these through a single, central server), but this is not the bottleneck for our robot's performance so it's okay. (There is also the benefit that we get around Python's global interpreter lock because each UDSClient is running in a different process, but it's unclear and rather unimportant whether this is a net benefit for performance.)

At a high level, UDSClients work as follows (see `hlsockets.py` and `clienttemplate.py` for actual details): a client microservice creates a UDSClient and self-identifies its purpose, in the form of a number defined with hlsockets.NAME (listed below and in `hlsockets.py`). When it sends a message, it specifies the target identifier, and the central server will automatically forward the message to the right place. It is undefined to open and receive messages from multiple UDSClients with the same identifier. However, it's perfectly fine to send to the same UDSClient from multiple places.

## Protocols:
(defined as hlsockets.NAME)

0: SERVO(angle0, angle1, ..., anglen)

1: CONTROLLER(N/A)

2: TEENSY(N/A)

## How to run simulation:

In `/server/` working directory:

`python3 server.py`

start `mech.ttt` simulation

`python3 simclient.py`

`python3 controller.py`

## Files

Disclaimer: this list has not been updated for this year yet

### server.py 
the central routing server

### simclient.py
symlink to the client forwarding SERVO messages to V-REP

### clienttemplate.py 
a template for UDSClients

### controller.py
symlink to the client for converting controller input to SERVO instructions

### hlsockets.py 
the class definition of UDSClient, a collection of objects to simplify network code
