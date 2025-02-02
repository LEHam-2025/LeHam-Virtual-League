'''
The library for sensing functions. 
Must have the camera set through the set_cam function 
before anything else is used.
Imports from math and is imported by the movement library.
This is the first file in the chain.
'''

from math import inf

camera = None
means = [ #The categories of marker ids. In the form ['first id', 'last id', Group No, Group Name]
[0, 28, 0, 'bound'], #Boundary
[100, 120, 1, 'z0'], #zone 0 pallets
[120, 140, 2, 'z1'], #zone 1 pallets
[140, 160, 3, 'z2'], #zone 2 pallets
[160, 180, 4, 'z3'], #zone 3 pallets
[195, 199, 5, 'high rise']] #high rises (199 for centre)

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

def get_facing_angle():
    wall_markers = [mark for mark in get_markers() if id_type(mark.id) == 0]
    
    if len(wall_markers) >= 2:
        face_angle = compare(wall_markers[0], wall_markers[1])

def compare(mark1, mark2):
    pass

def get_markers():
    '''
    Returns the list of markers seen.
    This is a wrapper for the camera.see method
    '''
    return camera.see()