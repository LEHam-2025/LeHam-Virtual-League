'''
The library for sensing functions. 
Must have the camera set through the set_cam function 
before anything else is used.
Doesn't make any imports and is imported by the movement library.
This is the lowest-level file in the chain.
'''

camera = None

def set_cam(cam):
    global camera
    camera = cam

def get_angle(markerID):
    '''Returns the horizontal angle of the
    first marker spotted that matches the inputted ID.
    Returns 10 if the marker is not seen'''
    markers = camera.see()

    for marker in markers:
        if marker.id == markerID:
            return marker.position.horizontal_angle

    return 10

def get_markers():
    return camera.see()