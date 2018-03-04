import numpy
import math
import time
from threading import Thread
import threading
import pypot.dynamixel

"""motor stuff from last year"""

# Config code
my_config = {
    'controllers': {
        'my_dxl_controller': {
            'sync_read': False,
            'attached_motors': ['leg1', 'leg2', 'leg3', 'leg4', 'turret'],
            'port': '/dev/ttyACM0'
        }
    },
    'motorgroups': {
        'leg1': ['hip1', 'knee1', 'ankle1'],
        'leg2': ['hip2', 'knee2', 'ankle2'],
        'leg3': ['hip3', 'knee3', 'ankle3'],
        'leg4': ['hip4', 'knee4', 'ankle4'],
        'turret': ['pan', 'tilt', 'string']
        
    },
    'motors': {
        'hip4': {
            'orientation': 'direct',
            'type': 'AX-12',
            'id': 8,
            'angle_limit': [-150.0, 150.0],
            'offset': 0.0
        },
        'knee4': {
            'orientation': 'direct',
            'type': 'AX-12',
            'id': 2,
            'angle_limit': [-150.0, 150.0],
            'offset': 0.0
        },
        'ankle4': {
            'orientation': 'direct',
            'type': 'AX-12',
            'id': 11,
            'angle_limit': [-150.0, 150.0],
            'offset': 0.0
        },
        'hip3': {
            'orientation': 'direct',
            'type': 'AX-12',
            'id': 12,
            'angle_limit': [-150.0, 150.0],
            'offset': 0.0
        },
        'knee3': {
            'orientation': 'direct',
            'type': 'AX-12',
            'id': 10,
            'angle_limit': [-150.0, 150.0],
            'offset': 0.0
        },
        'ankle3': {
            'orientation': 'direct',
            'type': 'AX-12',
            'id': 5,
            'angle_limit': [-150.0, 150.0],
            'offset': 0.0
        },
        'hip2': {
            'orientation': 'direct',
            'type': 'AX-12',
            'id': 15,
            'angle_limit': [-150.0, 150.0],
            'offset': 0.0
        },
        'knee2': {
            'orientation': 'direct',
            'type': 'AX-12',
            'id': 6,
            'angle_limit': [-150.0, 150.0],
            'offset': 0.0
        },
        'ankle2': {
            'orientation': 'direct',
            'type': 'AX-12',
            'id': 4,
            'angle_limit': [-150.0, 150.0],
            'offset': 0.0
        },
        'hip1': {
            'orientation': 'direct',
            'type': 'AX-12',
            'id': 9,
            'angle_limit': [-150.0, 150.0],
            'offset': 0.0
        },
        'knee1': {
            'orientation': 'direct',
            'type': 'AX-12',
            'id': 1,
            'angle_limit': [-150.0, 150.0],
            'offset': 0.0
        },
        'ankle1': {
            'orientation': 'direct',
            'type': 'AX-12',
            'id': 3,
            'angle_limit': [-150.0, 150.0],
            'offset': 0.0
        },
        'pan': {
            'orientation': 'direct',
            'type': 'AX-18',
            'id': 17,
            'angle_limit': [-150.0, 150.0],
            'offset': 0.0
        },
        'tilt': {
            'orientation': 'direct',
            'type': 'AX-18',
            'id': 18,
            'angle_limit': [-150.0, 150.0],
            'offset': 0.0
        },
        'string': {
            'angle_limit': [-150.0, 150.0],
            'orientation': 'direct',
            'type': 'AX-12',
            'id': 19,
            'offset': 0.0
        }
    }
}

dxl_io = pypot.dynamixel.DxlIO('/dev/ttyACM0', baudrate=57600)
