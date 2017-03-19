import settings2 as s
from visual import *
import time
import math
from threading import Thread
import threading
import numpy
import json
import random
import math

import os


# helper functions
def vectorAdd(tuple1, tuple2):
	return tuple(map(lambda x, y: x + y, tuple1, tuple2))

def revForV(tuple):
	return (tuple[0], tuple[2], -tuple[1])


# define floor and base
floor = box (pos=revForV((0,0,0)), length=50, height=0.1, width=100, color=color.white)
base = box (pos=revForV((0,0,-s.HOMEPOS_FOOTHEIGHT + s.BASE_THICKNESS/2.0 + s.FOOT_RADIUS)), length=s.BASE_LENGTH, height= s.BASE_THICKNESS, width=s.BASE_WIDTH, color=color.red, axis=revForV((1,0,0)))

panBox = box (pos = numpy.add(base.pos, revForV([0,0, s.PANBOX_HEIGHT/2.0])), length=s.PANBOX_LENGTH, width=s.PANBOX_WIDTH, height= s.PANBOX_HEIGHT, color=color.green, axis=revForV((1,0,0)))
barrel = cylinder(pos=numpy.add(panBox.pos, revForV([0,0, s.PANBOX_HEIGHT/2.0])),  axis=(1,0,0), length = s.BARREL_LENGTH, radius=.1, color= color.white)
directionArrow = arrow(pos=(0,0,1.0), axis=revForV((0,0,2.0)), shaftwidth=.3, color=color.black)


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
    [servoHipAngle, servoKneeAngle, servoAnkleAngle] = [s.ServoPos[legNum - 1][0], s.ServoPos[legNum - 1][1], s.ServoPos[legNum - 1][2]] 

    idealHipAngle = servoHipAngle + s.IDEAL_SERVO_POSITIONS[legNum - 1][0] - s.HOME_LEG_POSITIONS[legNum - 1][0]
    idealKneeAngle = servoKneeAngle + s.IDEAL_SERVO_POSITIONS[legNum - 1][1] - s.HOME_LEG_POSITIONS[legNum - 1][1]
    idealAnkleAngle = servoAnkleAngle + s.IDEAL_SERVO_POSITIONS[legNum - 1][2] - s.HOME_LEG_POSITIONS[legNum - 1][2]
    
    return (idealHipAngle % 360, idealKneeAngle % 360, idealAnkleAngle % 360)

def rotateVector(vector, theta):
    a = vector[0]
    b = vector[1]
    L = (a**2.0 + b ** 2.0) ** 0.5
    alpha = math.atan2(b,a)

    return [L * math.cos(alpha + theta), L * math.sin(alpha + theta), vector[2]]

def updateLegsAndBase():

    # get ideal angles in radian for the visual arrows to update
    ServoPosRadian = [makeRadian(getCurrentAngles(1)),makeRadian(getCurrentAngles(2)),makeRadian(getCurrentAngles(3)),makeRadian(getCurrentAngles(4))]
    # loop through all legs
    for i in range(1,5):
        x_neg = (-1) ** ((i - 1)%3 > 0)
        y_neg = (-1)** math.floor(i/3)

        leg = str(i)

        legs['leg'+leg]['vert'].pos = vectorAdd(base.pos,revForV(rotateVector((x_neg * s.BASE_LENGTH/2.0,y_neg * s.BASE_WIDTH/2.0,-s.BASE_THICKNESS/2.0), s.BaseOrientationAngle)))
        legs['leg'+leg]['vert'].axis = revForV((0,0,s.HIPVERTUP_LENGTH))
        legs['leg'+leg]['horiz'].pos = vectorAdd(legs['leg'+leg]['vert'].pos,legs['leg'+leg]['vert'].axis)
        legs['leg'+leg]['horiz'].axis = revForV(rotateVector((s.HIPHORIZ_LENGTH*cos(ServoPosRadian[i - 1][0]),s.HIPHORIZ_LENGTH*sin(ServoPosRadian[i - 1][0]),0), s.BaseOrientationAngle))
        legs['leg'+leg]['knee2ankle'].pos = vectorAdd(legs['leg'+leg]['horiz'].pos,legs['leg'+leg]['horiz'].axis)
        legs['leg'+leg]['knee2ankle'].axis = revForV(rotateVector((s.L1_LENGTH*cos(ServoPosRadian[i - 1][1])*cos(ServoPosRadian[i - 1][0]),s.L1_LENGTH*cos(ServoPosRadian[i - 1][1])*sin(ServoPosRadian[i - 1][0]),s.L1_LENGTH*sin(ServoPosRadian[i - 1][1])), s.BaseOrientationAngle))
        legs['leg'+leg]['ankle2foot'].pos = vectorAdd(legs['leg'+leg]['knee2ankle'].pos,legs['leg'+leg]['knee2ankle'].axis)
        legs['leg'+leg]['ankle2foot'].axis = revForV(rotateVector((s.L2_LENGTH*cos(ServoPosRadian[i - 1][2])*cos(ServoPosRadian[i - 1][0]),s.L2_LENGTH*cos(ServoPosRadian[i - 1][2])*sin(ServoPosRadian[i - 1][0]),s.L2_LENGTH*sin(ServoPosRadian[i - 1][2])), s.BaseOrientationAngle))

        legs['leg'+leg]['foot'].pos = vectorAdd(legs['leg'+leg]['ankle2foot'].pos,legs['leg'+leg]['ankle2foot'].axis)

        #if i == 1:
           # print (legs['leg'+leg]['foot'].pos)

    base.pos = revForV(s.BasePos)
    base.axis =revForV((math.cos(s.BaseOrientationAngle),math.sin(s.BaseOrientationAngle),0))
    base.length = s.BASE_LENGTH

    TurretPosRadians = [math.radians(s.TurretPos[0]), math.radians(s.TurretPos[1])]
    panBox.axis = revForV((math.cos(s.BaseOrientationAngle + TurretPosRadians[0]),math.sin(s.BaseOrientationAngle + TurretPosRadians[0]),0))
    panBox.pos = numpy.add(base.pos, revForV([0,0,s.PANBOX_HEIGHT/2.0]))
    panBox.length = s.PANBOX_LENGTH


    barrel.pos = numpy.add(panBox.pos, revForV([0,0,s.PANBOX_HEIGHT/2.0]))
    tiltAngle = TurretPosRadians[1]/s.TURRET_GEAR_RATIO
    barrel.axis = revForV((math.cos(tiltAngle) * math.cos(s.BaseOrientationAngle + TurretPosRadians[0] + math.pi/2.0),math.cos(tiltAngle) * math.sin(s.BaseOrientationAngle + TurretPosRadians[0] + + math.pi/2.0), math.sin(tiltAngle)))
    barrel.length = s.BARREL_LENGTH
    if s.isFiring:
        barrel.color = color.red
    else:
        barrel.color = color.white

    directionArrow.pos = [base.pos[0], base.pos[1], base.pos[2] + s.BASE_THICKNESS]
    directionArrow.axis = revForV((math.cos(s.BaseOrientationAngle + math.pi/2.0),math.sin(s.BaseOrientationAngle + math.pi/2.0),0))
    directionArrow.length = s.BASE_LENGTH
        


#updateLegsAndBase()



def readPipe():
    rfPath = "./p1"
    try:
        os.mkfifo(rfPath)
    except OSError:
        pass
    while True:
        rp = open(rfPath, 'r')
        response = rp.read()
        rp.close()
        
        

        arr = response.split(';')
        
        #print ("received", arr)

        if len(arr) > 18:
            for leg in range(4):
                for servo in range(3):
                    s.ServoPos[leg][servo] = float(arr[leg*3 + servo])
            for i in range(3):
                s.BasePos[i] = float(arr[12 + i])

            s.BaseOrientationAngle = float(arr[15])
            s.TurretPos[0] = float(arr[16])
            s.TurretPos[1] = float(arr[17])
            s.isFiring = float(arr[18])
        

readPipeThread = Thread(target=readPipe, args=())
readPipeThread.start()



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


# I copied this code that allows the visualizer to be rotated and zoomed in, using a mouse.
scene.userzoom = False
scene.userspin = False
scene.range = 15

rangemin = .5
rangemax = 40

zoom = False
spin = False


    
scene.forward = revForV([-0.0,1.0,-1.0])

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
        print scene.forward
        lastray = newray


# -------------------------------------------

    #base.pos = revForV(0,0,0)

    # UPDATE LEGS AND BASE
    updateLegsAndBase()



