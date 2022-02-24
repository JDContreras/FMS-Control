#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 17:44:04 2018

@author: controlcap2
"""

import telnetlib
import time
import numpy as np
import threading 

class ASRS_Control:
    
    def __init__(self, Event, IP = '192.168.200.12', PORT = 4000):
         self.PORT = PORT
         self.IP = IP
         self.s = telnetlib.Telnet(self.IP, self.PORT)
         self.BUFFER_SIZE = 1024
         self.M = np.zeros((5,5))
         #self.M[0] = [1, 1, 1, 1, 1]
         self.P = np.zeros((5,5))
         self.F = np.array([])
         self.event = Event
         
    def waitFin(self):
        letra = self.s.read_until(b"DONE\r\n")
        return letra
    def PUT(self):
        self.F = np.append(self.F,1)
        print("Orden de poner pallet agregada: "+str(self.F))
        
    def PICK(self):
        self.F = np.append(self.F,2)
        print("Orden de recoger pallet agregada: "+str(self.F))
     
        
    def free(self, K):
        for i in range(5):
            for j in range(5):
                print(i,j)
                print(K[i,j])
                if K[i,j] == 0:
                    return i , j
                
    def RunPUT(self):
        s = self.s
        
        i,j = self.free(self.M)
        MESSAGE = "m2c{}".format(str(i+1)+str(j+1))+"\n"
        s.write(MESSAGE.encode())
        s.read_until(b"DONE\r\n")
        self.M[i,j] = 1 
        
               
    def RunPICK(self):
        event, s = self.event, self.s
        MESSAGE1 = "waitPRODUCT"+"\n"
        s.write(MESSAGE1.encode())
        s.read_until(b"DONE\r\n")
        print("IN CONVEYOR")
        event.event.State = 5
        event.trigger()
        time.sleep(8)
        print("trigget")
        i,j = self.free(self.P)
        MESSAGE1 = "c2p{}".format(str(i+1)+str(j+1))+"\n"
        s.write(MESSAGE1.encode())
        s.read_until(b"DONE\r\n")
        self.P[i,j] = 1
        
    def ASRSManager(self):
        while True:
            time.sleep(2)           
            if self.F.size == 0:
                ll = 1
                
            elif self.F[0] == 1:
                print("running PUT")
                self.RunPUT()
                self.F = np.delete(self.F,0)
                
            elif self.F[0] == 2:
                print("running Pick")
                self.RunPICK()
                self.F = np.delete(self.F,0)
        
    def runASRS(self):
        t1 = threading.Thread(target=self.ASRSManager)
        t1.start()
        

