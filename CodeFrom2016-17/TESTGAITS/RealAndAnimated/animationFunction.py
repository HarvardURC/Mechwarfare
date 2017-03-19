import time
import math
from threading import Thread
import threading
import numpy
import json
import os


import TESTGAITS.RealAndAnimated.settings as s
'''
import settings as s
'''

wfPath = "TESTGAITS/RealAndAnimated/p1"

x_negs = [(-1) ** ((leg)%3 > 0) for leg in range(4)]
y_negs = [(-1)** math.floor(leg/2) for leg in range(4)]


def makeRadian(angles):
    return [math.radians(angles[0]),math.radians(angles[1]), math.radians(angles[2])]

def getCurrentAngles(legNum):
            
    [servoHipAngle, servoKneeAngle, servoAnkleAngle] = [s.ServoPos[legNum - 1][0], s.ServoPos[legNum - 1][1], s.ServoPos[legNum - 1][2]] 

    idealHipAngle = servoHipAngle + s.IDEAL_SERVO_POSITIONS[legNum - 1][0] - s.HOME_LEG_POSITIONS[legNum - 1][0]
    idealKneeAngle = servoKneeAngle + s.IDEAL_SERVO_POSITIONS[legNum - 1][1] - s.HOME_LEG_POSITIONS[legNum - 1][1]
    idealAnkleAngle = servoAnkleAngle + s.IDEAL_SERVO_POSITIONS[legNum - 1][2] - s.HOME_LEG_POSITIONS[legNum - 1][2]
    
    return (idealHipAngle % 360, idealKneeAngle % 360, idealAnkleAngle % 360)


def getDisplacementFromAngles(legNum, currentAngles):
    currentAngles = makeRadian(currentAngles)
    x = (s.HIPHORIZ_LENGTH + s.L1_LENGTH * math.cos(currentAngles[1]) + s.L2_LENGTH * math.cos(currentAngles[1] + currentAngles[2])) * math.cos(currentAngles[0])
    y = (s.HIPHORIZ_LENGTH + s.L1_LENGTH * math.cos(currentAngles[1]) + s.L2_LENGTH * math.cos(currentAngles[1] + currentAngles[2])) * math.sin(currentAngles[0])
    z = s.HIPVERTUP_LENGTH + s.L1_LENGTH * math.sin(currentAngles[1]) + s.L2_LENGTH * math.sin(currentAngles[1] + currentAngles[2])
    return [x,y,z]


def rotateVector(vector, theta):
    a = vector[0]
    b = vector[1]
    L = (a**2.0 + b ** 2.0) ** 0.5
    alpha = math.atan2(b,a)

    return [L * math.cos(alpha + theta), L * math.sin(alpha + theta), vector[2]]

def updateTurretServosAndTurret():

    storeTurretPos = s.TurretPos
    storeGoalPos = s.turretServoGoalPos

    # iterate once for pan and once for tilt
    for i in range(2):
        currentPos = storeTurretPos[i]
        goalPos = storeGoalPos[i]

        # check if servo needs changing
        if abs(goalPos - currentPos) > 0.0:
            difference = goalPos - currentPos
            animationServoDelta = s.ANIMATED_TURRET_SERVO_SPEED[i] * s.SERVO_UPDATE_DELAY

            # if difference is smaller than delta, then just make servo what it should be
            if abs(difference) < animationServoDelta:
                s.TurretPos[i] = s.turretServoGoalPos[i]
            else:
                # else move servoPos closer to goal servo position
                s.TurretPos[i] = s.TurretPos[i] + animationServoDelta * numpy.sign(difference)



def updateServosAndBase():
    while True:
        time.sleep(s.SERVO_UPDATE_DELAY)


        storeLegPos = list(s.ServoPos)
        storeGoalPos = list(s.servoGoalPos)

        oldBaseLocation = list(s.BasePos)
        oldLegDisplacements = [getDisplacementFromAngles(leg, getCurrentAngles(leg)) for leg in range(1,5)]

        xs = [oldLegDisplacements[leg][0] for leg in range(4)]
        ys = [oldLegDisplacements[leg][1] for leg in range(4)]

        oldLegThetas = [math.atan2(ys[leg] + y_negs[leg] * (s.BASE_LENGTH/2.0), xs[leg] + x_negs[leg] * (s.BASE_WIDTH/2.0)) for leg in range(4)]

        for leg in range(4):

            # turn dragging off if leg is done
            if (s.ServoPos[leg] == s.servoGoalPos[leg]):
                s.draggingLegs[leg] = 0

            for servo in range(3):
                currentPos = storeLegPos[leg][servo] 
                goalPos = storeGoalPos[leg][servo]

                # check if servo needs changing
                if abs(goalPos - currentPos) > 0.0:
                    difference = goalPos - currentPos
                    animationServoDelta = s.ANIMATED_LEG_SERVO_SPEED * s.SERVO_UPDATE_DELAY

                    # if difference is smaller than delta, then just make servo what it should be
                    if abs(difference) < animationServoDelta:
                        s.ServoPos[leg][servo] = s.servoGoalPos[leg][servo]
                    else:
                        # else move servoPos closer to goal servo position
                        s.ServoPos[leg][servo] = s.ServoPos[leg][servo] + animationServoDelta * numpy.sign(difference)

        storedDraggingLegs = list(s.draggingLegs)

        # if legs are dragging
        if sum(storedDraggingLegs) >= 1:
            
            #  for base position calculations
            newLegDisplacements = [getDisplacementFromAngles(leg, getCurrentAngles(leg)) for leg in range(1,5)]

            '''
            print "OLD THEN NEW: "
            print "old: ", oldLegDisplacements
            print "new: ", newLegDisplacements
            '''

            BaseDisplacements = numpy.subtract(oldLegDisplacements,newLegDisplacements)
            AvgBaseDisplacement = numpy.array([BaseDisplacements[leg] for leg in range(4) if storedDraggingLegs[leg] == 1]).sum(axis=0)/float(sum(storedDraggingLegs))
            
            '''
            print "diff: ", BaseDisplacements
            print "AVG: ",AvgBaseDisplacement
            print ""
            '''

            # base displacement, accounting for BaseAngle (base orientation)
            AvgBaseDisplacement[2] = 0.0

            rotatedDisplacement = rotateVector(AvgBaseDisplacement, s.BaseOrientationAngle)

            # change base position
            s.BasePos = list(numpy.add(oldBaseLocation,rotatedDisplacement))


            # for base orientation calculations

            xs = [newLegDisplacements[leg][0] for leg in range(4)]
            ys = [newLegDisplacements[leg][1] for leg in range(4)]
            newLegThetas = [math.atan2(ys[leg] + y_negs[leg] * (s.BASE_LENGTH/2.0), xs[leg] + x_negs[leg] * (s.BASE_WIDTH/2.0)) for leg in range(4)]

            baseThetaDisplacements = numpy.subtract(oldLegThetas,newLegThetas)

            # get average theta
            avgThetaDisplacement = sum([baseThetaDisplacements[leg] for leg in range(4) if storedDraggingLegs[leg] == 1])/float(sum(storedDraggingLegs))

            # update s.BaseOrientationAngle
            s.BaseOrientationAngle = s.BaseOrientationAngle + avgThetaDisplacement

        

        stringServoPositions = ""
        for leg in range(4):
            for servo in range(3):
                stringServoPositions = stringServoPositions + str(float(s.ServoPos[leg][servo])) + ";"
        for i in range(3):
            stringServoPositions = stringServoPositions + str(float(s.BasePos[i])) + ";"
        stringServoPositions = stringServoPositions + str(float(s.BaseOrientationAngle)) + ";" + str(float(s.TurretPos[0])) + ";" + str(float(s.TurretPos[1])) + ";"
        stringServoPositions = stringServoPositions + str(float(s.isFiring)) + ";"
        #print ("sending: ", stringServoPositions)

        # send data over pipe

        wp = open(wfPath, 'w')
        wp.write(stringServoPositions)
        wp.close()

        #print (s.BasePos, s.BaseOrientationAngle)

        # then update turret
        updateTurretServosAndTurret()

        


