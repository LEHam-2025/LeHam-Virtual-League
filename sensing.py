'''
The library for sensing functions. 
Imports from math and sr.robot3, and is imported by the movement library.
This is the first file in the chain.
'''

from math import inf
from math import sin
from sr.robot3 import *

r = Robot()

#The respective boards of the robot

MOTORS = r.motor_board.motors #There is only one motor board, with two motors
SERVOS = r.servo_board.servos #There is only one servo, which controls the arm
POWER = r.power_board.outputs #There is only one non-standard connection, in position H0, which controls the vacuum
CAMERA = r.camera
ARDUINO = r.arduino

MEANS = [ #The categories of marker ids. In the form ['first id', 'last id', Group No, Group Name]
[0, 28, 0, 'bound'], #Boundary
[100, 120, 1, 'z0'], #zone 0 pallets
[120, 140, 2, 'z1'], #zone 1 pallets
[140, 160, 3, 'z2'], #zone 2 pallets
[160, 180, 4, 'z3'], #zone 3 pallets
[195, 199, 5, 'mid rise'], #high rises
[199, 200, 6, 'high rise']] #centre high rise

##Pins##
#front_ultra = (2, 3)
#left_ultra = (4, 5)
#right_ultra = (6, 7)
#back_ultra = (8, 9)
FRONT_LEFT_BUMP = ARDUINO.pins[10]
FRONT_RIGHT_BUMP = ARDUINO.pins[11]
REAR_LEFT_BUMP = ARDUINO.pins[12]
REAR_RIGHT_BUMP = ARDUINO.pins[13]

FRONT_LEFT_BUMP.mode = INPUT
FRONT_RIGHT_BUMP.mode = INPUT
REAR_LEFT_BUMP.mode = INPUT
REAR_RIGHT_BUMP.mode = INPUT

myZone = None

def free_space(threshold: int = 500):
    '''
    Returns all the directions that are unblocked.
    If threshold is given, passes that to the is_space
    function
    '''
    return [direction for direction in ['front', 'back', 'left', 'right'] if is_space(direction, threshold)]

def is_space(direction: str, threshold: int = 500) -> bool:
    '''
    Returns a boolean value of whether there is enough space in a certain direction.
    The threshold defaults to 500mm
    '''
    match direction:
        case 'front':
            return front_space() >= threshold
        case 'back':
            return back_space() >= threshold
        case 'left':
            return left_space() >= threshold
        case 'right':
            return right_space() >= threshold
        case _:
            print('Not a direction')
            return False

def front_space():
    '''
    Returns the unobscured distance, in mm, in front of the robot.
    This considers the front bumpers, the front ultrasound and the camera
    '''
    if FRONT_LEFT_BUMP.digital_read() or FRONT_RIGHT_BUMP.digital_read():
        return 0

    ultra_dist = ARDUINO.ultrasound_measure(2, 3)
    if not ultra_dist:
        ultra_dist = 5750
    
    close = get_markers(floor= False)
    if close:
        cam_dist = close[0].position.distance
    else:
        cam_dist = 5750
    
    return min([ultra_dist, cam_dist])

def back_space():
    '''
    Returns the unobscured distance, in mm, behind the robot.
    This considers the rear bumpers and the rear ultrasound
    '''
    if REAR_LEFT_BUMP.digital_read() or REAR_RIGHT_BUMP.digital_read():
        return 0

    ultra_dist = ARDUINO.ultrasound_measure(8, 9)
    if not ultra_dist:
        ultra_dist = 5750
    
    return ultra_dist

def right_space():
    '''
    Returns the unobscured distance, in mm, to the right of the robot.
    This considers the right ultrasound.
    '''
    ultra_dist = ARDUINO.ultrasound_measure(6, 7)
    if not ultra_dist:
        ultra_dist = 5750

    return ultra_dist

def left_space():
    '''
    Returns the unobscured distance, in mm, to the left of the robot.
    This considers the left ultrasound.
    '''
    ultra_dist = ARDUINO.ultrasound_measure(4, 5)
    if not ultra_dist:
        ultra_dist = 5750

    return ultra_dist

def stacked(mark1, mark2):
    '''Returns a boolean value denoting whether two markers are stacked or not'''

    hoz_tolerance = 0.18
    vert_tolerance = 50
    dist_tolerance = 200

    angles = (mark1.position.horizontal_angle, mark2.position.horizontal_angle)
    distances = (mark1.position.distance, mark2.position.distance)
    heights = (height(mark1), height(mark2))

    if ((max(angles) - min(angles)) < hoz_tolerance) and ((max(heights) - min(heights)) > vert_tolerance) and (max(distances) - min(distances) < dist_tolerance):
        return True
    
    return False

def max_height(stack):
    return height(stack[0])

def id_type(in_id, type_out = 0):
    '''Returns the marker category. type_out defualts to 0, 
    returning the number for easier handling, but can be set to 1
    to return a string representation.'''

    for type in MEANS:
        if in_id in range(type[0], type[1]):
            if type_out == 0:
                return type[2]
            else:
                return type[3]

def get_angle(markerID, type = 'y'):
    '''Returns the yaw angle of the
    first marker spotted that matches the inputted ID.
    Returns 10 if the marker is not seen'''
    result = 0
    
    try: #This is actually awful practice, but whatever
        for _ in range(3):
            markers = CAMERA.see()

            for marker in markers:
                if marker.id == markerID:
                    if type == 'y':
                        result +=  marker.orientation.yaw
                    else:
                        result += marker.position.horizontal_angle
                    break
        if result == 0:
            return 10
        return (result/3)
    except: #And it gets worse
        return 10

def get_distance(markerID):
    '''Returns the distance in mm to the
    first marker spotted that matches the inputted ID.
    Returns inf if the marker is not seen'''
    markers = CAMERA.see()

    for marker in markers:
        if marker.id == markerID:
            return marker.position.distance

    return inf

def dist_sort(marker):
    '''For the sort function. 
    Returns the distance to the marker'''

    return marker.position.distance

def is_type(marker, type = 'Any'):
    if type == 'Any':
        return True
    
    if id_type(marker.id, 1) == type:
        return True
    else:
        return False

def height(marker):
    '''Returns the vertical height of a marker'''
    return (sin(marker.position.vertical_angle)*marker.position.distance)

def get_markers(type = 'Any', floor = True):
    '''
    Returns the list of markers seen.
    If type is given, only returns markers of a specific category
    floor defaults to True, only returning grounded markers
    '''
    markers = CAMERA.see()

    if type != 'Any':
        markers = [marker for marker in markers if is_type(marker, type)]
    if floor == True:
        markers = [marker for marker in markers if height(marker) < 30]
    
    markers.sort(key=dist_sort)
    return markers