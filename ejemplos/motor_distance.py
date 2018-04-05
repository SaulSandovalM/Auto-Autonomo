import sys
sys.path.append("/home/pi/bmw/libs")
import motorbk as motor
import time
import math

long = 3.14159*6 
dist = 150
real = dist/long

motor1=motor.motorbk(7)
motor2=motor.motorbk(6)

motor1.turn(-255,real)
motor2.turn(255,real)
motor1.wait()
motor2.wait()

