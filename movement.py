'''The move and turn constants must be made more accurate. Apart from that, this should be mostly done.
New functions can be added if necessary.'''



from sr.robot3 import *
r = Robot()

#The respective boards of the robot

motors = r.motor_board.motors #There is only one motor board, with two motors
servos = r.servo_board.servos #There is only one servo, which controls the arm
power = r.power_board.outputs #There is only one non-standard connection, in position H0, which controls the vacuum


#Coefficients stored as constants to allow measurement of movement in helpful units
#These may not be exactly right, so feel free to change them
#The move constant is an arbitrary value, but the turn constant should allow turns to be measured in degrees
MOVE_CONST = 0.5
TURN_CONST = 0.015

def drive(distance):
    '''
    This function moves the robot forward some distance by
    letting the robot move for a time equal to the inputted distance * MOVE_CONST.
    A negative distance will move the robot backwards.
    '''

    if distance >= 0:
        motors[0].power = 1
        motors[1].power = 1
    else:
        motors[0].power = -1
        motors[1].power = -1
        
    r.sleep(abs(distance)*MOVE_CONST)
    
    motors[0].power = 0
    motors[1].power = 0
    r.sleep(0.1) 
    #Pauses the robot at the end of the action to minimise randomness in ending position 

def turn(angle):
    '''
    This function turns the robot clockwise by some angle by
    giving the wheels opposite powers and letting the robot move
    for a time equal to the inputted angle * TURN_CONST.
    A negative angle will move the robot anticlockwise.
    '''
    
    if angle < 0:
        angle = abs(angle)
        motors[0].power = 0
        motors[1].power = 0.5
        r.sleep(angle*TURN_CONST)
    else:
        motors[1].power = 0
        motors[0].power = 0.5
        r.sleep(angle*TURN_CONST)
    motors[0].power = 0
    motors[1].power = 0
    r.sleep(0.1)


def pickup(start_height = None, end_height = None):
    '''
    This function turns on the robot's vacuum arm. 
    If start_height and end_height are specified, the arm 
    will move to start_height before activating and to end_height after activating
    '''

    r.sleep(0.1)
    if start_height != None:
        servos[0].position = start_height #servos[0] is the arm servo

    power[OUT_H0].is_enabled = True #power[OUT_H0] is the power to the vacuum

    if end_height != None:
        servos[0].position = end_height

    r.sleep(0.2)
    
    
    
def drop(start_height = None, end_height = None):
    '''
    This function turns off the robot's vacuum arm. 
    If start_height and end_height are specified, the arm 
    will move to start_height before deactivating and to end_height after deactivating
    '''

    r.sleep(0.1)
    if start_height != None:
        servos[0].position = start_height

    power[OUT_H0].is_enabled = False

    if end_height != None:
        servos[0].position = end_height

    r.sleep(0.2)

def arm_move(new_pos):
    '''
    This function moves the arm to a different height.
    It is pretty much just a wrapper and it only accepts float values between -1 and 1
    '''
    
    r.sleep(0.1)
    servos[0].position = new_pos
    r.sleep(0.1)

