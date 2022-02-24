#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 18:04:39 2018

@author: cap
"""
def VIRU(Event):
    Event.event.Message = ua.LocalizedText("SENSOR: OK")
    Event.event.State = 2
    Event.trigger()
    print("trigged")