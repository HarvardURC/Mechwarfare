import numpy

# Config code
my_config = {
    'controllers': {
        'my_dxl_controller': {
            'sync_read': False,
            'attached_motors': ['leg1'],
            'port': '/dev/ttyACM0'
        }
    },
    'motorgroups': {
        'leg1': ['hip3', 'knee3', 'ankle3'],
    },
    'motors': {
        'hip3': {
            'orientation': 'indirect',
            'type': 'AX-12',
            'id': 9,
            'angle_limit': [150.0, 300.0],
            'offset': -178.0
        },
        'knee3': {
            'orientation': 'indirect',
            'type': 'AX-12',
            'id': 8,
            'angle_limit': [-60.0, 90.0],
            'offset': 36.5
        },
        'ankle3': {
            'orientation': 'indirect',
            'type': 'AX-12',
            'id': 7,
            'angle_limit': [-90.0, 90.0],
            'offset': -53.2
        },
    }
}

# constants
HOMEPOS_FOOTHEIGHT = -2
HOMEPOS = {"1": [2,2,HOMEPOS_FOOTHEIGHT],
           "2": [-2,2, HOMEPOS_FOOTHEIGHT],
           "3": [-2,-2,HOMEPOS_FOOTHEIGHT],
           "4": [2,-2,HOMEPOS_FOOTHEIGHT]}


# static lengths from robot model
L1_LENGTH = 1.5
L2_LENGTH = 2.5
HIPHORIZ_LENGTH = 2.5
HIPVERTUP_LENGTH = 1.25
BASE_WIDTH = 5
#BASE_LENGTH = 

# variables for robot walk gait
DRAG_INTERVALS = 5
LIFTFOOTHEIGHT = 1

STEP_DELAY = .5


def makeRadian(angles):
    return [math.radians(angles[0]),math.radians(angles[1]), math.radians(angles[2])]

def getCurrentAngles(legNum):
    #return [legNum*30,(legNum + 2) * 30,(legNum + 4) * 30]
    return [0,-60,30]


# takes in the x, y, and z displacement from 
def getIKAnglesFromDisplacement(legNum, x,y,z):

    # these define the new x and new z values used for the 2DOF IK calculation
    new_x = ((x**2.0 + y**2.0)**.5) - HIPHORIZ_LENGTH
    new_z = -HIPVERTUP_LENGTH + z
    cosAnkleAngle = (new_x**2.0 + new_z**2.0 - L1_LENGTH**2.0 - L2_LENGTH**2.0)/(2.0*L1_LENGTH*L2_LENGTH)

    if abs(cosAnkleAngle) > 1.0:
        raise ValueError('Displacement out of range of servos - Will')

    # get leg joint angles
    ankleAngle = math.atan2(-1 * (1.0 - cosAnkleAngle**2)**.5, cosAnkleAngle)
    kneeAngle = math.atan2(new_z,new_x) - math.atan2(L2_LENGTH*math.sin(ankleAngle), L1_LENGTH + L2_LENGTH*math.cos(ankleAngle))
    hipAngle = math.atan2(y,x)

    return [math.degrees(hipAngle), math.degrees(kneeAngle), math.degrees(ankleAngle)]

def getDisplacementFromAngles(legNum, currentAngles):
    currentAngles = makeRadian(currentAngles)
    x = (HIPHORIZ_LENGTH + L1_LENGTH * math.cos(currentAngles[1]) + L2_LENGTH * math.cos(currentAngles[1] + currentAngles[2])) * math.cos(currentAngles[0])
    y = (HIPHORIZ_LENGTH + L1_LENGTH * math.cos(currentAngles[1]) + L2_LENGTH * math.cos(currentAngles[1] + currentAngles[2])) * math.sin(currentAngles[0])
    z = HIPVERTUP_LENGTH + L1_LENGTH * math.sin(currentAngles[1]) + L2_LENGTH * math.sin(currentAngles[1] + currentAngles[2])
    return [x,y,z]

# moves foot by lifting it
def moveFoot(legNum, newDispVector):
    currentAngles = getCurrentAngles(legNum)
    
    currentDispVector = getDisplacementFromAngles(legNum, currentAngles)

    [x,y,z] = currentDispVector + .5 * numpy.subtract(newDispVector, currentDispVector)

    z = z + LIFTFOOTHEIGHT

    newAngles = getIKAnglesFromDisplacement(legNum, x, y, z)

    print "current: ", currentDispVector, "destination: ", newDispVector

    print ('moveFoot() ', 'disp:', [x,y,z], 'angles:', newAngles)

    '''
    getattr(robot,"hip" + str(legNum)).goal_position = newAngles[0]
    getattr(robot,"knee" + str(legNum)).goal_position = newAngles[1]
    getattr(robot,"ankle" + str(legNum)).goal_position = newAngles[2]
    '''

    [x,y,z] = newDispVector

    newAngles = getIKAnglesFromDisplacement(legNum, x, y, z)

    print ('moveFoot() ', 'disp:', [x,y,z], 'angles:', newAngles)

    '''
    getattr(robot,"hip" + str(legNum)).goal_position = newAngles[0]
    getattr(robot,"knee" + str(legNum)).goal_position = newAngles[1]
    getattr(robot,"ankle" + str(legNum)).goal_position = newAngles[2]
    '''



# this will probably eventually replace the move foot function
def moveMultFeet(legNums, newDispVectors):

    # find current displacement vectors at beginning
    currentDispVectors = []
    for l in range(len(legNums)):
        legNum = legNums[l]
        currentAngles = getCurrentAngles(legNum)
        currentDispVectors.append(getDisplacementFromAngles(legNum, currentAngles))

    print "currentDispVectors: ", currentDispVectors, 'newDispVectors: ', newDispVectors

    # take multiple steps up at the same time
    for l in range(len(legNums)):
        legNum = legNums[l]
        newDispVector = newDispVectors[l]
        currentDispVector = currentDispVectors[l]

        [x,y,z] = currentDispVector + .5 * numpy.subtract(newDispVector, currentDispVector)
        z = z + LIFTFOOTHEIGHT

        newAngles = getIKAnglesFromDisplacement(legNum, x, y, z)

        print ('moveMultFeet() ', l, 'disp:', [x,y,z], 'angles:', newAngles)

        '''
        getattr(robot,"hip" + str(legNum)).goal_position = newAngles[0]
        getattr(robot,"knee" + str(legNum)).goal_position = newAngles[1]
        getattr(robot,"ankle" + str(legNum)).goal_position = newAngles[2]
        '''

    time.sleep(STEP_DELAY)
    print 'SECOND PART'
    # put multiple foots down
    for l in range(len(legNums)):
        legNum = legNums[l]
        [x,y,z] = newDispVectors[l]

        newAngles = getIKAnglesFromDisplacement(legNum, x, y, z)
        print ('moveMultFeet() ', l, 'disp:', [x,y,z], 'angles:', newAngles)
        '''
        getattr(robot,"hip" + str(legNum)).goal_position = newAngles[0]
        getattr(robot,"knee" + str(legNum)).goal_position = newAngles[1]
        getattr(robot,"ankle" + str(legNum)).goal_position = newAngles[2]
        '''

    time.sleep(1)

# moves body by dragging foot
def dragFoot(legNum, newDispVector):
    currentAngles = getCurrentAngles(legNum)

    currentDispVector = getDisplacementFromAngles(legNum, currentAngles)

    print "currentDispVector: ", currentDispVector, 'newDispVector: ', newDispVector

    z = currentDispVector[2]
    for i in range(DRAG_INTERVALS):

        # get xyz finds position the foot should be in at time t in the path from currentDispVector to newDispVector
        x = currentDispVector[0] + (i + 1)*(newDispVector[0] - currentDispVector[0])/DRAG_INTERVALS
        y = currentDispVector[1] + (i + 1)*(newDispVector[1] - currentDispVector[1])/DRAG_INTERVALS
        z = currentDispVector[2] + (i + 1)*(newDispVector[2] - currentDispVector[2])/DRAG_INTERVALS

        newAngles = getIKAnglesFromDisplacement(legNum, x,y,z)

        print ('dragFoot() ', 'disp:', [x,y,z], 'angles:', newAngles)

        '''
        getattr(robot,"hip" + str(legNum)).goal_position = newAngles[0]
        getattr(robot,"knee" + str(legNum)).goal_position = newAngles[1]
        getattr(robot,"ankle" + str(legNum)).goal_position = newAngles[2]
        '''

        time.sleep(.5)

def dragMultFeet(legNums, newDispVectors):
        
        # find current displacement vectors at beginning
        currentDispVectors = []
        for l in range(len(legNums)):
            legNum = legNums[l]
            currentAngles = getCurrentAngles(legNum)
            currentDispVectors.append(getDisplacementFromAngles(legNum, currentAngles))

        print "currentDispVectors: ", currentDispVectors, 'newDispVectors: ', newDispVectors

        # drag all feet at same rate
        for i in range(DRAG_INTERVALS):

            for l in range(len(legNums)):
                legNum = legNums[l]
                newDispVector = newDispVectors[l]
                currentDispVector = currentDispVectors[l]

                # get xyz finds position the foot should be in at time t in the path from currentDispVector to newDispVector
                x = currentDispVector[0] + (i + 1)*(newDispVector[0] - currentDispVector[0])/DRAG_INTERVALS
                y = currentDispVector[1] + (i + 1)*(newDispVector[1] - currentDispVector[1])/DRAG_INTERVALS
                z = currentDispVector[1] + (i + 1)*(newDispVector[2] - currentDispVector[2])/DRAG_INTERVALS

                newAngles = getIKAnglesFromDisplacement(legNum, x,y,z)

                print ('dragMultFeet() ', l, 'disp:', [x,y,z], 'angles:', newAngles)

                '''
                getattr(robot,"hip" + str(legNum)).goal_position = newAngles[0]
                getattr(robot,"knee" + str(legNum)).goal_position = newAngles[1]
                getattr(robot,"ankle" + str(legNum)).goal_position = newAngles[2]
                '''

            time.sleep(.5)

# this one is a generalized version of the others. Dragging is discretized only into two
# because it matches with the two discretizations of the move foot
def moveAndDragMultFeet(legNums, newDispVectors, isMovings):
    # find current displacement vectors at beginning
    currentDispVectors = []
    for l in range(len(legNums)):
        legNum = legNums[l]
        currentAngles = getCurrentAngles(legNum)
        currentDispVectors.append(getDisplacementFromAngles(legNum, currentAngles))

    print "currentDispVectors: ", currentDispVectors
    print 'newDispVectors: ', newDispVectors

    # take multiple steps up at the same time and half drag
    for l in range(len(legNums)):
        legNum = legNums[l]
        newDispVector = newDispVectors[l]
        currentDispVector = currentDispVectors[l]

        # if this command is for stepping foot
        if isMovings[l]:
            [x,y,z] = currentDispVector + .5 * numpy.subtract(newDispVector, currentDispVector)
            z = z + LIFTFOOTHEIGHT

        # else its for dragging foot
        else:
            # get xyz of half drag in the path from currentDispVector to newDispVector
            [x,y,z] = currentDispVector + .5 * numpy.subtract(newDispVector, currentDispVector)

        newAngles = getIKAnglesFromDisplacement(legNum, x,y,z)

            
        print ('moveAndDragMultFeet() ', l, 'moving?: ', isMovings[l], 'disp:', [x,y,z], 'angles:', newAngles)

        '''
        getattr(robot,"hip" + str(legNum)).goal_position = newAngles[0]
        getattr(robot,"knee" + str(legNum)).goal_position = newAngles[1]
        getattr(robot,"ankle" + str(legNum)).goal_position = newAngles[2]
        '''

    time.sleep(STEP_DELAY)

    # put multiple foots down and finish drag
    for l in range(len(legNums)):
        legNum = legNums[l]
        newDispVector = newDispVectors[l]

        if isMovings[l]:
            [x,y,z] = newDispVector
        else:
            [x,y,z] = newDispVector

        newAngles = getIKAnglesFromDisplacement(legNum, x,y,z)

        print ('moveAndDragMultFeet() ', l, 'moving?: ', isMovings[l], 'disp:', [x,y,z], 'angles:', newAngles)

        '''
        getattr(robot,"hip" + str(legNum)).goal_position = newAngles[0]
        getattr(robot,"knee" + str(legNum)).goal_position = newAngles[1]
        getattr(robot,"ankle" + str(legNum)).goal_position = newAngles[2]   
        '''

    time.sleep(1)

def goToHomeFromAnyPosition():
    moveMultFeet([1, 3]  [HOMEPOS["1"], HOMEPOS["3"]])
    moveMultFeet([2, 4]  [HOMEPOS["2"], HOMEPOS["4"]])



def walkingForward():
    #goToHomeFromAnyPosition():

    # thought I would need this starting position but I don't
    #newDispVectors = [numpy.add(HOMEPOS["1"] + [0,1,0]),numpy.add(HOMEPOS["3"] + [0,1,0]), numpy.add(HOMEPOS["2"] + [0,-1,0]), numpy.add(HOMEPOS["4"] + [0,-1,0])]
    #moveAndDragMultFeet([1, 3, 2, 4], newDispVectors, [1,1,0,0])

    for iterations in range(1):
        newDispVectors = [numpy.add(HOMEPOS["1"], [0,-1,0]), numpy.add(HOMEPOS["3"], [0,-1,0]), numpy.add(HOMEPOS["2"], [0,1,0]), numpy.add(HOMEPOS["4"], [0,1,0])]
        moveAndDragMultFeet([1, 3, 2, 4], newDispVectors, [0,0,1,1])

        newDispVectors = [numpy.add(HOMEPOS["1"], [0,1,0]), numpy.add(HOMEPOS["3"], [0,1,0]), numpy.add(HOMEPOS["2"], [0,-1,0]), numpy.add(HOMEPOS["4"], [0,-1,0])]
        moveAndDragMultFeet([1, 3, 2, 4], newDispVectors, [1,1,0,0])

def rotate(degree, direction):
    #goToHomeFromAnyPosition():
    legRadius = (HOMEPOS["1"][0] ** 2.0 + HOMEPOS["1"][1] ** 2.0) **.5
    circleRadius = (BASE_WIDTH/2.0) * math.sqrt(2.0) + legRadius
    x = circleRadius * math.cos(math.radians(45.0 + degree)) - (BASE_WIDTH/2.0) - HOMEPOS["1"][0]
    y = circleRadius * math.sin(math.radians(45.0 + degree)) - (BASE_WIDTH/2.0) - HOMEPOS["1"][1]

    for iterations in range(1):
        moveMultFeet([1, 3], [numpy.add(HOMEPOS["1"], [x,y,0]), numpy.add(HOMEPOS["3"], [-x,-y,0])])
        print "NEW---------------------"
        moveMultFeet([2, 4], [numpy.add(HOMEPOS["2"], [-y,x,0]), numpy.add(HOMEPOS["3"], [y,-x,0])])

        moveAndDragMultFeet([1, 3, 2, 4], [HOMEPOS["1"], HOMEPOS["3"], HOMEPOS["2"], HOMEPOS["4"]], [0,0,0,0])






import time
import numpy
import math


#print("current angles: ", getCurrentAngles(1))
#print(getDisplacementFromAngles(1, getCurrentAngles(1)))
#moveFoot(1,HOMEPOS["1"])
#moveFoot(2,HOMEPOS["2"])

print "-----------------------"
#moveMultFeet([1, 2],  [HOMEPOS["1"], HOMEPOS["2"]])
#walkingForward()
rotate(30, 'LEFT')
'''
dragFoot(1,HOMEPOS["1"])
dragFoot(2,HOMEPOS["2"])
print "-----------------------"
dragMultFeet([1, 2],  [HOMEPOS["1"], HOMEPOS["2"]])

newDispVectors = [numpy.add(HOMEPOS["1"], [0,-1,0]), numpy.add(HOMEPOS["3"], [0,-1,0]), numpy.add(HOMEPOS["2"], [0,1,0]), numpy.add(HOMEPOS["4"], [0,1,0])]
moveAndDragMultFeet([1, 3, 2, 4], newDispVectors, [0,0,1,1])
'''

