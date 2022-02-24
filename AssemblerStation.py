#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 17:44:46 2018

@author: cap
"""
import serial

from RobotAssembler import _RobotAssembler
from opcua import ua
port = serial.Serial(port = "COM1", baudrate=9600, parity="O", bytesize=7, stopbits=2,xonxoff = False)
R = _RobotAssembler(port)
R.r.c.timeout=20
R.PICK()
R.PUT()
def _runPICK(Revent):
    R.r.c.reset_input_buffer()
    R.runPICK()
    R.r.c.read(1)
    print("Fin")

def _runPUT(Revent):
    R.r.c.reset_input_buffer()
    R.runPUT()
    R.r.c.read(1)
    Revent.event.Message = ua.LocalizedText("OK")
    Revent.event.State = 4
    Revent.trigger()
    print("trigget")   
    
    #R.r.RS()