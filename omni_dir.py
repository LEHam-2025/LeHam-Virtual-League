from sr.robot3 import Robot
from math import sin, cos, radians
#create robot object
robot = Robot()

MOTOR1 = robot.motor_boards["SR0NBL"]	
MOTOR2 = robot.motor_boards["SR0HDM"]

DCONST = 0.2 #DRIVE CONSTANT - SPEED OF DRIVING
ACONST = 0.1 #ANGLE CONSTANT - SPEED OF TURN

DTIME = 1 #DRIVE TIME - SEE CODE
ATIME = 0.00748 #TIME TO TURN

BIAS00 = 1.1 #THESE BIASES ARE FOR
BIAS01 = 1 #CALIBRATIONS OF THE 
BIAS10 = 1.3 #MOTORS SO THEY TURN AT
BIAS11 = 1.35	 #THE SAME SPEED


def straight_1(distance): #Moves using one set of wheels
    MOTOR1.motors[0].power = BIAS00 * DCONST
    MOTOR1.motors[1].power = BIAS01 * DCONST
    MOTOR2.motors[0].power = 0
    MOTOR2.motors[1].power = 0
    robot.sleep(distance * DTIME)
    MOTOR1.motors[0].power = 0
    MOTOR1.motors[1].power = 0
    MOTOR2.motors[0].power = 0
    MOTOR2.motors[1].power = 0

def straight_2(distance): #Moves using the other set of wheels
    MOTOR2.motors[0].power = BIAS10 * DCONST
    MOTOR2.motors[1].power = BIAS11 * DCONST
    MOTOR1.motors[0].power = 0
    MOTOR1.motors[1].power = 0
    robot.sleep(distance * DTIME)
    MOTOR1.motors[0].power = 0
    MOTOR1.motors[1].power = 0
    MOTOR2.motors[0].power = 0
    MOTOR2.motors[1].power = 0

def cust_angle(angle, distance): #Moves at a custom angle
    adjust1 = cos(radians(angle))
    adjust2 = sin(radians(angle))

    MOTOR1.motors[0].power = BIAS00 * DCONST * adjust1
    MOTOR1.motors[1].power = BIAS01 * DCONST * adjust1
    MOTOR2.motors[0].power = BIAS10 * DCONST * adjust2
    MOTOR2.motors[1].power = BIAS11 * DCONST * adjust2

    robot.sleep(distance * DTIME)

    MOTOR1.motors[0].power = 0
    MOTOR1.motors[1].power = 0
    MOTOR2.motors[0].power = 0
    MOTOR2.motors[1].power = 0


