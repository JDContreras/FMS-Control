# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 12:13:34 2018

@author: cap
"""
import time


import serial
import RobotMC_KEYS
import time
import API_CNC
from opcua import ua

"""
###############################################################################
instancia de modulo
###############################################################################
"""
__robPort = "COM6"
__mcPort = "COM5"
#Este puerto es el 6
try:
    port = serial.Serial(port = __robPort, baudrate=9600, parity="O", bytesize=7, stopbits=2,xonxoff = False)
    R = RobotMC_KEYS._RobotMC(port)
except serial.serialutil.SerialException as error:
    print("[ERROR] No se pudo conectar al puerto "+ __robPort  +" para el robot. Asegurate de que este conectado y encendido")
    print("DETALLES: "+str(error))
mc = API_CNC.cnc(port=__mcPort)   #el control de flujo por software no esta funcionando para el ttyUSB0


"""
###############################################################################
Configuracion del robot, predefinir secuencias
###############################################################################
"""
#solo se debe crear una ves y sobre escribir si se cambia alguna posicion
#M.mount_comand()
#M.wait_mc_comand()
#M.unmount()
#M.put_in_pallet()

"""
###############################################################################
Enseñar rutina robot
###############################################################################
"""
def teachMC():
    R.M1()
    R.M2()
    R.M3()
    R.M4()

"""
###############################################################################
Condiciones iniciales
###############################################################################
"""
def ConfMCStation():
    mc.closedoor()
    R.r.MO(550,"O")
    mc.closedoor()
    mc.code("G28 X0 Y0")
    mc.openclamp()
    mc.opendoor()
    mc.openclamp()
    mc.opendoor()
    R.r.c.timeout = 50  #aumentar timeout a 50 segundos


def RunMCStation(MCEvent,N):

    """
    ###############################################################################
    Secuencia para fabricar una pieza en el centro de mecanizado
    ###############################################################################
    """
    #mover pieza del pallet al cm
    R.runM1() #17
    time.sleep(2)
    ###############################################################################
    #Cerrar la mordaza del cm y esperar a que agarre
    mc.closeclamp()
    time.sleep(2)
    ###############################################################################
    #sacar brazo del torno
    R.runM2()
    
    ###############################################################################
    #cerrar la puerta  cuando el brazo este afuera
    mc.closedoor()
    time.sleep(1)  #hay que esperar a que cierre antes de seguir
    ###############################################################################
    #enviar el programa para que se fabrique la pieza
    #recordar que esto debe ser de acuerdo a base de datos y rfid

    if N == 1:
        #mc.nc("NC/BOTELLA.NC")
        mc.nc("NC/E2F.NC")
    elif N==2:
        mc.nc("NC/E3F.NC")
    else:
        mc.nc("NC/EJE.NC")
    time.sleep(3)  #esperar suficiente para que se termine en programa antes de mandar el robot
                    #a futuro hacerlo con la salida digital del cnc

    mc.opendoor()
    ###############################################################################
    #esto envia comando de abrir puerta 200 veces para llenar buffer,
    ch = 0
    while ch < 20:
        mc.code("M11")
        ch = ch +1
    time.sleep(1)  #esperar suficiente para que se termine el programa antes de mandar el robot
                    #a futuro hacerlo con la salida digital del cnc
    ###############################################################################
    #mandar al robot a desmontar la pieza
    R.runM3()

    ###############################################################################
    #abrir la sujecion
    mc.openclamp()
    time.sleep(2)
    ###############################################################################
    #Llevar la pieza al pallet
    R.runM4()
    time.sleep(1)
    ###############################################################################
    #Activar evento para que el coordinador sepa que ya termino
    MCEvent.event.Message = ua.LocalizedText("OK")
    MCEvent.event.State = 2
    MCEvent.trigger()
    print("Trigget")

ConfMCStation()
