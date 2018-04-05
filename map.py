import sys
import atexit
sys.path.append("/home/pi/bmw/libs")
import motorbk as motor
import time
import io
import time
import picamera
import math
import distancebk as distance
import colorbk as colorx
#################################################

sensor1 = colorx.colorbk(1)
sensor2 = colorx.colorbk(2)

sensor = distance.distancebk(3)

motor1 = motor.motorbk(7) # pin del motor izquierdo
motor2 = motor.motorbk(6) # pin del motor derecho

loc_x_car = 25 # coordenada inicial en y
loc_y_car = 25 # coordenada inicual en x
mapping = 0
box_cord = [0] * 6

color = 0

ppr = 600
radio_rueda = 3
pi = 3.14159

rueda = pi * 2 * radio_rueda

dist = rueda / ppr

####### Avanza en linea recta ###################

def avanza(speed, dist, lon): #avanza el coche en linea recta

    rel = dist / lon
    motor1.turn(-speed,rel)
    motor2.turn(speed,rel)
    motor1.wait()
    motor2.wait()

######## Linea ###############################################
def linea(cuenta, objetivo, velocidad, enci, encd, dist):

	while (cuenta <= objetivo):

		if sensor1.read() == sensor2.read():
			motor1.set(-130)
			motor2.set(130)

		elif sensor1.read() == "white" and sensor2.read() != "white" :
			motor1.set(-150)
			motor2.set(130)

		elif sensor1.read() !="white" and sensor2.read() == "white" :
			motor1.set(-130)
			motor2.set(150)

		new_mot_i = motor1.read()

		encoderi = enci - new_mot_i
		enci = new_mot_i


		new_mot_d = motor2.read()
		encoderd = new_mot_d - encd
		encd = new_mot_d

		cuenta = cuenta + encoderi * dist

		time.sleep(0.01) ## para no saturar


####### Girar vehiculo ##########################################

def gira(velocidad, grados): # velocidad, grados de giro, girar clockwise?

	motor1.move(velocidad, grados)
	motor2.move(velocidad, grados)
	motor1.wait()
	motor2.wait()
	time.sleep(0.1)

########## Saber en que cuadrante esta el coche ####


def get_quad(loc_x_car, loc_y_car):


	if loc_x_car == 25 and loc_y_car < 175:
		quad = 1
	elif loc_x_car < 175 and loc_y_car == 175:
		quad = 2
	elif loc_x_car == 175 and loc_y_car > 25:
		quad = 3
	elif loc_x_car > 25 and loc_y_car == 25:
		quad = 4

	return quad

############## Quads ###################################
########################################################

def obj_pos(q, x_past, y_past, move_made, dist):

	if q == 1:

		y_obj = y_past + move_made
		x_obj = 37.5 + dist

		y_sup = y_obj + 25
		x_sup = x_obj

		y_inf = y_obj - 25
		x_inf = x_obj

	elif q == 2:

		y_obj = 162.5 - dist
		x_obj = x_past + move_made

		y_sup = y_obj
		x_sup = x_obj +25

		y_inf = y_obj
		x_inf = x_obj -25


	elif q == 3:

		y_obj = y_past - move_made
		x_obj = 162.5 - dist

		y_inf = y_obj - 25
		x_inf = x_obj

		y_sup = y_obj + 25
		x_sup = x_obj

	elif q == 4:

		y_obj = 37.5 + dist
		x_obj = x_past - move_made

		y_inf = y_obj
		x_inf = x_obj - 25

		y_inf = y_obj
		x_inf = x_obj + 25

	return x_obj, y_obj, x_sup, y_sup, x_inf, y_inf

#######################################################
############# update positions depending on quad ######
def update_pos(quad, loc_x_car, loc_y_car):

	if quad == 1:
	    x_car_pos = loc_x_car
	    y_car_pos = loc_y_car + 25

	elif quad == 2:
		x_car_pos = loc_x_car + 25
		y_car_pos = loc_y_car

	elif quad == 3:
		x_car_pos = loc_x_car
		y_car_pos = loc_y_car - 25
	elif quad == 4:
		x_car_pos = loc_x_car -25
		y_car_pos = loc_y_car

	return x_car_pos, y_car_pos

############check if we are in a corner ###############

def check_corners(loc_x_car, loc_y_car):

	if loc_x_car == 25 and 	loc_y_car == 175:
		corner = True
	elif loc_x_car == 175 and loc_y_car == 175:
		corner = True
	elif loc_x_car == 175 and loc_y_car == 25:
		corner = True
	else:
		corner = False

	return corner

#######################################################
###### Maracar objeto y localizacion ##################
#######################################################

"""
def check_color(color):
	if color == rojo:
		orden = 1
	elif color == verde:
		orden = 2
	elif color == azul:
		orden = 3
	elif color == amarillo:
		orden = 4
	return orden
"""

def take_photo(name)
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        time.sleep(0.2)
        camera.capture(str(name)+'.jpg')


def check_prueba(color):
	if color == 1:
		num = 1
	elif color == 2:
		num = 2
	elif color == 3:
		num = 3
	elif color == 4:
		num = 4

	return num

def mapeo():

	mapea = True
	loc_x_car = 25 # coordenada inicial en y
	loc_y_car = 25 # coordenada inicual en x
	mapping = 0
	box_cord = [0] * 30
	order = 0
	num = 0
	color = -1

	while(mapea):

		quad = get_quad(loc_x_car, loc_y_car)
		corner = check_corners(loc_x_car, loc_y_car)
		time.sleep(0.5)
		if corner == True:
			gira(-190, 471.23889/2)
			mapping = mapping + 1

		#avanza(190, 25, lon)

		enci = motor1.read()
		encd = motor2.read()
		linea(0, 25, 130, enci, encd, dist)

		loc_x_car, loc_y_car = update_pos(quad, loc_x_car, loc_y_car)
		gira(-190, 471.23889/2) # gira para ver si hay caja

		take_photo(name)

		time.sleep(0.5)

		dis = sensor.read()

		if dis < 150:

			x_cor, y_cor, x_sup, y_sup, x_inf, y_inf = obj_pos(quad, loc_x_car, loc_y_car, 25, dis)
			color = color + 1
			order = color
			box_cord[order] = [x_cor, y_cor, x_sup, y_sup, x_inf, y_inf]

			print (box_cord)

		gira(190, 471.23889/2)
		time.sleep(0.5)

		if mapping == 4:
		    color = 0
		    mapea = False

mapeo()
