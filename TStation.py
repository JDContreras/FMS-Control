#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 15:11:16 2017

@author: cap
"""
##sudo chmod 666 /dev/ttyS0
import time
"""
from osbrain import run_agent
from osbrain import run_nameserver
from osbrain import AgentAddress
"""

import serial
import RobotT
import API_CNC

#__cncPort = "COM4"
#__robotPort = "COM1"
__cncPort = "COM4"
__robotPort = "COM3"

"""
###############################################################################
instancia de modulo
###############################################################################
"""
try:
    port = serial.Serial(port = __robotPort, baudrate=9600, parity="O", bytesize=7, stopbits=2,xonxoff = True)
    R = RobotT._RobotT(port)
except serial.serialutil.SerialException as error:
    print("No se pudo conectar al puerto "+ __robotPort  +" para el robot. Asegurate de que este conectado y encendido")
    print("DETALLES: "+str(error))
except Exception as error:
    print("No se pudo conectar al puerto "+ __robotPort  +" para el robot. Asegurate de que este conectado y encendido")
    print("DETALLES: "+str(error))
t = API_CNC.cnc(port=__cncPort)


#time.sleep(10)


"""
###############################################################################
Enseñar posiciones del robot
###############################################################################
"""

def teachT():
    R.toT()
    R.waitT()
    R.pick()
    R.toPallet()

"""
###############################################################################
Configuraciones iniciarles
###############################################################################
"""

def ConfTStation():
    t.openclamp()
    t.opendoor()
    t.openclamp()
    t.closedoor()
    t.code("G28 U0 W0")
    t.opendoor()
    t.closeclamp()
    t.closeclamp()
    R.r.MO(400,"O")
    R.r.c.timeout = 30  #aumentar timeout a 30 segundos
    #R.r.MO(100,"O")

def RunTStation(TEvent, NPieza):
    """
    ###############################################################################
    Secuencia para fabricar una pieza en el Torno
    ###############################################################################
    """
    ###############################################################################
    #mover pieza del pallet al cm
    t.opendoor()
    t.openclamp()
    time.sleep(1)
    R.run_toT()#14
    ###############################################################################
    #esperar hasta que termine
    """
    R.r.c.reset_input_buffer()
    poi = R.r.c.read(1)
    print(poi)
    """

    ###############################################################################
    #Cerrar la mordaza del cm y esperar a que agarre
    t.closeclamp()
    time.sleep(2)
    ###############################################################################
    #sacar brazo del torno
    R.run_waitT() #4
    ###############################################################################
    #espera que salga el brazo

    """R.r.c.reset_input_buffer()
    poi = R.r.c.read(1)
    print(poi)
    """

    ###############################################################################
    #cerrar la puerta  cuando el brazo este afuera
    t.closedoor()
    time.sleep(2)  #hay que esperar a que cierre antes de seguir
    ###############################################################################
    #enviar el programa para que se fabrique la pieza
    #recordar que esto debe ser de acuerdo a base de datos y rfid

    if NPieza == 1:
        t.nc("NC/cadcam.NC")
        #t.nc("NC/E2T.NC")
        print("OK1")
    elif NPieza == 2:
        #t.nc("NC/E3T.NC")
        t.nc("NC/cadcam.NC")
        print("OK3")
    else:
        #t.nc("NC/EJE.NC")
        print("OK3")


    ch = 0
    ###############################################################################
    #esto envia comando de abrir puerta 200 veces para llenar buffer,
    while ch < 100:
        t.code("M38")
        ch = ch +1
    time.sleep(1)  #esperar suficiente para que se termine en programa antes de mandar el robot
                    #a futuro hacerlo con la salida digital del cnc
    ###############################################################################
    #mandar al robot a desmontar la pieza
    R.run_pick() #5
    ###############################################################################
    #espera que  el brazo este en posicion
    """
    R.r.c.reset_input_buffer()
    poi = R.r.c.read(1)
    print(poi)
    """

    ###############################################################################
    #abrir la sujecion
    t.openclamp()
    time.sleep(2)
    ###############################################################################
    #Llevar la pieza al pallet

    R.run_toPallet() #11

    ###############################################################################
    #enviar evento al coordinador
    t.closeclamp()
    TEvent.event.State = 1
    TEvent.trigger()
    print("trigget")

ConfTStation()
