'''
This is currently empty, 
but will be where the high level logic takes place.
Imports from the movement library and is imported 
by the robot.py file.
'''

from movement import *

pals = 6 #Number of pallets





def closest(type = 'Any'):
    '''Returns the closest marker. If type is given,
    only considers a specific category of markers.'''
    marks = search_any(type)

    try:
        return marks[0]
    except:
        return None

def deposit(dest: (str | int) = 'centre'):
    '''
    Goes to dest and releases the pallet.
    If dest is given as an int, goes to that ID marker.
    If dest is given as a string, goes to the closest 
    marker of that category. dest defaults to centre
    '''
    if type(dest) == int:
        drive_towards(dest)

    elif dest == 'mid':
        drive_towards(closest('mid rise').id)
        arm_move(-1)
    elif dest == 'mid':
        drive_towards(closest('high rise').id)
        arm_move(1)
    
    drop()
    global pals
    pals -= 1

def game():
    while pals:
        pallet_place()

def pallet_place():
    '''
    The start_game function. 
    Deposits the closest pallet 
    on the closest mid high rise.
    '''
    target = closest('z0')
    if target != None:
        go_to_pick(target.id)
        deposit('mid')
    else:
        print('Not seen')