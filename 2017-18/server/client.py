# client template

from hlsockets import UDSClient

PROTOCOL = 0            # SERVO(servo_id, angle)
params = [b'servo_id ', b'angle']

client = UDSClient()
client.open(PROTOCOL)
client.send(0, params)
client.close()


