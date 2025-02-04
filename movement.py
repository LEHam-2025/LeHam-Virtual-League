'''
This is being worked on. 
Imports from the sensing library 
and is imported by the logic library.

This library also imports from sr.robot3 and math for calculations
'''



from sr.robot3 import *
from sensing import *
from math import degrees

r = Robot()

#The respective boards of the robot

motors = r.motor_board.motors #There is only one motor board, with two motors
servos = r.servo_board.servos #There is only one servo, which controls the arm
power = r.power_board.outputs #There is only one non-standard connection, in position H0, which controls the vacuum
set_cam(r.camera)

#Coefficients stored as constants to allow measurement of movement in helpful units
#These may not be exactly right, so feel free to change them
#The move constant is an arbitrary value, but the turn constant should allow turns to be measured in degrees
MOVE_CONST = 1
TURN_CONST = 0.015





def drive(distance, rest=0.1):
    '''
    This function moves the robot forward some distance by
    letting the robot move for a time equal to the inputted distance * MOVE_CONST.
    A negative distance will move the robot backwards.
    '''

    if distance >= 0:
        motors[0].power = 0.2
        motors[1].power = 0.2
    else:
        motors[0].power = -0.2
        motors[1].power = -0.2
        
    r.sleep(abs(distance)*MOVE_CONST)
    
    motors[0].power = 0
    motors[1].power = 0
    r.sleep(rest) 
    #Pauses the robot at the end of the action to minimise randomness in ending position 

def turn(angle, unit = 'd'):
    '''
    This function turns the robot clockwise by some angle by
    giving the wheels opposite powers and letting the robot move
    for a time equal to the inputted angle * TURN_CONST.
    A negative angle will move the robot anticlockwise.
    Unit defaults to degrees, but if it is given as r, 
    it will treat it as a radians value.
    '''
    if unit == 'r': #if the angle is in radians, convert to degrees
        angle = degrees(angle)
    if angle < 0: #Turn the other way
        angle = abs(angle)
        motors[0].power = -0.2 #For some reason backwards is
        motors[1].power = 0.2   #about double the power of forwards
        r.sleep(angle*TURN_CONST)
    else:
        motors[1].power = -0.2
        motors[0].power = 0.2
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
     
def drop(start_height = None):
    '''
    This function turns off the robot's vacuum arm. 
    If start_height and end_height are specified, the arm 
    will move to start_height before deactivating and to end_height after deactivating
    '''

    
    if start_height != None:
        servos[0].position = start_height
    r.sleep(0.2)
    
    power[OUT_H0].is_enabled = False

    servos[0].position = 1

    r.sleep(0.2)

def arm_move(new_pos):
    '''
    This function moves the arm to a different height.
    It is pretty much just a wrapper and it only accepts float values between -1 and 1
    '''
    
    r.sleep(0.1)
    servos[0].position = new_pos
    r.sleep(0.1)

def align(marker_ID, accuracy = 0.02, type = 'y'):
    '''
    Aligns the robot wth the marker of inputted ID, 
    to the accuracy of the inputted angle (in radians).
    If no accuracy is given, it defaults to 0.02 (~1 degrees)
    '''

    while abs(get_angle(marker_ID, type)) > accuracy:
        #print(get_angle(marker, type)) #For testing
        if get_angle(marker_ID) == 10: #If not seen, turn 30 degrees
            turn(15)
        else:
            turn((0.4*(get_angle(marker_ID, type))), 'r') #Since get_angle returns a radians value
    r.sleep(0.1)

def drive_towards(marker_ID, dist_from = 5):
    '''
    Drives the robot towards a marker and stops
    dist_from away. dist_from defaults to 5.
    '''
    stop = False

    align(marker_ID, 0.01, 'h')
    dist_remain = get_distance(marker_ID)
    dis = (dist_remain - dist_from)/510
    drive(dis)
    
    while not stop:
        if get_angle(marker_ID) > 0.005: #If misaligned
            align(marker_ID, 0.005, 'h')
        
        dist_remain = get_distance(marker_ID)
        dis = (dist_remain - dist_from)/255
        drive(dis)
        
        if (dist_remain - (255*dis)) <= (dist_from + 3): #If too close, the camera does not pick up the marker
            stop = True

def go_to_pick(marker_ID, s_height = -1, e_height = 1):
    '''Moves the robot to the marker and picks it up. 
    s_height and e_height are passed to the pickup function
    as start_height and end_height respectively'''
    arm_move(-1)
    drive_towards(marker_ID)
    pickup(start_height=s_height, end_height = e_height)

def search_any(type = 'Any'):
    '''Return a list of markers. If none are seen, turns until at least 1 is spotted'''
    markers = get_markers(type)

    while not markers:
        turn(20)
        markers = get_markers(type)
    
    return markers