'''
This is currently empty, 
but will be where the high level logic takes place.
Imports from the movement library and is imported 
by the robot.py file.

Must run init_Zone() before anything else to automatically set the zone
'''

from movement import *


def game():
    init_Zone()
    while True:
        pallet_place()
        pallet_place()
        pallet_place('cen')

def init_Zone():
    '''Automatically initialises myZone by seeing what high rise is in front of the robot'''
    
    global myZone

    if (closest(dest=False).id) == 195:
        myZone = 'z0'
    elif (closest(dest=False).id) == 196:
        myZone = 'z1'
    elif (closest(dest=False).id) == 197:
        myZone = 'z2'
    else:
        myZone = 'z3'

def closest(type = 'Any', dest = True, pallet = False, floor = True):
    '''Returns the closest marker. If type is given,
    only considers a specific category of markers. If pallet is given, only considers pallets'''
    marks = search_any(type, floor = floor)
    try:
        if dest:
            marks = [mark for mark in marks if valid_place(mark)]

        if pallet:
            marks = [mark for mark in marks if (id_type(mark.id) in range(1, 5))]
        return marks[0]
    except:
        escape()
        return closest(type=type, dest=dest, pallet=pallet, floor=floor)

def deposit(dest: (str | int) = 'cen'):
    '''
    Goes to dest and releases the pallet.
    If dest is given as an int, goes to that ID marker.
    If dest is given as a string, goes to the closest 
    marker of that category. dest defaults to cen (centre)
    '''
    

    if type(dest) == int:
        drive_towards(dest, 1)
        tower_height = [((max_height(tower(dest)) // 100)), 0]

    elif dest == 'mid':
        id = closest('mid rise', floor = False).id
        maximal = max_height(tower(id))
        tower_height = [((maximal// 100)), 0]
        drive_towards(id, 1, 0.02)
        
    elif dest == 'cen':
        drive_towards(199, 1, 0.01)
        tower_height = [1, -1]
    else:
        print('not an option')
        return
    
    arm_move(max(tower_height))
    r.sleep(0.1)
    drop()
    drive(-1)

def pallet_place(dest = 'mid', a_height = 0):
    '''
    The complete pallet placing function. 
    Deposits the closest pallet 
    on the closest mid high rise.
    '''
    target = closest(myZone, floor = True)
    if target != None:
        go_to_pick(target.id, a_height=a_height)
        deposit(dest)
    else:
        print('Not seen')