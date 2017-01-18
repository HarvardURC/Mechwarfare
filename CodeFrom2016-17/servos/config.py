robot_config = {
    'controllers': {
        'my_dxl_controller': {
            'sync_read': False,
            'attached_motors': ['leg1', 'leg2', 'leg3', 'leg4', 'turret'],
            'port': 'auto'
        }
    },
    'motorgroups': {
        'leg1': ['m1', 'm2', 'm3'],
        'leg2': ['m4', 'm5', 'm6'],
        'leg3': ['m7', 'm8', 'm9'],
        'leg4': ['m10', 'm11', 'm12'],
        'turret': ['m13']
    },
    'motors': dict([("m{}".format(i+1), {
        'orientation': 'indirect',
        'type': 'AX-12A',
        'id': i+1,
        'angle_limit': [-90.0, 90.0],
        'offset': 0.0
    }) for i in range(13)])
}
