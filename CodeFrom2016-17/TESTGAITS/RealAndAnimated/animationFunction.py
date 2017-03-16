import time
import math
from threading import Thread
import threading
import numpy


import walking as w
import settings as s


x_negs = [(-1) ** ((leg)%3 > 0) for leg in range(4)]
y_negs = [(-1)** (leg/2) for leg in range(4)]



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
        if abs(goalPos - currentPos) > 0.1:
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
        oldLegDisplacements = [w.getDisplacementFromAngles(leg, w.getCurrentAngles(leg)) for leg in range(1,5)]

        xs = [oldLegDisplacements[leg][0] for leg in range(4)]
        ys = [oldLegDisplacements[leg][1] for leg in range(4)]
        oldLegThetas = [math.atan2(ys[leg] + y_negs[leg] * (s.BASE_LENGTH/2.0), xs[leg] + x_negs[leg] * (s.BASE_WIDTH/2.0)) for leg in range(4)]

        for leg in range(4):

            # turn dragging off if leg is done
            if (s.ServoPos[leg] == s.servoGoalPos[leg]):

                s.draggingLegs[leg] = False

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
            newLegDisplacements = [w.getDisplacementFromAngles(leg, w.getCurrentAngles(leg)) for leg in range(1,5)]

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
            s.BasePos = numpy.add(oldBaseLocation,rotatedDisplacement)


            
            # for base orientation calculations

            xs = [newLegDisplacements[leg][0] for leg in range(4)]
            ys = [newLegDisplacements[leg][1] for leg in range(4)]
            newLegThetas = [math.atan2(ys[leg] + y_negs[leg] * (s.BASE_LENGTH/2.0), xs[leg] + x_negs[leg] * (s.BASE_WIDTH/2.0)) for leg in range(4)]

            baseThetaDisplacements = numpy.subtract(oldLegThetas,newLegThetas)

            # get average theta
            avgThetaDisplacement = sum([baseThetaDisplacements[leg] for leg in range(4) if storedDraggingLegs[leg] == 1])/float(sum(storedDraggingLegs))

            # update s.BaseOrientationAngle
            s.BaseOrientationAngle = s.BaseOrientationAngle + avgThetaDisplacement

        # then update turret
        updateTurretServosAndTurret()



