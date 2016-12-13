# based on MonkMakes 08_manual_robot_continuous.py
# Use the arrow keys to direct the robot

from multiprocessing import Process
from rrb3 import *
import sys
import tty
import termios

rr = RRB3(9.0, 6.0) # battery, motor
motor_speed = 0.4

UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3

print("Use the arrow keys to move the robot")
print("Press CTRL-c TWICE to quit the program")

# These nexttwo functions allow the program to read your keyboard
def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return ord(c3) - 65  # 0=Up, 1=Down, 2=Right, 3=Left arrows

# This controls the distance measuring
def loop_a():
    while 1:    
        distance = rr.get_distance()
        if distance < 20:
            print (distance)
            rr.reverse(2, motor_speed)
            print 'sensor'            
#            break

# Start Process (sensor) loop
Process(target=loop_a).start()

# This will control the movement of your robot and display on your screen
try: 
    while True:
        keyp = readkey()
        if keyp == UP:
            rr.forward(0, motor_speed) # if you don't specifiy duration it keeps going indefinately
            print 'forward'
        elif keyp == DOWN:
            rr.reverse(0, motor_speed)
            print 'backward'
        elif keyp == RIGHT:
            rr.right(0, motor_speed)
            print 'clockwise'
        elif keyp == LEFT:
            rr.left(0, motor_speed)
            print 'anti clockwise'
        elif keyp == ' ':
            rr.stop()
            print 'end stop'
        elif ord(keyp) == 3:  #Press CTRL-c TWICE to quit the program
            print 'break'
            break

except KeyboardInterrupt:
    GPIO.cleanup()


