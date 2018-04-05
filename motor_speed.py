#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("/home/pi/bmw/libs")
import motorbk as motor
import math
import time
#motpin - pin del motor
#pulmot - pulsos leidos por el encoder del motor n

motori = motor.motorbk(7) #motor izquierdo
motord = motor.motorbk(6) #motor derecho



def get_pul_ini(motpin): # obtener pulsos iniciales para resetear

    pulsos_ini = motpin.read() # reset a los pulsos leidos
    return pulsos_ini


def motor_get_dist(motpin, pulmot): #distancias recorridas por motores en cm
   
    radio = 3 # radio de la llanta en  cm
    c = pi * 2 * radio # circunferencia  de la llanta en cm
    pulsos_act = motpin.read() - pulmot    #pulsos leídos restando los pulsos iniciales
    dist = pulsos_act * c / 600 # calcular distancia recorrida en base a los ppr - se da en cm
    return dist

"""
def main():

    while True:
       
        disti = motor_get_dist(motori, pulso_mi) #distancia recorrida por motor izquierdo
        distd = motor_get_dist(motord, pulso_md) #distancia recorrida por motor derecho
        print disti, distd
        
"""        
        
pulso_mi = get_pul_ini(motori) #pulso inicial motor izquierdo
pulso_md = get_pul_ini(motord) #pulso inicial motor derecho    


#####loop infinito
try:
    while(1):
        disti = motor_get_dist(motori, pulso_mi) #distancia recorrida por motor izquierdo
        distd = motor_get_dist(motord, pulso_md) #distancia recorrida por motor derecho
        #print disti, distd
        time.sleep(0.01) ##para no saturar
        
except (KeyboardInterrupt, SystemExit):
    pass



