import sys
sys.path.append("/home/pi/bmw/libs")
import motorbk as motor
import time
import math


lon = 3.14159 * 6 #lon llanta en centimetros

dist = 40

rel = dist / lon

motor1 = motor.motorbk(7)
motor2 = motor.motorbk(6)


motor1.turn(-255,rel)
motor2.turn(255,rel)
motor1.wait()
motor2.wait()

