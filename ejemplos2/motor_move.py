import sys
sys.path.append("/home/pi/bmw/libs")
import motorbk as motor
import time

motor1 = motor.motorbk(7)
motor1.move(255,180)
motor1.wait()
motor1.move(-255,180)
motor1.wait()
