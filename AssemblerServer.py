#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 17:54:47 2018

@author: cap
"""

import time
import threading
#sudo chmod 666 /dev/ttyUSB0 
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
from AssemblerStation import _runPICK, _runPUT

# method to be exposed through server

def Pick(parent, Station):
    S = threading.Thread(target=_runPICK,args=(Revent,))
    S.start()
    print("Moving Robot")
    return [ua.Variant(4, ua.VariantType.Int32)]
def Put(parent, Station):
    C = threading.Thread(target=_runPUT,args=(Revent,))
    C.start()
    print("Moving Robot")
    return [ua.Variant(4, ua.VariantType.Int32)]

if __name__ == "__main__":
    # optional: setup logging
    logging.basicConfig(level=logging.WARN)

    # now setup our server
    server = Server()
    #server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
    server.set_endpoint("opc.tcp://172.17.17.105:4000/ASS/")
    server.set_server_name("Assembler Robot Server")

    # setup our own namespace
    uri = "http://cap.edu.co"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our custom stuff
    objects = server.get_objects_node()

    # populating our address space
    Services = objects.add_object(idx, "Services")
    
    RunRobot = Services.add_method(idx, "RunPICK", Pick, [ua.VariantType.Int32],[ua.VariantType.Int32])
    RunRobot = Services.add_method(idx, "RunPUT", Put, [ua.VariantType.Int32],[ua.VariantType.Int32])
    # Creating a custom event
    etype = server.nodes.base_event_type.add_object_type(2, 'fin')
    etype.add_property(2, 'State', ua.Variant(0, ua.VariantType.Int32))

    Revent = server.get_event_generator(etype, Services)

    # starting!
    server.start()
    print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
    try:
        print("Ready")
        embed()
    finally:
        server.stop()
