# client template

from hlsockets import UDSClient
from time import sleep

PROTOCOL = 0            # SERVO(servo_id, angle)
params = [b'servo_id ', b'angle']

client = UDSClient()
client.open(PROTOCOL)
while True:
    client.send(0, params)
    params = client.recv()
    print(str(params) + "\n")
    sleep(1)
client.close()


