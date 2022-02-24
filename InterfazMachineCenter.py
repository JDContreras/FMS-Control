# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 11:11:45 2018

@author: juandavid.contreras
"""
from API_CNC import cnc
from tkinter import *
import tkinter as tk
import time
from tkinter import messagebox
root = Tk()
root.title("CNC Control")
"""
##############################################################################
Funciones
##############################################################################
"""
dnc = cnc("COM1")
A = 0
V= 0

def update():
    global A
    global V
    A = int(Dis.get())
    V = int(Vel.get())
    print("parametros actualizados")
    print("mm por click = " + str(A))
    print("Velocidad de avance = " + str(V))
    dnc.code("F%s" % V)
    
def moveX():
    global A
    dnc.code("G01 U%s" % A)
    time.sleep(0.2)
    
def moveY():
    global A
    dnc.code("G01 V%s" % A)
    time.sleep(0.2)
    
def moveZ():
    global A
    dnc.code("G01 W%s" % A)
    time.sleep(0.2)

def moveXn():
    global A
    dnc.code("G01 U-%s" % A)
    time.sleep(0.2)
    
def moveYn():
    global A
    dnc.code("G01 V-%s" % A)
    time.sleep(0.2)
    
def moveZn():
    global A
    dnc.code("G01 W-%s" % A)
    time.sleep(0.2) 
    
def moveXK(event):
    global A
    dnc.code("G01 U%s" % A)
    time.sleep(0.2)
    
def moveYK(event):
    global A
    dnc.code("G01 V%s" % A)
    time.sleep(0.2)
    
def moveZK(event):
    global A
    dnc.code("G01 W%s" % A)
    time.sleep(0.2)

def moveXnK(event):
    global A
    dnc.code("G01 U-%s" % A)
    time.sleep(0.2)
    
def moveYnK(event):
    global A
    dnc.code("G01 V-%s" % A)
    time.sleep(0.2)
    
def moveZnK(event):
    global A
    dnc.code("G01 W-%s" % A)
    time.sleep(0.2)    
    
def homeX():
    result = messagebox.askquestion("Confirmar", "¿Esta seguro de enviar el eje X a home?", icon='warning')
    if result == 'yes':
        dnc.code("G91 G28 X0")
        time.sleep(0.2)
    else:
        print ("Cancelado")
    
    
def homeY():
    result = messagebox.askquestion("Confirmar", "¿Esta seguro de enviar el eje X a home?", icon='warning')
    if result == 'yes':
        dnc.code("G91 G28 Y0")
        time.sleep(0.2)
    else:
        print ("Cancelado")
    
def homeZ():
    result = messagebox.askquestion("Confirmar", "¿Esta seguro de enviar el eje X a home?", icon='warning')
    if result == 'yes':
        dnc.code("G91 G28 Z0")
        time.sleep(0.2)
    else:
        print ("Cancelado")
    
def tool():
    result = messagebox.askquestion("Confirmar", "¿Esta seguro de cambiar herramienta?", icon='warning')
    if result == 'yes':
        T = Tool.get()      
        dnc.code("M6 T%s" % T)
        time.sleep(0.2)
    else:
        print ("Cancelado")

def NewWin():
    newWindow = Toplevel(root) 
    newWindow.bind("<Left>", moveXK)
    newWindow.bind("<Right>", moveXnK)
    newWindow.bind("<Up>", moveYnK)
    newWindow.bind("<Down>", moveYK)
    newWindow.bind("<KeyPress-a>", moveZK)
    newWindow.bind("<KeyPress-z>", moveZnK)       
    
def SendFile():
    File = Name.get()
    print(File)
    cnc.nc(File)
    
    
    
   
"""
##############################################################################
Cuadro de funciones de control codigos M
##############################################################################
"""
fcontrol = LabelFrame(root, text= "Funciones de Control",pady=5,padx=5)  
fcontrol.grid(row=0, column = 0,ipadx=5,ipady=5,pady=5,padx=5)

#Widgets
W1=20
H1=6
Open = Button(fcontrol, text="Abrir Puerta", width = W1, height = H1,command = dnc.abrirpuerta)
Close = Button(fcontrol, text="Cerrar Puerta",width = W1, height = H1,command = dnc.cerrarpuerta)
ClampON = Button(fcontrol, text="Abrir Prensa",width = W1, height = H1, command = dnc.abrirprensa)
ClampOFF = Button(fcontrol, text="Cerrar Prensa", width = W1, height = H1, command = dnc.cerrarprensa)
SpinON = Button(fcontrol, text="Encender Spindle",width = W1, height = H1, command = dnc.spindlecw)
SpinOFF = Button(fcontrol, text="Apagar Spindle", width = W1, height = H1,command = dnc.stopspindle)


Open.grid(row=0, column = 0,ipadx=5,ipady=5,pady=5,padx=5)
Close.grid(row=0, column = 1,ipadx=5,ipady=5,pady=5,padx=5)
ClampON.grid(row=1, column = 0,ipadx=5,ipady=5,pady=5,padx=5)
ClampOFF.grid(row=1, column = 1,ipadx=5,ipady=5,pady=5,padx=5)
SpinON.grid(row=2, column = 0,ipadx=5,ipady=5,pady=5,padx=5)
SpinOFF.grid(row=2, column = 1,ipadx=5,ipady=5,pady=5,padx=5)
"""
##############################################################################
Cuadro de mover manualmente codigos G
##############################################################################
"""
manualmove = LabelFrame(root,text= "Funciones de Movimiento",pady=5,padx=5)  
manualmove.grid(row=0, column = 2,ipadx=5,ipady=5,pady=5,padx=5)


#Widgets
VelT = Label(manualmove,text="Velocidad de Avance:")
DisT = Label(manualmove,text="mm por Click:")
Vel = Entry(manualmove)
Dis = Entry(manualmove)
ControlBox = LabelFrame(manualmove,text= "Control de movimiento",pady=5,padx=5)
XP = Button(manualmove, text="Actualizar", width = 40, height = 1, command = update)

ControlBox.grid(row=3, column = 0, columnspan = 2,ipadx=5,ipady=5,pady=5,padx=5)
Vel.grid(row=0, column = 1,ipadx=5,ipady=5,pady=5,padx=5)
Dis.grid(row=1, column = 1,ipadx=5,ipady=5,pady=5,padx=5)
VelT.grid(row=0, column = 0,ipadx=5,ipady=5,pady=5,padx=5, stick=E)
DisT.grid(row=1, column = 0,ipadx=5,ipady=5,pady=5,padx=5,stick=E)
XP.grid(row=2, column = 0, columnspan = 2, ipadx=5, ipady=5, pady=5, padx=5)
#Widgwts dentro de ControlBox
XP = Button(ControlBox, text="+X", width = 5, height = 2, command = moveX)
XL = Button(ControlBox, text="-X", width = 5, height = 2, command = moveXn)
YP = Button(ControlBox, text="+Y", width = 5, height = 2, command = moveY)
YL = Button(ControlBox, text="-Y", width = 5, height = 2, command = moveYn)
ZP = Button(ControlBox, text="+Z", width = 5, height = 2, command = moveZ)
ZL = Button(ControlBox, text="-Z", width = 5, height = 2, command = moveZn)
FL = Frame(ControlBox,bg="black", width = 1,height = 150)
KEY = Button(ControlBox, text="Key", width = 2, height = 1, command = NewWin)

XP.grid(row=1, column = 0,ipadx=5,ipady=5,pady=5,padx=5)
XL.grid(row=1, column = 2,ipadx=5,ipady=5,pady=5,padx=5)
YP.grid(row=0, column = 1,ipadx=5,ipady=5,pady=5,padx=5)
YL.grid(row=2, column = 1,ipadx=5,ipady=5,pady=5,padx=5)
ZP.grid(row=0, column = 5,ipadx=5,ipady=5,pady=5,padx=5)
ZL.grid(row=2, column = 5,ipadx=5,ipady=5,pady=5,padx=5)
FL.grid(row=0,column=4,rowspan = 4,ipadx=0,ipady=0,pady=0,padx=10)
KEY.grid(row=1,column=1,ipadx=0,ipady=0,pady=0,padx=0)
"""
##############################################################################
Cuadro de crear y enviar codigo
##############################################################################
"""
SendDNC = LabelFrame(root,text= "Enviar comandos",pady=5,padx=5)  
SendDNC.grid(row=2, column = 2,ipadx=5,ipady=5,pady=5,padx=5)

TName = Label(SendDNC,text="Diccion del archivo a enviar:")
Name = Entry(SendDNC,width = 20)
Send = Button(SendDNC, text="Enviar", width = 40, height = 2, command = SendFile)

TName.grid(row=0, column = 0, ipadx=5,ipady=5,pady=5,padx=5)
Name.grid(row=1, column = 0 , ipadx=5,ipady=5,pady=5,padx=5)
Send.grid(row=2, column = 0 , ipadx=5,ipady=5,pady=5,padx=5)
"""
##############################################################################
Cuadro de cambio de herramienta en el magazine
##############################################################################
"""
magazine = LabelFrame(root,text= "Cambio de herramienta",pady=5,padx=5)  
magazine.grid(row=2, column = 0,ipadx=5,ipady=5,pady=5,padx=5)

#Widgwts 
Change = Button(magazine, text="Cambiar Herramienta", width = 20, height = 2, command = tool)
Tool = Entry(magazine, width = 20)
TText = Label(magazine, text="Posicion:")
HomeX =  Button(magazine, text="Home eje X", width = 40, height = 2,command = homeX)
HomeY =  Button(magazine, text="Home eje Y", width = 40, height = 2,command = homeY)
HomeZ =  Button(magazine, text="Home eje Z", width = 40, height = 2,command = homeZ)

Change.grid(row=1, column = 0,columnspan = 2, ipadx=5,ipady=5,pady=5,padx=5)
Tool.grid(row=0, column = 1,ipadx=5,ipady=5,pady=5,padx=5)
TText.grid(row=0, column = 0,ipadx=5,ipady=5,pady=5,padx=5)
HomeX.grid(row =3, column = 0 , columnspan = 2,ipadx=5,ipady=2,pady=4,padx=5)
HomeY.grid(row= 4, column = 0 , columnspan = 2,ipadx=5,ipady=2,pady=4,padx=5)
HomeZ.grid(row =2, column = 0 , columnspan = 2,ipadx=5,ipady=2,pady=4,padx=5)
"""
##############################################################################
Inicio de la aplicacion
##############################################################################
"""
SP1 = Frame(root,width = 670, height = 5,bg="blue")
SP2 = Frame(root,width = 5, height = 700,bg="blue")
#SP1.grid(row =1, columnspan = 3)
#SP2.grid(column =1, row = 0, rowspan = 3)



root.mainloop()