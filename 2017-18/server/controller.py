# client template

import hlsockets
from time import sleep

# 0-2 are leg 1, 3-5 are leg 2, 6-8 are leg 3, 9-11 are leg4
# 0 -> BodyUpper, 1 -> UpperMiddle, 2 -> MiddleLower
angles = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

client = hlsockets.UDSClient()
client.open(hlsockets.CONTROLLER)
while True:
    #for i in range(len(angles)):
    #    angles[i] -= 0.01
    client.send(hlsockets.SERVO, angles)
client.close()


