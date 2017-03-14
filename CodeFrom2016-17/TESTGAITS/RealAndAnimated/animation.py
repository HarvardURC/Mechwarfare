from visual import *
import time
import math
from threading import Thread
import threading
import numpy

import walking as w
import settings as s


# helper functions
def vectorAdd(tuple1, tuple2):
	return tuple(map(lambda x, y: x + y, tuple1, tuple2))

def revForV(tuple):
	return (tuple[0], tuple[2], -tuple[1])



# define floor and base
floor = box (pos=revForV((0,0,0)), length=50, height=0.1, width=100, color=color.white)
base = box (pos=revForV((0,0,-s.HOMEPOS_FOOTHEIGHT + s.BASE_THICKNESS/2.0 + s.FOOT_RADIUS)), length=s.BASE_LENGTH, height= s.BASE_THICKNESS, width=s.BASE_WIDTH, color=color.red, axis=revForV((1,0,0)))




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

def updateLegsAndBase():

    # get ideal angles in radian for the visual arrows to update
    ServoPosRadian = [w.makeRadian(w.getCurrentAngles(1)),w.makeRadian(w.getCurrentAngles(2)),w.makeRadian(w.getCurrentAngles(3)),w.makeRadian(w.getCurrentAngles(4))]

    # loop through all legs
    for i in range(1,5):
        x_neg = (-1) ** ((i - 1)%3 > 0 )
        y_neg = (-1)** (i/3)
        leg = str(i)
        legs['leg'+leg]['vert'].pos = vectorAdd(base.pos,revForV((x_neg * s.BASE_LENGTH/2.0,y_neg * s.BASE_WIDTH/2.0,-s.BASE_THICKNESS/2.0)))
        legs['leg'+leg]['vert'].axis = revForV((0,0,s.HIPVERTUP_LENGTH))
        legs['leg'+leg]['horiz'].pos = vectorAdd(legs['leg'+leg]['vert'].pos,legs['leg'+leg]['vert'].axis)
        legs['leg'+leg]['horiz'].axis = revForV((s.HIPHORIZ_LENGTH*cos(ServoPosRadian[i - 1][0]),s.HIPHORIZ_LENGTH*sin(ServoPosRadian[i - 1][0]),0))
        legs['leg'+leg]['knee2ankle'].pos = vectorAdd(legs['leg'+leg]['horiz'].pos,legs['leg'+leg]['horiz'].axis)
        legs['leg'+leg]['knee2ankle'].axis = revForV((s.L1_LENGTH*cos(ServoPosRadian[i - 1][1])*cos(ServoPosRadian[i - 1][0]),s.L1_LENGTH*cos(ServoPosRadian[i - 1][1])*sin(ServoPosRadian[i - 1][0]),s.L1_LENGTH*sin(ServoPosRadian[i - 1][1])))
        legs['leg'+leg]['ankle2foot'].pos = vectorAdd(legs['leg'+leg]['knee2ankle'].pos,legs['leg'+leg]['knee2ankle'].axis)
        legs['leg'+leg]['ankle2foot'].axis = revForV((s.L2_LENGTH*cos(ServoPosRadian[i - 1][2])*cos(ServoPosRadian[i - 1][0]),s.L2_LENGTH*cos(ServoPosRadian[i - 1][2])*sin(ServoPosRadian[i - 1][0]),s.L2_LENGTH*sin(ServoPosRadian[i - 1][2])))

        legs['leg'+leg]['foot'].pos = vectorAdd(legs['leg'+leg]['ankle2foot'].pos,legs['leg'+leg]['ankle2foot'].axis)


# initialize time variable
s.t = 0
updateLegsAndBase()



# put here whatever function you want to call
def movementFun():
    w.walkingForward('L',3,1,100)
    #w.rotate(20, 1)
t1 = Thread(target=movementFun, args=())
t1.start()



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

    # increment time
    s.t += 1

    #base.pos = revForV(0,0,0)

    # UPDATE LEGS AND BASE
    updateLegsAndBase()



