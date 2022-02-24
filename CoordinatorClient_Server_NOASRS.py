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


from opcua import Client, Server
from opcua import ua


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
        RunMC.call_method("2:RunMC",2)       
    elif N == 3:
        #RunQC.call_method("2:RunQC",3)
        RunC.call_method("2:Piston",2)
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

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    #logger = logging.getLogger("KeepAlive")
    #logger.setLevel(logging.DEBUG)
    MC = Client("opc.tcp://192.168.200.101:4841/MC/")
    T = Client("opc.tcp://192.168.200.101:8000/T/")
    #ASRS = Client("opc.tcp://192.168.200.100:4842/ASRS/")
    Transport = Client("opc.tcp://192.168.200.100:4840/ARD/")
    #QC = Client("opc.tcp://192.168.200.100:8080/QC/")
    ASS = Client("opc.tcp://192.168.200.100:4000/ASS/")
    # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
    try:
        
       
        """
        Conexion a servidor de transporte
        """
        Transport.connect()
        rootC = Transport.get_root_node()
        # entrar a servicios
        RunC = rootC.get_child(["0:Objects", "2:Services"])

        """
        Conexion a servidor de Machine center
        """
        MC.connect()
        rootMC = MC.get_root_node()
        # entrar a servicios
        RunMC = rootMC.get_child(["0:Objects", "2:Services"])
      
        
        """
        Conexion a servidor de Lathe
        """
        T.connect()
        rootT = T.get_root_node()
        # entrar a servicios
        RunT = rootT.get_child(["0:Objects", "2:Services"])
        
        """
        Conexion a servidor ASRS
        
        ASRS.connect()
        rootASRS = ASRS.get_root_node()
        # entrar a servicios
        RunASRS = rootASRS.get_child(["0:Objects", "2:Services"])
        
       
        Conexion a servidor QC
        """
        #QC.connect()
        #rootQC = QC.get_root_node()
        # entrar a servicios
        #RunQC = rootQC.get_child(["0:Objects", "2:Services"])
        
        
        """
        Conexion a servidor ASS robot de ensamble
        """
        ASS.connect()
        rootASS = ASS.get_root_node()
        # entrar a servicios
        RunASS = rootASS.get_child(["0:Objects", "2:Services"])               

        """
        Crear servidor
        """
        # now setup our server
        server = Server()
        #server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
        server.set_endpoint("opc.tcp://192.168.200.101:4001/Control/")
        server.set_server_name("Control Manual")
        uri = "http://cap.edu.co"
        idx = server.register_namespace(uri)
        objects = server.get_objects_node()
        Services = objects.add_object(idx, "Services")
        Estaciones = Services.add_method(idx, "Estaciones", RunStations2, [ua.VariantType.Int32],[ua.VariantType.Int32])
        Pistones = Services.add_method(idx, "Pistones", RunPiston2, [ua.VariantType.Int32],[ua.VariantType.Int32])
        
        server.start()
        print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
        
        embed()
        
    finally:
        Transport.disconnect()
        MC.disconnect()
        T.disconnect()
        #ASRS.disconnect()
        ASS.disconnect()
        #QC.disconnect()