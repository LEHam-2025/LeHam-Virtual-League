'''
The library for sensing functions. 
Must have the camera set through the set_cam function 
before anything else is used.
Imports from math and is imported by the movement library.
This is the first file in the chain.
'''

from math import inf
from math import sin

camera = None
myZone = None

means = [ #The categories of marker ids. In the form ['first id', 'last id', Group No, Group Name]
[0, 28, 0, 'bound'], #Boundary
[100, 120, 1, 'z0'], #zone 0 pallets
[120, 140, 2, 'z1'], #zone 1 pallets
[140, 160, 3, 'z2'], #zone 2 pallets
[160, 180, 4, 'z3'], #zone 3 pallets
[195, 199, 5, 'mid rise'], #high rises
[199, 200, 6, 'high rise']] #centre high rise



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

    for type in means:
        if in_id in range(type[0], type[1]):
            if type_out == 0:
                return type[2]
            else:
                return type[3]

def set_cam(cam):
    '''Sets the camera 
    for the functions in this file. 
    I will most likely make this redundant later'''

    global camera
    camera = cam

def get_angle(markerID, type = 'y'):
    '''Returns the yaw angle of the
    first marker spotted that matches the inputted ID.
    Returns 10 if the marker is not seen'''
    markers = camera.see()

    for marker in markers:
        if marker.id == markerID:
            if type == 'y':
                return marker.orientation.yaw
            else:
                return marker.position.horizontal_angle

    return 10

def get_distance(markerID):
    '''Returns the distance in mm to the
    first marker spotted that matches the inputted ID.
    Returns inf if the marker is not seen'''
    markers = camera.see()

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
    markers = camera.see()

    if type != 'Any':
        markers = [marker for marker in markers if is_type(marker, type)]
    if floor == True:
        markers = [marker for marker in markers if height(marker) < 30]
    
    markers.sort(key=dist_sort)
    return markers