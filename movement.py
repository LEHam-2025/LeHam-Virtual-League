'''
This is being worked on. 
Imports from the sensing library 
and is imported by the logic library.

This library also imports from math for calculations
'''




from sensing import *
from math import degrees, cos


#Coefficients stored as constants to allow measurement of movement in helpful units
#These may not be exactly right, so feel free to change them
MOVE_CONST = 1     #The move constant makes the robot move roughly 1/255 mm per drive unit
TURN_CONST = 0.015 #The turn constant allows the robot to turn in degrees



def valid_place(marker):
    mark_tower = tower(marker.id)
    if max_height(mark_tower) < 200:
        return True
    elif id_type(mark_tower[0], 1) != myZone:
        return True
    else:
        return False

def clean(towerIDs):
    towerIDs.sort(key=height, reverse= True)
    ids = []
    final = []

    for mark in towerIDs:
        if mark.id not in ids:
            ids.append(mark.id)
            final.append(mark)
    
    return final

def tower(marker_ID):
    '''Returns all the markers in a stack with the given one, arranged from highest to lowest'''
    marks = search_any(wanted_ID = marker_ID) #Get all markers
    try:
        wanted_mark = [mark for mark in marks if mark.id == marker_ID][0] #The marker being considered
        parts = [mark for mark in marks if stacked(wanted_mark, mark)] + [wanted_mark]
        parts = clean(parts)
        return parts
    
    except IndexError:
        return

def drive(distance, rest=0.1):
    '''
    This function moves the robot forward some distance by
    letting the robot move for a time equal to the inputted distance * MOVE_CONST.
    A negative distance will move the robot backwards.
    '''

    if distance >= 0:
        MOTORS[0].power = 0.2
        MOTORS[1].power = 0.2
    else:
        MOTORS[0].power = -0.2
        MOTORS[1].power = -0.2
        
    r.sleep(abs(distance)*MOVE_CONST)
    
    MOTORS[0].power = 0
    MOTORS[1].power = 0
    r.sleep(rest) 
    #Pauses the robot at the end of the action to minimise randomness in ending position 

def turn(angle, unit = 'd', speed = 0.2):
    '''
    This function turns the robot clockwise by some angle by
    giving the wheels opposite powers and letting the robot move
    for a time equal to the inputted angle * TURN_CONST.
    A negative angle will move the robot anticlockwise.
    Unit defaults to degrees, but if it is given as r, 
    it will treat it as a radians value.
    '''

    alt_constant = TURN_CONST*(0.2/speed)
    if unit == 'r': #if the angle is in radians, convert to degrees
        angle = degrees(angle)
    if angle < 0: #Turn the other way
        angle = abs(angle)
        MOTORS[0].power = -speed 
        MOTORS[1].power = speed   
        r.sleep(angle*TURN_CONST)
    else:
        MOTORS[1].power = -speed
        MOTORS[0].power = speed
        r.sleep(angle*alt_constant)
    MOTORS[0].power = 0
    MOTORS[1].power = 0
    
    r.sleep(0.1)

def pickup(start_height = None, end_height = None):
    '''
    This function turns on the robot's vacuum arm. 
    If start_height and end_height are specified, the arm 
    will move to start_height before activating and to end_height after activating
    '''

    r.sleep(0.1)
    if start_height != None:
        SERVOS[0].position = start_height #SERVOS[0] is the arm servo

    POWER[OUT_H0].is_enabled = True #POWER[OUT_H0] is the power to the vacuum
    
    r.sleep(0.5)
    if end_height != None:
        SERVOS[0].position = end_height

    r.sleep(0.1)
     
def drop(start_height = None):
    '''
    This function turns off the robot's vacuum arm. 
    If start_height and end_height are specified, the arm 
    will move to start_height before deactivating and to end_height after deactivating
    '''

    
    if start_height != None:
        SERVOS[0].position = start_height
    
    POWER[OUT_H0].is_enabled = False

    SERVOS[0].position = 1

def arm_move(new_pos):
    '''
    This function moves the arm to a different height.
    It is pretty much just a wrapper and it only accepts float values between -1 and 1
    '''
    
    SERVOS[0].position = new_pos
    r.sleep(0.1)

def align(marker_ID, accuracy = 0.02, type = 'h'):
    '''
    Aligns the robot wth the marker of inputted ID, 
    to the accuracy of the inputted angle (in radians).
    If no accuracy is given, it defaults to 0.02 (~1 degrees)
    '''
    turned = 0
    angle = get_angle(marker_ID, type=type)
    while abs(angle) > accuracy:
        r.sleep(0.01)
        if angle == 10: #If not seen, turn 15 degrees
            turn(15, speed=1)
            turned += 15

            if turned >= 360:
                return False
        else:
            turn((0.4*(angle)), 'r', 0.1) #Since get_angle returns a radians value
        
        angle = get_angle(marker_ID, type=type)
    
    return True

def drive_towards(marker_ID, dist_from = 3, precision = 0.01):
    '''
    Drives the robot towards a marker and stops
    dist_from away. dist_from defaults to 5.
    '''
    try:
        stop = False
        align(marker_ID, 0.02, 'h')
        r.sleep(0.1)
        dist_remain = get_distance(marker_ID)

        dis = ((dist_remain - dist_from)/255) - 3
        drive(dis)
        
        while not stop:
            r.sleep(0.1)
            if get_angle(marker_ID) > (0.5*precision): #If misaligned
                align(marker_ID, precision, 'h')
            
            dist_remain = get_distance(marker_ID)

            dis = ((dist_remain - dist_from)/255)
            drive(dis)
            
            if (dist_remain - (255*dis)) <= (dist_from + 1): #If too close, the camera does not pick up the marker
                stop = True

    except:
        escape()
        drive_towards(marker_ID, dist_from, precision)

def go_to_pick(marker_ID, s_height = -1, e_height = 1, a_height = 0):
    '''Moves the robot to the marker and picks it up. 
    s_height and e_height are passed to the pickup function
    as start_height and end_height respectively. a_height is the approach height'''

    arm_move(a_height)
    drive_towards(marker_ID, 3, precision=0.005)
    pickup(start_height=s_height, end_height = e_height)

def escape():
    allowed_directions = free_space(1000)
    if 'front' in allowed_directions:
        drive(2)    
    elif 'back' in allowed_directions:
        drive(-2)
    elif 'right' in allowed_directions:
        turn(90)
        drive(2)
    elif 'left' in allowed_directions:
        turn(-90)
        drive(2)
    else:
        print('trapped')

def search_any(type = 'Any', wanted_ID = None, floor = False):
    '''Return a list of markers. 
    If none are seen, turns until at least one is spotted. 
    If a full 360 turn has been completed, move somewhere else.
    If wanted_ID is given, looks for that specific ID.
    If type is given, only considers markers of that type'''

    if wanted_ID != None:
        align(wanted_ID, 0.05)
    
    markers = get_markers(type, floor=floor)

    turned = 0
    while not markers:
        turn(15)
        turned += 15
        markers = get_markers(type)

        if turned == 360:
            return []
    
    return markers