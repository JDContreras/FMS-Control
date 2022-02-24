#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 09:29:04 2018

@author: cap
"""
#2-5
#3-4
#4-3
#5-2

#2-5
import sys
sys.path.insert(0, "..")
import logging
import time
import threading
import numpy as np

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()
        
        


from opcua import Client, Server
from opcua import ua

class orders:
    
    def __init__(self):
         self.OL = np.array([])
         self.OMC = np.array([])
         self.entradas = 0
         self.terminadas = 0
         self.pendientes = self.entradas - self.terminadas
         
         
    def CreateOrder(self,N):
        self.entradas = self.entradas + 1
        self.OL = np.append(self.OL,N)
        self.OMC = np.append(self.OMC,N)
        self.pendientes = self.entradas - self.terminadas
        #RunASRS.call_method("2:RunPUT",0)
        print("Orden agregada para el producto " + str(N))
        
    def DeleteOL(self):
        self.OL = np.delete(self.OL,0)
      
    def DeleteOMC(self):
        self.OMC = np.delete(self.OMC,0)
        
    def DeleteOrder(self):
        self.terminadas = self.terminadas + 1
        self.pendientes = self.entradas - self.terminadas
        
    def GetPendientes(self):
        return self.pendientes
                
    def GetOL(self):
        return self.OL[0]

    def GetOMC(self):
        return self.OMC[0]

"""
#########################
ADMINISTRADOR DE ORDENES
#########################
"""

om = orders()

"""
################################################################################
metodos control automatico
################################################################################
"""


def RunPiston(N):
    if N == 1:
        print("1")
        try:
            om.DeleteOL()
        except:
            print("no hay elementos a borrar")
        RunC.call_method("2:Piston",1)
    elif N == 2:
        print("2")
        try:
            om.DeleteOMC()
        except:
            print("no hay elementos a borrar")
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
        
def RunStations(N):     
    if N == 1:
        #RunT.call_method("2:RunT",1)
        try:
            O = om.GetOL()
            RunT.call_method("2:RunT",O)
            
        except:
            print("no hay elementos en cola")
            RunC.call_method("2:Piston",1)
        
    elif N == 2:
        #RunMC.call_method("2:RunMC",2)
        try:
            O = om.GetOMC()
            #RunMC.call_method("2:RunMC",O)
            RunC.call_method("2:Piston",2)
        except:
            print("no hay elementos en cola")
            RunC.call_method("2:Piston",2)
             
    elif N == 3:
        #RunQC.call_method("2:RunQC",3)
        RunC.call_method("2:Piston",3)
    elif N == 4:
        RunASS.call_method("2:RunPICK",4)
    elif N == 5:
        #RunASRS.call_method("2:RunPICK",11)
        om.DeleteOrder()
        ter = om.terminadas
        server.set_attribute_value(terminadas.nodeid, ua.DataValue(ter))
        pen = om.pendientes
        server.set_attribute_value(fabricando.nodeid, ua.DataValue(pen))
        #RunASRS.call_method("2:RunPICK",5)
    else:
        print("Nothing to do here")

def OrderProduct(sender, ID):
    ID = ID.Value
    t = threading.Thread(target=om.CreateOrder, args=(ID,))
    t.start()
    ped = om.entradas
    
    server.set_attribute_value(pedidos.nodeid, ua.DataValue(ped))
    pen = om.pendientes
    server.set_attribute_value(fabricando.nodeid, ua.DataValue(pen))
    print("ready")
    return [ua.Variant(1,ua.VariantType.Int32)]
    

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
        
"""
################################################################################
Metodos para el control manual
################################################################################
"""

def RunPiston2(master,N):
    N = N.Value
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
        
        
def RunStations2(N,call): 
    print(N)
    print(call)
    N = call.Value  
    print(N)
    if N == 1:
        #RunT.call_method("2:RunT",1)
        RunT.call_method("2:RunT",1)
    elif N == 2:
        #RunMC.call_method("2:RunMC",2)
        #RunMC.call_method("2:RunMC",2)  
        RunC.call_method("2:Piston",2)
    elif N == 3:
        #RunQC.call_method("2:RunQC",3)
        RunC.call_method("2:Piston",3)
    elif N == 41:
        RunASS.call_method("2:RunPICK",4)
    #elif N == 5:
        #RunASRS.call_method("2:RunPICK",11)
        #RunASRS.call_method("2:RunPICK",5)
    #elif N == 0:
        #RunASRS.call_method("2:RunPICK",11)
        #RunASRS.call_method("2:RunPUT",0)
    elif N == 42:
        #RunASRS.call_method("2:RunPICK",11)
        RunASS.call_method("2:RunPUT",6)
    else:
        print("Nothing to do here")
        
        
def _RunPiston2(parent, Station):
    print(Station)
    StationN = Station.Value
    print(StationN)
    t = threading.Thread(target=RunPiston2,args=(StationN,))
    t.start()
    print("Ejecutado")
    return [ua.Variant(1, ua.VariantType.Int32)]

def _RunStations2(parent, Station):
    print(Station)
    StationN = Station.Value
    print(StationN)
    g = threading.Thread(target=RunStations2,args=(StationN,))
    g.start()
    print("Ejecutado")
    return [ua.Variant(1, ua.VariantType.Int32)]

"""
################################################################################
Inicio del programa
################################################################################
"""
if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    #logger = logging.getLogger("KeepAlive")
    #logger.setLevel(logging.DEBUG)
    MC = Client("opc.tcp://192.168.200.101:4841/MC/")
    T = Client("opc.tcp://192.168.200.101:8000/T/")
    #ASRS = Client("opc.tcp://192.168.200.100:4842/ASRS/")
    #8.19
    Transport = Client("opc.tcp://192.168.200.100:4840/ARD/") #192.168.200.100:4840
    #QC = Client("opc.tcp://192.168.200.100:8080/QC/")
    ASS = Client("opc.tcp://192.168.200.100:4000/ASS/")
    # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
   
        
    try: 
        """
        Conexion a servidor de Machine center
         """
        MC.connect()
        rootMC = MC.get_root_node()
        # entrar a servicios
        RunMC = rootMC.get_child(["0:Objects", "2:Services"])
        # entrar a eventos
        MCEvent = rootMC.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "2:fin"])


        """
        Conexion a servidor de Lathe
        """
        T.connect()
        rootT = T.get_root_node()
        # entrar a servicios
        RunT = rootT.get_child(["0:Objects", "2:Services"])
        # entrar a eventos
        TEvent = rootT.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "2:fin"])


        
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
        deja
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


        
        
        RunPiston(1)
        time.sleep(0.5)
        RunPiston(2)
        time.sleep(0.5)
        RunPiston(3)
        time.sleep(0.5)
        RunPiston(4)
        time.sleep(0.5)
        RunPiston(5)
        time.sleep(0.5)
        RunPiston(1)
        time.sleep(0.5)
        RunPiston(2)
        time.sleep(0.5)
        RunPiston(3)
        time.sleep(0.5)
        RunPiston(4)
        time.sleep(0.5)
        RunPiston(5)
        time.sleep(0.5)
        
        """
        ################################################################################
        creacion del servidor
        ################################################################################
        """
        # now setup our server
        server = Server()
        #server.set_endpoint("opc.tcp://172.17.20.94:4000/Control/")
        server.set_endpoint("opc.tcp://192.168.200.101:4000/Control/")
        server.set_server_name("Contro lserver")
        uri = "http://cap.edu.co"
        idx = server.register_namespace(uri)
        objects = server.get_objects_node()
        Services = objects.add_object(idx, "Services")
        Variables = objects.add_object(idx, "Variables")
        """
        ################################################################################
        Servicios
        ################################################################################
        """
        Estaciones = Services.add_method(idx, "Estaciones", RunStations2, [ua.VariantType.Int32],[ua.VariantType.Int32])
        Pistones = Services.add_method(idx, "Pistones", RunPiston2, [ua.VariantType.Int32],[ua.VariantType.Int32])
        Ordenar = Services.add_method(idx, "Ordenar", OrderProduct, [ua.VariantType.Int32],[ua.VariantType.Int32])
        """
        ################################################################################
        Variables
        ################################################################################
        """
        pedidos = Variables.add_variable(idx, "pedidos", 0)
        fabricando = Variables.add_variable(idx, "fabricando", 0)
        terminadas = Variables.add_variable(idx, "terminadas", 0)
        
        """
        ################################################################################
        inicio del servidor
        ################################################################################
        """
        server.start()
        print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
        
        embed()
        
    finally:
        T.disconnect()
        MC.disconnect()
        
        #ASRS.disconnect()

       # QC.connect()