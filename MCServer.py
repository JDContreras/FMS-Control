#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 15:11:16 2017

@author: cap
"""
##sudo chmod 666 /dev/ttyS0
import sys
sys.path.insert(0, "..")
import logging

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()

from opcua import ua, uamethod, Server

import time

import threading
from MCStation_FIX import RunMCStation, ConfMCStation
Check = True

def abrir():
    ConfMCStation()

def run(sender,N):
    #metodo de opc ua
    #ejecurtar el proceso de la maquina
    N=N.Value
    t = threading.Thread(target=RunMCStation, args=(event,N))
    t.start()
    print("ready")
    return [ua.Variant(1,ua.VariantType.Int32)]



if __name__ == "__main__":


    logging.basicConfig(level=logging.WARN)

    server = Server()
    server.set_endpoint("opc.tcp://192.168.0.107:4841/MC/")
    server.set_server_name("MCStation")

    # setup our own namespace
    uri = "http://MCStation.javerianacali.edu.co"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our custom stuff
    objects = server.get_objects_node()

    # populating our address space
    Services = objects.add_object(idx, "Services")
    RunfMC_method = Services.add_method(idx, "RunMC", run,[ua.VariantType.Int32],[ua.VariantType.Int32])
    etype = server.create_custom_event_type(idx, 'fin')
    etype.add_property(2,"State",ua.Variant(0,ua.VariantType.Int32))
    event = server.get_event_generator(etype, Services)
    # starting!
    try:
        server.start()
    except Exception as error:
        print("\n\n\n[ERROR]Fue imposible conectarse a la ip asgignada. Verifica la IP")
        print("[ERROR] "+str(error))
        print("\t----------------SE RECOMIENDA REINICIAR EL PROGRAMA------------\n\n")
    print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
    try:
        embed()
    except Exception as error:
        print("[ERROR] Error general")
        print("[ERROR] "+str(error))
    finally:
        server.stop()
