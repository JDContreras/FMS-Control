#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 09:29:04 2018

@author: cap
"""

import sys
sys.path.insert(0, "..")
import logging
import time
import threading

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()


from opcua import Client
from opcua import ua

def RunPiston(N):
    if N == 1:
        print("1")
        RunC.call_method("2:Piston",1)
    elif N == 2:
        print("2")
        RunC.call_method("2:Piston",2)
    elif N == 3:
        print("3")
        RunC.call_method("2:Piston",3)
    elif N == 4:
        print("4")
        RunC.call_method("2:Piston",4)
    elif N == 5:
        print("5")
        RunC.call_method("2:Piston",5)
    else:
        print("Nothin to show",N)

def VIRU(state):
    print("quitando viruta")  
    time.sleep(20)
    RunC.call_method("2:Piston",2)
    print("trigged")  

def CAM(state):
    print("camara")  
    time.sleep(20)
    RunC.call_method("2:Piston",3)
    print("trigged")

def LAST(state):
    print("Fin")  
    time.sleep(20)
    RunC.call_method("2:Piston",5)
    print("trigged")      
    
def RunStations(N):     
    if N == 1:
        RunT.call_method("2:RunT",1)
    elif N == 2:
        VIRUTA = threading.Thread(target=VIRU,args=(N,))
        VIRUTA.start()
        #TF.call_method("2:RunT")        
    elif N == 3:
        C = threading.Thread(target=CAM,args=(N,))
        C.start()
    elif N == 4:
        RunASS.call_method("2:RunRobot",4)
    elif N == 5:
        F = threading.Thread(target=LAST,args=(N,))
        F.start()
    else:
        print("Nothing to do here")

class Stations(object):

    def event_notification(self, event):
        StS = event.State
        tf = threading.Thread(target=RunPiston,args=(StS,))
        tf.start()

            
class SubHandlerC(object):

    def event_notification(self, event):
        StS = event.State
        tf = threading.Thread(target=RunStations,args=(StS,))
        tf.start()

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    #logger = logging.getLogger("KeepAlive")
    #logger.setLevel(logging.DEBUG)
    #MC = Client("opc.tcp://192.168.200.102:4840/MC/")
    #QC = Client("opc.tcp://192.168.200.102:8080/QC/")
    T = Client("opc.tcp://192.168.200.100:8080/T/")
    #ASRS = Client("opc.tcp://192.168.200.100:4840/ASRS/")
    Transport = Client("opc.tcp://192.168.200.103:4840/ARD/")
    ASS = Client("opc.tcp://192.168.200.103:4000/ASS/")
    # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
    try:
        
        Transport.connect()
        """
        Conexion a servidor de transporte
        """
        rootC = Transport.get_root_node()
        # entrar a servicios
        RunC = rootC.get_child(["0:Objects", "2:Services"])
        # entrar a eventos
        SensorEvent = rootC.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "2:Sensor"])
        mscltC = SubHandlerC()
        subC = Transport.create_subscription(100, mscltC)
        handleC = subC.subscribe_events(RunC, SensorEvent)

        
        
        msclt = Stations()  #conexion para todas las estaciones que dependen de los pistones
        

        
        """
        Conexion a servidor de Lathe
        """
        T.connect()
        rootT = T.get_root_node()
        # entrar a servicios
        RunT = rootT.get_child(["0:Objects", "2:Services"])
        # entrar a eventos
        TEvent = rootT.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "2:fin"])
        subT = T.create_subscription(100, msclt)
        handleT = subT.subscribe_events(RunT, TEvent)
        
        """
        Conexion a servidor ASRS
        
        ASRS.connect()
        rootASRS = ASRS.get_root_node()
        # entrar a servicios
        RunASRS = rootASRS.get_child(["0:Objects", "2:Services"])
        # entrar a eventos
        ASRSEvent = rootASRS.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "2:fin"])
        subASRS = ASRS.create_subscription(100, msclt)
        handleASRS = subASRS.subscribe_events(RunASRS, ASRSEvent)
        #RunASRS.call_method("2:RunPUT",11)
        
        Conexion a servidor QC
        
        QC.connect()
        rootQC = QC.get_root_node()
        # entrar a servicios
        RunQC = rootQC.get_child(["0:Objects", "2:Services"])
        # entrar a eventos
        QCEvent = rootQC.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "2:fin"])
        subQC = QC.create_subscription(100, msclt)
        handleQC = subQC.subscribe_events(RunQC, QCEvent)
        
        """
        """
        Conexion a servidor ASS robot de ensamble
        """
        ASS.connect()
        rootASS = ASS.get_root_node()
        # entrar a servicios
        RunASS = rootASS.get_child(["0:Objects", "2:Services"])
        # entrar a eventos
        ASSEvent = rootASS.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "2:fin"])
        subASS = ASS.create_subscription(100, msclt)
        handleASS = subASS.subscribe_events(RunASS, ASSEvent)
        
        
        RunPiston(1)
        time.sleep(2)
        RunPiston(2)
        time.sleep(2)
        RunPiston(3)
        time.sleep(2)
        RunPiston(4)
        time.sleep(2)
        RunPiston(5)
        time.sleep(2)

        embed()
        
    finally:
        Transport.disconnect()
        T.disconnect()
        #ASRS.disconnect()
        ASS.disconnect()
        #QC.disconnect()