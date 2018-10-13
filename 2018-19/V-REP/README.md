# V-REP / Python interface

Useful links:

[V-REP download (pro^edu)](http://www.coppeliarobotics.com/downloads.html)

[How to build a robot model](http://www.coppeliarobotics.com/helpFiles/en/buildingAModelTutorial.htm)

[How to build a robot model 2](http://www.coppeliarobotics.com/helpFiles/en/hexapodTutorial.htm)

---

[Server Side](http://www.coppeliarobotics.com/helpFiles/en/remoteApiServerSide.htm)

[Client Side](http://www.coppeliarobotics.com/helpFiles/en/remoteApiClientSide.htm)

[Python APIs](http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm)

[Video Tutorial](https://www.youtube.com/watch?v=SQont-mTnfM)

---

You need `remoteApi.dll`, `remoteApi.dylib`, or `remoteApi.so` from `[V-REP install] > programming > remoteApi > lib > lib` in your working directory in order to interface with Python. (These correspond to Windows, macOS, and Linux respectively.)

We access the V-REP scene `simserver.ttt` with Python as a remote API client in `simclient.py`.

---

### hlsockets.py

The class definition of UDSClient

### remoteApi.dylib

The dynamic library for the V-REP remote C API (for macOS)

### simclient.py

A UDSClient that receives servo instructions and forwards them to V-REP

### simserver.ttt

V-REP simulation file with:
* (currently) the 2017-18 robot design
* an environment script that opens V-REP to remote control

### vrep.py

V-REP Python/C interface. Do not change this file.

### vrepConst.py

Constants for the V-REP Python/C interface. Do not change this file.
