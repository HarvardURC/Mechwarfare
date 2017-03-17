import settings as s

s.isAnimation = True

from visual import *
import time
import math
from threading import Thread
import threading
import numpy
import json
import random



# helper functions
def vectorAdd(tuple1, tuple2):
	return tuple(map(lambda x, y: x + y, tuple1, tuple2))

def revForV(tuple):
	return (tuple[0], tuple[2], -tuple[1])


# define floor and base
floor = box (pos=revForV((0,0,0)), length=50, height=0.1, width=100, color=color.white)
base = box (pos=revForV((0,0,-s.HOMEPOS_FOOTHEIGHT + s.BASE_THICKNESS/2.0 + s.FOOT_RADIUS)), length=s.BASE_LENGTH, height= s.BASE_THICKNESS, width=s.BASE_WIDTH, color=color.red, axis=revForV((1,0,0)))

panBox = box (pos = numpy.add(base.pos, revForV([0,0, s.PANBOX_HEIGHT/2.0])), length=s.PANBOX_LENGTH, width=s.PANBOX_WIDTH, height= s.PANBOX_HEIGHT, color=color.green, axis=revForV((1,0,0)))
barrel = cylinder(pos=numpy.add(panBox.pos, revForV([0,0, s.PANBOX_HEIGHT/2.0])),  axis=(1,0,0), length = s.BARREL_LENGTH, radius=.1)



# initialize Leg Arrows
legs = {
    'leg1': {
        'vert': arrow(pos=(0,0,1.0), axis=revForV((0,0,2.0)), shaftwidth=.5, color=color.yellow),
        'horiz': arrow(pos=(0,0,1.0), axis=revForV((0,0,2.0)), shaftwidth=.5, color=color.yellow),
        'knee2ankle': arrow(pos=(0,0,1.0), axis=revForV((0,0,2.0)), shaftwidth=.5, color=color.green),
        'ankle2foot': arrow(pos=(0,0,1.0), axis=revForV((0,0,2.0)), shaftwidth=.5, color=color.blue),
        'foot': sphere(pos=(1,2,1), radius=s.FOOT_RADIUS, color=color.black)
    },
    'leg2': {
        'vert': arrow(pos=(0,0,1.0), axis=revForV((0,0,2.0)), shaftwidth=.5, color=color.yellow),
        'horiz': arrow(pos=(0,0,1.0), axis=revForV((0,0,2.0)), shaftwidth=.5, color=color.yellow),
        'knee2ankle': arrow(pos=(0,0,1.0), axis=revForV((0,0,2.0)), shaftwidth=.5, color=color.green),
        'ankle2foot': arrow(pos=(0,0,1.0), axis=revForV((0,0,2.0)), shaftwidth=.5, color=color.blue),
        'foot': sphere(pos=(1,2,1), radius=s.FOOT_RADIUS, color=color.black)
    },
    'leg3': {
        'vert': arrow(pos=(0,0,1.0), axis=revForV((0,0,2.0)), shaftwidth=.5, color=color.yellow),
        'horiz': arrow(pos=(0,0,1.0), axis=revForV((0,0,2.0)), shaftwidth=.5, color=color.yellow),
        'knee2ankle': arrow(pos=(0,0,1.0), axis=revForV((0,0,2.0)), shaftwidth=.5, color=color.green),
        'ankle2foot': arrow(pos=(0,0,1.0), axis=revForV((0,0,2.0)), shaftwidth=.5, color=color.blue),
        'foot': sphere(pos=(1,2,1), radius=s.FOOT_RADIUS, color=color.black)
    },
    'leg4': {
        'vert': arrow(pos=(0,0,1.0), axis=revForV((0,0,2.0)), shaftwidth=.5, color=color.yellow),
        'horiz': arrow(pos=(0,0,1.0), axis=revForV((0,0,2.0)), shaftwidth=.5, color=color.yellow),
        'knee2ankle': arrow(pos=(0,0,1.0), axis=revForV((0,0,2.0)), shaftwidth=.5, color=color.green),
        'ankle2foot': arrow(pos=(0,0,1.0), axis=revForV((0,0,2.0)), shaftwidth=.5, color=color.blue),
        'foot': sphere(pos=(1,2,1), radius=s.FOOT_RADIUS, color=color.black)
    }
}

def makeRadian(angles):
    return [math.radians(angles[0]),math.radians(angles[1]), math.radians(angles[2])]

def getCurrentAngles(legNum):

    with open('SharedVariables.json', 'r') as f:
        data = json.load(f)
    [servoHipAngle, servoKneeAngle, servoAnkleAngle] = [data["ServoPos"][legNum - 1][0], data["ServoPos"][legNum - 1][1], data["ServoPos"][legNum - 1][2]] 

    idealHipAngle = servoHipAngle + s.IDEAL_SERVO_POSITIONS[legNum - 1][0] - s.HOME_LEG_POSITIONS[legNum - 1][0]
    idealKneeAngle = servoKneeAngle + s.IDEAL_SERVO_POSITIONS[legNum - 1][1] - s.HOME_LEG_POSITIONS[legNum - 1][1]
    idealAnkleAngle = servoAnkleAngle + s.IDEAL_SERVO_POSITIONS[legNum - 1][2] - s.HOME_LEG_POSITIONS[legNum - 1][2]
    
    return (idealHipAngle % 360, idealKneeAngle % 360, idealAnkleAngle % 360)

def updateLegsAndBase():

    # get ideal angles in radian for the visual arrows to update
    ServoPosRadian = [makeRadian(getCurrentAngles(2)),makeRadian(getCurrentAngles(2)),makeRadian(getCurrentAngles(3)),makeRadian(getCurrentAngles(4))]
    # loop through all legs
    for i in range(1,5):
        x_neg = (-1) ** ((i - 1)%3 > 0 )
        y_neg = (-1)** math.floor(i/3)
        leg = str(i)

        legs['leg'+leg]['vert'].pos = vectorAdd(base.pos,revForV(aF.rotateVector((x_neg * s.BASE_LENGTH/2.0,y_neg * s.BASE_WIDTH/2.0,-s.BASE_THICKNESS/2.0), s.BaseOrientationAngle)))
        legs['leg'+leg]['vert'].axis = revForV((0,0,s.HIPVERTUP_LENGTH))
        legs['leg'+leg]['horiz'].pos = vectorAdd(legs['leg'+leg]['vert'].pos,legs['leg'+leg]['vert'].axis)
        legs['leg'+leg]['horiz'].axis = revForV(aF.rotateVector((s.HIPHORIZ_LENGTH*cos(ServoPosRadian[i - 1][0]),s.HIPHORIZ_LENGTH*sin(ServoPosRadian[i - 1][0]),0), s.BaseOrientationAngle))
        legs['leg'+leg]['knee2ankle'].pos = vectorAdd(legs['leg'+leg]['horiz'].pos,legs['leg'+leg]['horiz'].axis)
        legs['leg'+leg]['knee2ankle'].axis = revForV(aF.rotateVector((s.L1_LENGTH*cos(ServoPosRadian[i - 1][1])*cos(ServoPosRadian[i - 1][0]),s.L1_LENGTH*cos(ServoPosRadian[i - 1][1])*sin(ServoPosRadian[i - 1][0]),s.L1_LENGTH*sin(ServoPosRadian[i - 1][1])), s.BaseOrientationAngle))
        legs['leg'+leg]['ankle2foot'].pos = vectorAdd(legs['leg'+leg]['knee2ankle'].pos,legs['leg'+leg]['knee2ankle'].axis)
        legs['leg'+leg]['ankle2foot'].axis = revForV(aF.rotateVector((s.L2_LENGTH*cos(ServoPosRadian[i - 1][2])*cos(ServoPosRadian[i - 1][0]),s.L2_LENGTH*cos(ServoPosRadian[i - 1][2])*sin(ServoPosRadian[i - 1][0]),s.L2_LENGTH*sin(ServoPosRadian[i - 1][2])), s.BaseOrientationAngle))

        legs['leg'+leg]['foot'].pos = vectorAdd(legs['leg'+leg]['ankle2foot'].pos,legs['leg'+leg]['ankle2foot'].axis)




        with open('SharedVariables.json', 'r') as f:
            data = json.load(f)

        base.pos = revForV(data["BasePos"])
        base.axis =revForV((math.cos(data["BaseOrientationAngle"]),math.sin(data["BaseOrientationAngle"]),0))
        base.length = s.BASE_LENGTH

        TurretPosRadians = [math.radians(data["TurretPos"][0]), math.radians(data["TurretPos"][1])]
        panBox.axis = revForV((math.cos(data["BaseOrientationAngle"] + TurretPosRadians[0]),math.sin(data["BaseOrientationAngle"] + TurretPosRadians[0]),0))
        panBox.pos = numpy.add(base.pos, revForV([0,0,s.PANBOX_HEIGHT/2.0]))
        panBox.length = s.PANBOX_LENGTH


        barrel.pos = numpy.add(panBox.pos, revForV([0,0,s.PANBOX_HEIGHT/2.0]))
        barrel.axis = revForV((math.cos(TurretPosRadians[1]) * math.cos(data["BaseOrientationAngle"] + TurretPosRadians[0]),math.cos(TurretPosRadians[1]) * math.sin(data["BaseOrientationAngle"] + TurretPosRadians[0]), math.sin(TurretPosRadians[1])))
        barrel.length = s.BARREL_LENGTH
        


        

updateLegsAndBase()


    

servoThread = Thread(target=aF.updateServosAndBase, args=())
servoThread.start()


'''
# control needs separate thread because of Vpython loop
controlLegsThread = Thread(target=legControl, args=())
controlLegsThread.start()
'''


'''
scene2 = display(title='Examples of Tetrahedrons',
     x=20, y=0, width=600, height=800,
     center=(5,0,0), background=(0,1,1))
'''



#legControl()


# I copied this code that allows the visualizer to be rotated and zoomed in, using a mouse.
scene.userzoom = False
scene.userspin = False
scene.range = 15

rangemin = .5
rangemax = 40

zoom = False
spin = False


while True:
    rate(s.t_per_second)


    # controls for rotation and such
    if scene.kb.keys:
        k = scene.kb.getkey()
        if k == 'z':
            scene.range = scene.range / 1.5 
        elif k == 'a':
            scene.range = scene.range * 1.5 
    elif scene.mouse.events:
        m = scene.mouse.getevent()
        if m.drag == 'middle':
            zoom = True
            lasty = m.pos.y
        elif m.drop == 'middle':
            zoom = False
        elif m.drag == 'left':
            spin = True
            lastray = scene.mouse.ray
        elif m.drop == 'left':
            spin = False
    elif zoom:
        newy = scene.mouse.pos.y
        if newy != lasty:
            distance = (scene.center-scene.mouse.camera).mag
            scaling = 10**((lasty-newy)/distance)
            newrange = scaling*scene.range.y
            if rangemin < newrange < rangemax:
                scene.range = newrange
                lasty = scaling*newy
    elif spin:
        newray = scene.mouse.ray
        dray = newray-lastray
        right = scene.forward.cross(scene.up).norm() # unit vector to the right
        up = right.cross(scene.forward).norm() # unit vector upward
        anglex = -4*arcsin(dray.dot(right))
        newforward = vector(scene.forward)
        newforward = rotate(newforward, angle=anglex, axis=scene.up)
        newray = rotate(newray, angle=anglex, axis=scene.up)
        angley = 4*arcsin(dray.dot(up))
        maxangle = scene.up.diff_angle(newforward)
        if not (angley >= maxangle or angley <= maxangle-pi):
            newforward = rotate(newforward, angle=angley, axis=right)
            newray = rotate(newray, angle=angley, axis=right)
        scene.forward = newforward
        lastray = newray


# -------------------------------------------

    #base.pos = revForV(0,0,0)

    # UPDATE LEGS AND BASE
    updateLegsAndBase()


