#!/usr/bin/python

my_config = {
    'controllers': {
        'my_dxl_controller': {
            'sync_read': False,
            'attached_motors': ['leg1', 'leg2', 'leg3', 'leg4', 'turret'],
            'port': 'auto'
        }
    },
    'motorgroups': {
        'leg1': ['hip1', 'knee1', 'ankle1'],
        'leg2': ['hip2', 'knee2', 'ankle2'],
        'leg3': ['hip3', 'knee3', 'ankle3'],
        'leg4': ['hip4', 'knee4', 'ankle4'],
        'turret': ['pan', 'tilt']
    },
    'motors': {
        'hip1': {
            'orientation': 'indirect',
            'type': 'AX-12',
            'id': 1,
            'angle_limit': [-90.0, 90.0],
            'offset': 0.0
        },
        'hip2': {
            'orientation': 'direct',
            'type': 'AX-12',
            'id': 2,
            'angle_limit': [-90.0, 90.0],
            'offset': 0.0
        },
        'hip3': {
            'orientation': 'indirect',
            'type': 'AX-12',
            'id': 3,
            'angle_limit': [-90.0, 90.0],
            'offset': 0.0
        },
        'hip4': {
            'orientation': 'direct',
            'type': 'AX-12', 
            'id': 4,
            'angle_limit': [-90.0, 90.0],
            'offset': 0.0
        },
        'knee1': {
            'orientation': 'indirect',
            'type': 'AX-12',
            'id': 5,
            'angle_limit': [-90.0, 90.0],
            'offset': 0.0
        },
        'knee2': {
            'orientation': 'direct',
            'type': 'MX-28',
            'id': 6,
            'angle_limit': [-90.0, 90.0],
            'offset': 0.0
        },
        'knee3': {
            'orientation': 'indirect',
            'type': 'MX-28',
            'id': 7,
            'angle_limit': [-90.0, 90.0],
            'offset': 0.0
        },
        'knee4': {
            'orientation': 'direct',
            'type': 'MX-28', 
            'id': 8,
            'angle_limit': [-90.0, 90.0],
            'offset': 0.0
        },
        'ankle1': {
            'orientation': 'indirect',
            'type': 'AX-12',
            'id': 9,
            'angle_limit': [-90.0, 90.0],
            'offset': 0.0
        },
        'ankle2': {
            'orientation': 'direct',
            'type': 'AX-12',
            'id': 10,
            'angle_limit': [-90.0, 90.0],
            'offset': 0.0
        },
        'ankle3': {
            'orientation': 'indirect',
            'type': 'AX-12',
            'id': 11,
            'angle_limit': [-90.0, 90.0],
            'offset': 0.0
        },
        'ankle4': {
            'orientation': 'direct',
            'type': 'AX-12', 
            'id': 12,
            'angle_limit': [-90.0, 90.0],
            'offset': 0.0
        },
        'm_pan': {
            'orientation': 'indirect',
            'type': 'AX-12',
            'id': 13,
            'angle_limit': [-90.0, 90.0],
            'offset': 0.0
        },
        'm_tilt': {
            'orientation': 'indirect',
            'type': 'AX-12',
            'id': 14,
            'angle_limit': [-90.0, 90.0],
            'offset': 0.0
        }
    }
}



import pypot

import robot

robot = pypot.robot.from_config(my_config)

for m in robot.leg1:
    print(m.name, m.id, m.present_position)

for m in robot.motors:
    print(m.name, m.present_position)


# robot.left_arm.moving_speed

#set_wheel_mode(robot.turret.pan)


robot.close()

