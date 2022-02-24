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

def OrderProduct(sender, ID):
    ID = ID.Value
    
    print(ID)
    return [ua.Variant(1,ua.VariantType.Int32)]
"""
################################################################################
Inicio del programa
################################################################################
"""
if __name__ == "__main__":

        
        """
        ################################################################################
        creacion del servidor
        ################################################################################
        """
        # now setup our server
        server = Server()
        #server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
        server.set_endpoint("opc.tcp://172.17.16.140:4000/Control/")
        server.set_server_name("Control Manual")
        uri = "http://cap.edu.co"
        idx = server.register_namespace(uri)
        objects = server.get_objects_node()
        Services = objects.add_object(idx, "Services")
        Variables = objects.add_object(idx, "Variables")
     

        Ordenar = Services.add_method(idx, "Ordenar", OrderProduct, [ua.VariantType.Int32],[ua.VariantType.Int32])
        """
        ################################################################################
        Variables
        ################################################################################
        """
        pedidos = Variables.add_variable(idx, "pedidos", 10)
        fabricando = Variables.add_variable(idx, "fabricando", 6)
        terminadas = Variables.add_variable(idx, "terminadas", 5)
        
        """
        ################################################################################
        inicio del servidor
        ################################################################################
        """
        server.start()
        print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
        
        embed()
