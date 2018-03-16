from time import sleep
import drivers, hlsockets

# 0-2 are leg 1, 3-5 are leg 2, 6-8 are leg 3, 9-11 are leg4
joints = [
            "Leg1_BodyUpper", "Leg1_UpperMiddle", "Leg1_MiddleLower",
            "Leg2_BodyUpper", "Leg2_UpperMiddle", "Leg2_MiddleLower",
            "Leg3_BodyUpper", "Leg3_UpperMiddle", "Leg3_MiddleLower",
            "Leg4_BodyUpper", "Leg4_UpperMiddle", "Leg4_MiddleLower"
         ]

jids = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # dynamixel servo ids
positions = None

# default offsets (in units of 0.29 degrees)
offsets = {
            "Leg1_BodyUpper"    : 0,
            "Leg1_UpperMiddle"  : 0,
            "Leg1_MiddleLower"  : 0,
            "Leg2_BodyUpper"    : 0,
            "Leg2_UpperMiddle"  : 0,
            "Leg2_MiddleLower"  : 0,
            "Leg3_BodyUpper"    : 0,
            "Leg3_UpperMiddle"  : 0,
            "Leg3_MiddleLower"  : 0,
            "Leg4_BodyUpper"    : 0,
            "Leg4_UpperMiddle"  : 0,
            "Leg4_MiddleLower"  : 0
          }

min_pos = 400
max_pos = 1000

err = init_motors()

client = hlsockets.UDSClient(0.03)
client.open(hlsockets.SERVO)
while 1:
    params = client.recv()
    if(params):
        positions = [1.0/0.29 * angle + offsets[joints[id]] for id, angle in enumerate(params)]
        drivers.set_target_positions(positions)
client.close()
err = deinit_motors()
