import numpy
import math
import time
from threading import Thread
import threading


from . import animationFunction as aF
from . import settings as s



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
        'turret': ['pan', 'tilt']
        
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
    }
}


def checkServoBounds(legNum, servoAngles):
    names = ["Hip", "Knee", "Ankle"]
    for i in range(len(servoAngles)):
        home = s.HOME_LEG_POSITIONS[legNum - 1][i]
        if (servoAngles[i] > home + s.SERVO_BOUNDS[i][1]) or (servoAngles[i] < home + s.SERVO_BOUNDS[i][0]):
            raise ValueError(names[i] + ' servo out of range. Requested position was ' + str(servoAngles[i]) + ' but range is ' + str(home + s.SERVO_BOUNDS[i][0]) + ' to ' + str(home + s.SERVO_BOUNDS[i][1]) + ' - Will')


def getServoAnglesFromIdeals(legNum, idealHipAngle, idealKneeAngle, idealAnkleAngle):
    conversion = servoHipAngle = idealHipAngle - s.IDEAL_SERVO_POSITIONS[legNum - 1][0] + s.HOME_LEG_POSITIONS[legNum - 1][0]
    if legNum == 1:
        if idealHipAngle > 270:
            servoHipAngle = -360 + conversion
        else:
            servoHipAngle = conversion
    elif legNum == 2 or legNum == 3:
        servoHipAngle = conversion
    elif legNum == 4:
        if idealHipAngle < 90:
            servoHipAngle = conversion + 360
        else:
            servoHipAngle = conversion


    # these are always the same.
    servoKneeAngle = idealKneeAngle - s.IDEAL_SERVO_POSITIONS[legNum - 1][1] + s.HOME_LEG_POSITIONS[legNum - 1][1]
    servoAnkleAngle = idealAnkleAngle - s.IDEAL_SERVO_POSITIONS[legNum - 1][2] + s.HOME_LEG_POSITIONS[legNum - 1][2]

    # Since we made IK return only positive values, if the angle is greater than 180 for an ankle or knee position
    # it means that a negative value was used
    if servoKneeAngle > 180:
        servoKneeAngle = servoKneeAngle - 360
    if servoAnkleAngle > 180:
        servoAnkleAngle = servoAnkleAngle - 360

    servoAngles = [servoHipAngle, servoKneeAngle, servoAnkleAngle]
    return servoAngles




# takes in angles that servos should move, and moves them according to positions they should be in
def moveServos(legNum, idealHipAngle, idealKneeAngle, idealAnkleAngle, isMoving):

    servoAngles = getServoAnglesFromIdeals(legNum, idealHipAngle, idealKneeAngle, idealAnkleAngle)

    checkServoBounds(legNum, servoAngles)

    if s.isAnimation:
        # made int of boolean because json files use false instead of False, so we're using 0 and 1 for booleans
        s.draggingLegs[legNum - 1] = int(not isMoving)
        s.servoGoalPos[legNum - 1] = servoAngles

    else:
        #print "ideals: ", (idealHipAngle, idealKneeAngle, idealAnkleAngle)
        #print "actuals: ", (servoAngles[0], servoAngles[1], servoAngles[2])

        getattr(robot,"hip" + str(legNum)).goal_position = servoAngles[0]
        getattr(robot,"knee" + str(legNum)).goal_position = servoAngles[1]
        getattr(robot,"ankle" + str(legNum)).goal_position = servoAngles[2]
        

# takes in legnum and returns the servo positions in the ideal frame
def getCurrentAngles(legNum):

    if s.isAnimation:
        [servoHipAngle, servoKneeAngle, servoAnkleAngle] = [s.ServoPos[legNum - 1][0], s.ServoPos[legNum - 1][1], s.ServoPos[legNum - 1][2]] 
    else:
        servoHipAngle = getattr(robot,"hip" + str(legNum)).present_position
        servoKneeAngle = getattr(robot,"knee" + str(legNum)).present_position
        servoAnkleAngle = getattr(robot,"ankle" + str(legNum)).present_position

    idealHipAngle = servoHipAngle + s.IDEAL_SERVO_POSITIONS[legNum - 1][0] - s.HOME_LEG_POSITIONS[legNum - 1][0]
    idealKneeAngle = servoKneeAngle + s.IDEAL_SERVO_POSITIONS[legNum - 1][1] - s.HOME_LEG_POSITIONS[legNum - 1][1]
    idealAnkleAngle = servoAnkleAngle + s.IDEAL_SERVO_POSITIONS[legNum - 1][2] - s.HOME_LEG_POSITIONS[legNum - 1][2]
    
    return (idealHipAngle % 360, idealKneeAngle % 360, idealAnkleAngle % 360)

    

def makeRadian(angles):
    return [math.radians(angles[0]),math.radians(angles[1]), math.radians(angles[2])]

# takes in the x, y, and z displacement from
def getIKAnglesFromDisplacement(legNum, x,y,z):

    # these define the new x and new z values used for the 2DOF IK calculation
    new_x = ((x**2.0 + y**2.0)**.5) - s.HIPHORIZ_LENGTH
    new_z = -s.HIPVERTUP_LENGTH + z
    cosAnkleAngle = (new_x**2.0 + new_z**2.0 - s.L1_LENGTH**2.0 - s.L2_LENGTH**2.0)/(2.0*s.L1_LENGTH*s.L2_LENGTH)

    if abs(cosAnkleAngle) > 1.0:
        raise ValueError('Displacement out of range of servos - Will')

    # get leg joint angles
    ankleAngle = math.atan2(-1 * (1.0 - cosAnkleAngle**2)**.5, cosAnkleAngle)
    kneeAngle = math.atan2(new_z,new_x) - math.atan2(s.L2_LENGTH*math.sin(ankleAngle), s.L1_LENGTH + s.L2_LENGTH*math.cos(ankleAngle))
    hipAngle = math.atan2(y,x)

    # returns mod version of angle, which means it will always be positive from 0 to 360
    return [math.degrees(hipAngle) % 360, math.degrees(kneeAngle) % 360, math.degrees(ankleAngle) % 360]

def getDisplacementFromAngles(legNum, currentAngles):
    currentAngles = makeRadian(currentAngles)
    x = (s.HIPHORIZ_LENGTH + s.L1_LENGTH * math.cos(currentAngles[1]) + s.L2_LENGTH * math.cos(currentAngles[1] + currentAngles[2])) * math.cos(currentAngles[0])
    y = (s.HIPHORIZ_LENGTH + s.L1_LENGTH * math.cos(currentAngles[1]) + s.L2_LENGTH * math.cos(currentAngles[1] + currentAngles[2])) * math.sin(currentAngles[0])
    z = s.HIPVERTUP_LENGTH + s.L1_LENGTH * math.sin(currentAngles[1]) + s.L2_LENGTH * math.sin(currentAngles[1] + currentAngles[2])
    return [x,y,z]

# moves foot by lifting it
def moveFoot(legNum, newDispVector):
    currentAngles = getCurrentAngles(legNum)

    currentDispVector = getDisplacementFromAngles(legNum, currentAngles)
    print("currentDispVector: ", currentDispVector)

    [x,y,z] = currentDispVector + .5 * numpy.subtract(newDispVector, currentDispVector)

    z = z + s.LIFTFOOTHEIGHT

    print ("halfxyz:", x,y,z)
    newAngles = getIKAnglesFromDisplacement(legNum, x, y, z)

    moveServos(legNum, newAngles[0], newAngles[1], newAngles[2], 1)

    time.sleep(s.STEP_DELAY)

    [x,y,z] = newDispVector

    newAngles = getIKAnglesFromDisplacement(legNum, x, y, z)

    moveServos(legNum, newAngles[0], newAngles[1], newAngles[2], 1)

    time.sleep(s.STEP_DELAY)




# moves body by dragging foot
def dragFoot(legNum, newDispVector):
    currentAngles = getCurrentAngles(legNum)

    currentDispVector = getDisplacementFromAngles(legNum, currentAngles)

    z = currentDispVector[2]
    for i in range(s.DRAG_INTERVALS):

        # get xyz finds position the foot should be in at time t in the path from currentDispVector to newDispVector
        x = currentDispVector[0] + (i + 1)*(newDispVector[0] - currentDispVector[0])/s.DRAG_INTERVALS
        y = currentDispVector[1] + (i + 1)*(newDispVector[1] - currentDispVector[1])/s.DRAG_INTERVALS
        z = currentDispVector[2] + (i + 1)*(newDispVector[2] - currentDispVector[2])/s.DRAG_INTERVALS

        newAngles = getIKAnglesFromDisplacement(legNum, x,y,z)

        moveServos(legNum, newAngles[0], newAngles[1], newAngles[2], 0)

        time.sleep(.5)


# this one is a generalized version of the others. Dragging is discretized only into two
# because it matches with the two discretizations of the move foot
def moveAndDragMultFeet(legNums, newDispVectors, isMovings):
    print ("moving to: ", newDispVectors, "...")

    # find current displacement vectors at beginning
    currentDispVectors = []
    for l in range(len(legNums)):
        legNum = legNums[l]
        currentAngles = getCurrentAngles(legNum)
        currentDispVectors.append(getDisplacementFromAngles(legNum, currentAngles))

    # take multiple steps up at the same time and half drag
    for l in range(len(legNums)):
        legNum = legNums[l]
        newDispVector = newDispVectors[l]
        currentDispVector = currentDispVectors[l]

        # if this command is for stepping foot
        if isMovings[l]:
            [x,y,z] = currentDispVector + .5 * numpy.subtract(newDispVector, currentDispVector)
            z = z + s.LIFTFOOTHEIGHT

        # else its for dragging foot
        else:
            # get xyz of half drag in the path from currentDispVector to newDispVector
            [x,y,z] = currentDispVector + .5 * numpy.subtract(newDispVector, currentDispVector)

        newAngles = getIKAnglesFromDisplacement(legNum, x,y,z)

        moveServos(legNum, newAngles[0], newAngles[1], newAngles[2], isMovings[l])

    time.sleep(s.STEP_DELAY)

    # put multiple foots down and finish drag
    for l in range(len(legNums)):
        legNum = legNums[l]
        newDispVector = newDispVectors[l]

        if isMovings[l]:
            [x,y,z] = newDispVector
        else:
            [x,y,z] = newDispVector


        newAngles = getIKAnglesFromDisplacement(legNum, x,y,z)

        moveServos(legNum, newAngles[0], newAngles[1], newAngles[2], isMovings[l])

    time.sleep(s.STEP_DELAY)

# moves two legs at a time to get back from home position. Should work without problem as long as robot
# is reasonably balanced when this is called
def goToHomeFromAnyPosition():
    changeServoSpeeds(s.MAX_SERVO_SPEED)
    moveAndDragMultFeet([1, 3],  [s.HOMEPOS["1"], s.HOMEPOS["3"]],[1,1])
    moveAndDragMultFeet([2, 4],  [s.HOMEPOS["2"], s.HOMEPOS["4"]], [1,1])


# if no motors are specified then changes all leg motors. Else it changes the motors in the list given.
# takes a list of strings like ["pan", "tilt"] as second argument
def changeServoSpeeds(speed, motors = None):
    # in the animated version you could either change all leg servos at same time or pan or tilt servo
    if (s.isAnimation):
        if (motors == None):
            s.ANIMATED_LEG_SERVO_SPEED = speed
        else:
            for name in motors:
                if name == 'pan':
                    s.ANIMATED_TURRET_SERVO_SPEED[0] = speed
                elif name == 'tilt':
                    s.ANIMATED_TURRET_SERVO_SPEED[1] = speed

    # real version has more options because you could input any motors for the motors parameter
    else:
        if (motors == None):
            for m in robot.motors:
                # only change leg motor speed
                if ((m.name != 'tilt') and (m.name != 'pan')):
                    m.moving_speed = speed
        else:
            for m in motors:
                getattr(robot,m).moving_speed = speed



# direction must be either F, B, L, or R. numSteps is the number of steps, obvs.
def walkingForward(direction, numSteps, stepSize, speed = None):
    if (speed != None):
        changeServoSpeeds(speed)

    if (direction == 'F'):
        y = -stepSize
        x = 0
    elif (direction == 'B'):
        y = stepSize
        x = 0
    elif (direction == 'L'):
        y = 0
        x = stepSize
    elif (direction == 'R'):
        y = 0
        x = -stepSize
    else:
        print ("You must choose either F, B, L, or R")

    for iterations in range(numSteps):
        newDispVectors = [numpy.add(s.HOMEPOS["1"], [x,y,0]), numpy.add(s.HOMEPOS["3"], [x,y,0]), numpy.add(s.HOMEPOS["2"], [-x,-y,0]), numpy.add(s.HOMEPOS["4"], [-x,-y,0])]
        moveAndDragMultFeet([1, 3, 2, 4], newDispVectors, [0,0,1,1])

        newDispVectors = [numpy.add(s.HOMEPOS["1"], [-x,-y,0]), numpy.add(s.HOMEPOS["3"], [-x,-y,0]), numpy.add(s.HOMEPOS["2"], [x,y,0]), numpy.add(s.HOMEPOS["4"], [x,y,0])]
        moveAndDragMultFeet([1, 3, 2, 4], newDispVectors, [1,1,0,0])

    #goToHomeFromAnyPosition()

def relHomPos(legNum, displacement):
    return numpy.add(s.HOMEPOS[str(legNum)], displacement)

def creep(direction, numSteps, stepSize, speed = None):
    if (speed != None):
        changeServoSpeeds(speed)

    if (direction == 'F'):
        feetOrder = [1, 2, 3, 4]
        y = -stepSize
        x = 0
    elif (direction == 'B'):
        feetOrder = [3,4,1,2]
        y = stepSize
        x = 0
    elif (direction == 'L'):
        feetOrder = [2,3,4,1]
        y = 0
        x = stepSize
    elif (direction == 'R'):
        feetOrder = [4,1,2,3]
        y = 0
        x = -stepSize
    else:
        print ("You must choose either F, B, L, or R")

    newDispVectors = [relHomPos(feetOrder[0],[x,y,0]), relHomPos(feetOrder[3],[-x,-y,0])]
    moveAndDragMultFeet([feetOrder[0], feetOrder[3]], newDispVectors, [1,1])

    
    for iterations in range(numSteps):
        
        moveAndDragMultFeet([feetOrder[0]], [relHomPos(feetOrder[0],[-x,-y,0])], [1])
        newDispVectors = [relHomPos(feetOrder[0],[0,0,0]), relHomPos(feetOrder[1],[x,y,0]), relHomPos(feetOrder[2],[x,y,0]), relHomPos(feetOrder[3],[0,0,0])]
        moveAndDragMultFeet([feetOrder[0], feetOrder[1], feetOrder[2], feetOrder[3]], newDispVectors, [0,0,0,0])
        moveAndDragMultFeet([feetOrder[2]], [relHomPos(feetOrder[2],[-x,-y,0])], [1])

        
        moveAndDragMultFeet([feetOrder[1]], [relHomPos(feetOrder[1],[-x,-y,0])], [1])
        newDispVectors = [relHomPos(feetOrder[0],[x,y,0]), relHomPos(feetOrder[1],[0,0,0]), relHomPos(feetOrder[2],[0,0,0]), relHomPos(feetOrder[3],[x,y,0])]
        moveAndDragMultFeet([feetOrder[0], feetOrder[1], feetOrder[2], feetOrder[3]], newDispVectors, [0,0,0,0])
        moveAndDragMultFeet([feetOrder[3]], [relHomPos(feetOrder[3],[-x,-y,0])], [1])
        


def rotate(degree, isClockwise, speed = None):
    if (speed != None):
        changeServoSpeeds(speed)

    direction = 1
    if isClockwise:
        direction = -1 
        
    legRadius = (s.HOMEPOS["1"][0] **2.0 + s.HOMEPOS["1"][1] **2.0)**.5
    circleRadius = ((s.BASE_WIDTH/2.0)**2.0 + (s.BASE_LENGTH/2.0)**2.0)**.5 + legRadius
    x = circleRadius * math.cos(math.radians(45.0 + direction * degree)) - (s.BASE_WIDTH/2.0) - s.HOMEPOS["1"][0]
    y = circleRadius * math.sin(math.radians(45.0 + direction * degree)) - (s.BASE_WIDTH/2.0) - s.HOMEPOS["1"][1]

    #moveAndDragMultFeet([1, 3], [numpy.add(s.HOMEPOS["1"], [x,y,0]), numpy.add(s.HOMEPOS["3"], [-x,-y,0])], [1,1])
    moveAndDragMultFeet([1,3,2, 4], [s.HOMEPOS["1"], s.HOMEPOS["3"], numpy.add(s.HOMEPOS["2"], [-y,x,0]), numpy.add(s.HOMEPOS["4"], [y,-x,0])], [0,0,1,1])
    moveAndDragMultFeet([1,3,2, 4], [numpy.add(s.HOMEPOS["1"], [x,y,0]), numpy.add(s.HOMEPOS["3"], [-x,-y,0]), s.HOMEPOS["2"], s.HOMEPOS["4"]], [1,1,0,0])
    #moveAndDragMultFeet([1, 3, 2, 4], [s.HOMEPOS["1"], s.HOMEPOS["3"], s.HOMEPOS["2"], s.HOMEPOS["4"]], [0,0,0,0])


def moveTurretServo(m,x):
    names = ["pan", "tilt"]
    getattr(robot,names[m]).compliant = False
    if (x > s.TURRET_SERVO_BOUNDS[m][1] or x < s.TURRET_SERVO_BOUNDS[m][0]):
        print(names[m] + ' servo out of range. Requested position was ' + str(x) + ' but range is ' + str(s.TURRET_SERVO_BOUNDS[m][0]) + ' to ' + str(s.TURRET_SERVO_BOUNDS[m][1]) + ' - Baby Mech has declared')
        current = getTurretServoAngle(m)
        if s.isAnimation:
            s.turretServoGoalPos[m] = x
        else:
            getattr(robot,names[m]).goal_position = current
    else:
        if s.isAnimation:
            s.turretServoGoalPos[m] = x
        else:
            getattr(robot,names[m]).goal_position = x
            
def stopTurretServo(m):
    names = ["pan", "tilt"]
    if s.isAnimation:
        s.turretServoGoalPos[m]
    else:
        getattr(robot,names[m]).compliant = True

def getTurretServoAngle(m):
    if s.isAnimation:
        return s.TurretPos[m]
    else:
        names = ["pan", "tilt"]
        return getattr(robot,names[m]).present_position

def getTurretBound(m,b):
    return s.TURRET_SERVO_BOUNDS[m][b]

def moveAgitatorServo(x):
    getattr(robot,"agitator").goal_position = x
            
# 1 for direction is clockwise, -1 is counterclockwise. degrees is number of degrees motor will change
def rotateTurretServo(m, degrees, isClockwise, speed = None):
    names = ["pan", "tilt"]
    if (speed != None):
        changeServoSpeeds(speed, [names[m]])

    direction = 1
    if isClockwise:
        direction = -1

    currentServoAngle = getTurretServoAngle(m)

    moveTurretServo(0,currentServoAngle + direction*degrees)


# initialize robot config if not animation
if s.isAnimation:
    # if we're in animation mode, then call the while loop in af that updates servo positions and other dependent variables
    servoThread = Thread(target=aF.updateServosAndBase, args=())
    servoThread.start()

else:
    import pypot.robot

    robot = pypot.robot.from_config(my_config)

    for m in robot.motors:
        m.moving_speed = 150
        m.compliant = False
        print(m.name, m.present_position)

    for i in range(4):
        print(i + 1, "currentangles: ", getCurrentAngles(i+1), "displacement: ", getDisplacementFromAngles(i+1,getCurrentAngles(i+1)))


    #robot.close()





                         
