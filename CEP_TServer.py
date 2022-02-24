#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 16:25:52 2018

@author: controlcap2
"""

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
import threading
from CEP_TStation import RunTStation  




A = 0
def run(sender,N):
    #ejecutar manufactura en torno
    global A
    t = threading.Thread(target=RunTStation, args=(event,A,))
    t.start()
    A = A+1
    
    print("ready")
    return [ua.Variant(1,ua.VariantType.Int32)]


if __name__ == "__main__":

    logging.basicConfig(level=logging.WARN)

    server = Server()
    server.set_endpoint("opc.tcp://192.168.200.100:8080/T/")
    server.set_server_name("TStation")

    # setup our own namespace
    uri = "http://TStation/.javerianacali.edu.co"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our custom stuff
    objects = server.get_objects_node()

    # populating our address space

    Services = objects.add_object(idx, "Services")
    RunT_method = Services.add_method(idx, "RunT", run,[ua.VariantType.Int32],[ua.VariantType.Int32])
    
    #Evento
    etype = server.create_custom_event_type(idx, 'fin')
    etype.add_property(2,"State",ua.Variant(0,ua.VariantType.Int32))
    event = server.get_event_generator(etype, Services)
    
    # starting!
    server.start()
    print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
    try:
        embed()
    finally:
        server.stop()