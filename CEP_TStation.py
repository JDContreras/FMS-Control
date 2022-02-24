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

__cncPort = "COM4"
__robotPort = "COM1"

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
 
     
def RunTStation(TEvent,A):
    """
    ###############################################################################
    Secuencia para fabricar una pieza en el Torno
    ###############################################################################
    """
    ###############################################################################
    #mover pieza del pallet al cm
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
    ###############################################################################
    #enviar e
    
    #l programa para que se fabrique la pieza
    #recordar que esto debe ser de acuerdo a base de datos y rfid
    lot = [8, 6, 2, 2, 2, 6, 0, 3, 2, 0, 0, 2, 0, 1, 0, 0, 2, 6, 2, 1, 0, 0, 6, 10, 0, 2, 6, 3, 2, 3]
    #lot =[3, 6, 2, 0, 2, 4, 2, 2, 7, 2, 0, 10, 6, 4, 7, 2, 2, 3, 2, 6, 0, 7, 3, 10, 6, 2, 9, 1, 6, 2]
    #[2, 0, 6, 2, 0, 2, 3, 0, 7, 0, 1, 2, 6, 0, 0, 6, 6, 2, 2, 3, 7, 0, 3, 1, 0, 2, 10, 7, 3, 1]
    #[7, 1, 0, 2, 2, 0, 2, 0, 0, 0, 2, 3, 6, 3, 2, 0, 3, 0, 2, 8, 2, 0, 7, 2, 2, 2, 0, 1, 2, 0]
    
    """
    Total piezas: 120
    piezas defectuosas: 45
    piezas por lote: 30
    numero de lotes: 4
    tipo 0  = 12-19,30
    suma 30
    tipo 1 = 12.5-19.5
    tipo 2 = 11.5-18.5
    suma 55
    tipo 3 = 12.7-19.7
    tipo 4 = 11.3-18.3
    suma 15
    tipo 5 = 13-20..
    tipo 6 = 11-18
    suma 15
    tipo 7 = 13.5-20.5
    tipo 8 = 10.5-17.5
    suma 10
    tipo 9 = 14-21
    tipo 10 = 10-17
    suma5
    """
    print(A)
    NF = lot[A]
    if NF == 0:
        file = "F0.NC"
    elif NF == 1:
        file = "F1.NC"
    elif NF == 2:
        file = "F2.NC"
    elif NF == 3:
        file = "F3.NC"
    elif NF == 4:
        file = "F4.NC"
    elif NF == 5:
        file = "F5.NC"
    elif NF == 6:
        file = "F6.NC"
    elif NF == 7:
        file = "F7.NC"
    elif NF == 8:
        file = "F8.NC"
    elif NF == 9:
        file = "F9.NC"
    elif NF == 10:
        file = "F10.NC"
    t.nc("CEP_NC_FILES/"+file)
    print(file)
    
    ch = 0
    ###############################################################################
    #esto envia comando de abrir puerta 200 veces para llenar buffer, 
    while ch < 150:
        t.code("M38")
        ch = ch +1
    time.sleep(1)  #esperar suficiente para que se termine en programa antes de mandar el robot
                    #a futuro hacerlo con la salida digital del cnc
    ###############################################################################
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

    
