# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 11:11:45 2018

@author: juandavid.contreras
"""
from RVM1 import execute, program
from tkinter import *
import tkinter as tk
import time
from tkinter import messagebox
from DEMOStation import FUNCIONS
import serial
root = Tk()
root.title("Control Robot RV-M1")


port = serial.Serial(port = "COM1", baudrate=9600, parity="O", bytesize=7, stopbits=2,xonxoff = False)


"""
##############################################################################
Funciones
##############################################################################
"""
e = execute(port)
p = program(port)
F = FUNCIONS(port)
A = 0
V= 0
def donde():
    P = e.where()
    PosText = str(P)
    PosLabel.config(text=PosText)

def update():
    global A
    global V
    A = int(Dis.get())
    V = int(Vel.get())
    print("parametros actualizados")
    print("mm por click = " + str(A))
    print("Velocidad de avance = " + str(V))
    dnc.code("F%s" % V)
    
def movejoin1p():
    J = angulo.get()
    e.MJ(int(J),0,0,0,0)
def movejoin1l():
    J = angulo.get()
    e.MJ(-int(J),0,0,0,0)
def movejoin2p():
    J = angulo.get()
    e.MJ(0,int(J),0,0,0)
def movejoin2l():
    J = angulo.get()
    e.MJ(0,-int(J),0,0,0)
def movejoin3p():
    J = angulo.get()
    e.MJ(0,0,int(J),0,0)
def movejoin3l():
    J = angulo.get()
    e.MJ(0,0,-int(J),0,0)
def movejoin4p():
    J = angulo.get()
    e.MJ(0,0,0,int(J),0)
def movejoin4l():
    J = angulo.get()
    e.MJ(0,0,0,-int(J),0)
def movejoin5p():
    J = angulo.get()
    e.MJ(0,0,0,0,int(J))
def movejoin5l():
    J = angulo.get()
    e.MJ(0,0,0,0,-int(J))
    
def movexp():
    O = offset.get()
    e.DW(int(O),0,0) 
def movexl():
    O = offset.get()
    e.DW(-int(O),0,0)
def moveyp():
    O = offset.get()
    e.DW(0,int(O),0) 
def moveyl():
    O = offset.get()
    e.DW(0,-int(O),0)
def movezp():
    O = offset.get()
    e.DW(0,0,int(O)) 
def movezl():
    O = offset.get()
    e.DW(0,0,-int(O))
    
def movepp():
    A = pichroll.get()
    A = float(A)
    A = round(A,1)
    P = e.where()
    e.MP(P[0],P[1],P[2],P[3]+A,P[4])
    
def movepl():
    A = pichroll.get()
    A = float(A)
    A = round(A,1)
    P = e.where()
    e.MP(P[0],P[1],P[2],P[3]-A,P[4])

def moverp():
    A = pichroll.get()
    A = float(A)
    A = round(A,1)
    P = e.where()
    e.MP(P[0],P[1],P[2],P[3],P[4]+A)
     
def moverl():
    A = pichroll.get()
    A = float(A)
    A = round(A,1)
    P = e.where()
    e.MP(P[0],P[1],P[2],P[3],P[4]-A)
    
def reset():
    e.RS()

def origen():
    e.OG()

def nest():
    e.NT()   

def gopen():
    e.GO()     

def gclose():
    e.GC() 

def aqui():
    A = Posicion.get()
    A = int(A)
    e.HE(A) 
    
def mover():
    X = moveto.get()
    X = int(X)
    Y = v1.get()
    if Y ==0:
        e.MO(X,"O")
    elif Y==1:
        e.MO(X,"C")
    else:
        print("No se reconoce el comando")
    """
    P = e.where()
    PosText = str(P)
    PosLabel.config(text=PosText)
    """
    
def moverrecto():
    X = movesLineto.get()
    Pasos = movesSteps.get()
    Pasos = int(Pasos)
    X = int(X)
    Y = v2.get()
    if Y ==0:
        e.MS(X,Pasos,"O")
    elif Y==1:
        e.MS(X,Pasos,"C")
    else:
        print("No se reconoce el comando")

    
def movercontinuo():
    FROM = movesCont1.get()
    TO = movesCont2.get()
    TO = int(TO)
    FROM = int(FROM)
    Y = v2.get()
    if Y ==0:
        e.MC(FROM,TO)
    elif Y==1:
        e.MC(FROM,TO)
    else:
        print("No se reconoce el comando")
        
    
def velocidad():
    S = speed.get()
    S = int(S)
    e.SP(S,"H")
    
def SendFile():
    File = FileE.get()
    try:
        F = open(File)
        for i in F:
            e.tx(i)
    except:
        print("nombre de archivo no valido")
    
def guardarpos():
    X = cX.get()
    X = float(X)
    Y = cX.get()
    Y = float(Y)
    Z = cX.get()
    Z = float(Z)
    P = cX.get()
    P = float(P)
    R = cX.get()
    R = float(R)
    A = Posicion.get()
    A = int(A)
    e.PD(A,X,Y,Z,P,R)
def escribir():
    P = palabra.get()
    F.ESCRIBIR(P)
    
def play():
    F.PLAY()
    
def pick():
    F.PICK()

image = PhotoImage(file="PUJ-Logo.png")
#image.zoom(5)
FRAME1 = Frame(root,pady=1,padx=1) 
FRAME2 = Frame(root,pady=1,padx=1) 
FRAME3 = Frame(root,pady=1,padx=1)   
FRAME3.grid(row=0, column = 2,ipadx=1,ipady=1,pady=5,padx=5)  
FRAME1.grid(row=0, column = 0,ipadx=1,ipady=1,pady=5,padx=5)  
FRAME2.grid(row=0, column = 1,ipadx=1,ipady=1,pady=5,padx=5) 

imagelabel = Label(FRAME3,image=image) 
LabelCAP = Label(FRAME3,text="Software desarrollado por el Centro de Automatizacion de Procesos")
imagelabel.grid(row=1, column = 0,ipadx=1,ipady=1,pady=5,padx=5) 
LabelCAP.grid(row=0, column = 0,ipadx=1,ipady=1,pady=5,padx=5) 

"""
##############################################################################
Cuadro Jogging
##############################################################################
"""
Jo = LabelFrame(FRAME1, text= "Jogging",pady=5,padx=5)  
Jo.grid(row=0, column = 0,ipadx=1,ipady=1,pady=5,padx=5)

#Widgets
W1=4
H1=1
#Mover articulaciones
t1p = Button(Jo, text="+J1", width = W1, height = H1,command = movejoin1p)
t1l = Button(Jo, text="-J1", width = W1, height = H1,command = movejoin1l)
t2p = Button(Jo, text="+J2", width = W1, height = H1,command = movejoin2p)
t2l = Button(Jo, text="-J2", width = W1, height = H1,command = movejoin2l)
t3p = Button(Jo, text="+J3", width = W1, height = H1,command = movejoin3p)
t3l = Button(Jo, text="-J3", width = W1, height = H1,command = movejoin3l)
t4p = Button(Jo, text="+J4", width = W1, height = H1,command = movejoin4p)
t4l = Button(Jo, text="-J4", width = W1, height = H1,command = movejoin4l)
t5p = Button(Jo, text="+J5", width = W1, height = H1,command = movejoin5p)
t5l = Button(Jo, text="-J5", width = W1, height = H1,command = movejoin5l)
angulo = Entry(Jo,width = 5)
Tangulo = Label(Jo,width = 22, text= "Avance por click en grados:")
#Mover XYZ
xp = Button(Jo, text="+X", width = W1, height = H1,command = movexp)
xl = Button(Jo, text="-X", width = W1, height = H1,command = movexl)
yp = Button(Jo, text="+Y", width = W1, height = H1,command = moveyp)
yl = Button(Jo, text="-Y", width = W1, height = H1,command = moveyl)
zp = Button(Jo, text="+Z", width = W1, height = H1,command = movezp)
zl = Button(Jo, text="-Z", width = W1, height = H1,command = movezl)
pp = Button(Jo, text="+P", width = W1, height = H1,command = movepp)
pl = Button(Jo, text="-P", width = W1, height = H1,command = movepl)
rp = Button(Jo, text="+R", width = W1, height = H1,command = moverp)
rl = Button(Jo, text="-R", width = W1, height = H1,command = moverl)
offset = Entry(Jo,width = 5)
Toffset = Label(Jo,width = 22, text= "Avance XYZ en milimetros:")
pichroll = Entry(Jo,width = 5)
Tpichroll = Label(Jo,width = 22, text= "Avance pich/roll en grados:")
ipx = 1
ipy = 1
t1p.grid(row=3, column = 0,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
t1l.grid(row=4, column = 0,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
t2p.grid(row=3, column = 1,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
t2l.grid(row=4, column = 1,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
t3p.grid(row=3, column = 2,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
t3l.grid(row=4, column = 2,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
t4p.grid(row=3, column = 3,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
t4l.grid(row=4, column = 3,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
t5p.grid(row=3, column = 4,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
t5l.grid(row=4, column = 4,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
angulo.grid(row=2, column = 4, ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
Tangulo.grid(row=2, column = 0, columnspan= 4, ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)

xp.grid(row=7, column = 0,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
xl.grid(row=8, column = 0,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
yp.grid(row=7, column = 1,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
yl.grid(row=8, column = 1,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
zp.grid(row=7, column = 2,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
zl.grid(row=8, column = 2,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
pp.grid(row=7, column = 3,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
pl.grid(row=8, column = 3,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
rp.grid(row=7, column = 4,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
rl.grid(row=8, column = 4,ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
offset.grid(row=5, column = 4, ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
Toffset.grid(row=5, column = 0, columnspan= 4, ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
pichroll.grid(row=6, column = 4, ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
Tpichroll.grid(row=6, column = 0, columnspan= 4, ipadx=ipx,ipady=ipy,pady=ipy,padx=ipx)
"""
##############################################################################
Cuadro de ensañar posiciones
##############################################################################
"""
teach = LabelFrame(FRAME2,text= "Funciones de Enseñar Posiciones",pady=5,padx=5)  
teach.grid(row=0, column = 0,ipadx=1,ipady=1,pady=5,padx=5)

#Widgets
AnchoXYZ = 5
here = Button(teach,text="Enseñar posicion actual",width = 20, height = 1, command = aqui)
Posicion = Entry(teach, width = AnchoXYZ)
Tpos = Label(teach,text="Guardar en la posicion numero:")

coordTeach = Button(teach, text="Guardar posicion segun coordenada", width = 32, height = 1, command = guardarpos)
TcX= Label(teach,text="X:")
cX = Entry(teach, width = AnchoXYZ)
TcY= Label(teach,text="Y:")
cY = Entry(teach, width = AnchoXYZ)
TcZ= Label(teach,text="Z:")
cZ = Entry(teach, width = AnchoXYZ)
TcP= Label(teach,text="P:")
cP = Entry(teach, width = AnchoXYZ)
TcR= Label(teach,text="R:")
cR = Entry(teach, width = AnchoXYZ)
pady2 = 5
here.grid(row=1,column=0,columnspan=5,ipadx=ipx,ipady=ipy,pady=10,padx=ipx)
Posicion.grid(row=0,column=4,ipadx=ipx,ipady=ipy,pady=pady2,padx=ipx)
Tpos.grid(row=0,column=0,columnspan=4,ipadx=ipx,ipady=ipy,pady=pady2,padx=ipx)


"""
##############################################################################
Cuadro velocidad
##############################################################################
"""
Velocidad = LabelFrame(FRAME2,text= "Velocidad",pady=5,padx=5)  
Velocidad.grid(row=1, column = 0,ipadx=1,ipady=1,pady=5,padx=5)

speed = IntVar()
speed.set(4)
vel1 = Radiobutton(Velocidad, text="1", variable=speed, value=1, command = velocidad)
vel2 = Radiobutton(Velocidad, text="2", variable=speed, value=2, command = velocidad)
vel3 = Radiobutton(Velocidad, text="3", variable=speed, value=3, command = velocidad)
vel4 = Radiobutton(Velocidad, text="4", variable=speed, value=4, command = velocidad)
vel5 = Radiobutton(Velocidad, text="5", variable=speed, value=5, command = velocidad)
vel6 = Radiobutton(Velocidad, text="6", variable=speed, value=6, command = velocidad)
vel7 = Radiobutton(Velocidad, text="7", variable=speed, value=7, command = velocidad)
vel8 = Radiobutton(Velocidad, text="8", variable=speed, value=8, command = velocidad)
vel9 = Radiobutton(Velocidad, text="9", variable=speed, value=9, command = velocidad)

vel1.grid(row=0, column = 0, ipadx=1,ipady=1,pady=1,padx=1)
vel2.grid(row=0, column = 1, ipadx=1,ipady=1,pady=1,padx=1)
vel3.grid(row=0, column = 2, ipadx=1,ipady=1,pady=1,padx=1)
vel4.grid(row=0, column = 3, ipadx=1,ipady=1,pady=1,padx=1)
vel5.grid(row=0, column = 4, ipadx=1,ipady=1,pady=1,padx=1)
vel6.grid(row=1, column = 0, ipadx=1,ipady=1,pady=1,padx=1)
vel7.grid(row=1, column = 1, ipadx=1,ipady=1,pady=1,padx=1)
vel8.grid(row=1, column = 2, ipadx=1,ipady=1,pady=1,padx=1)
vel9.grid(row=1, column = 3, ipadx=1,ipady=1,pady=1,padx=1)

"""
##############################################################################
Cuadro botones funciones simples
##############################################################################
"""
comandos = LabelFrame(FRAME2,text= "Comandos",pady=5,padx=5)  
comandos.grid(row=2, column = 0,ipadx=1,ipady=1,pady=5,padx=5)

Nest = Button(comandos, text="Nest", width = 13, height = 1, command=nest)
Orig = Button(comandos, text="Origen", width = 13,height = 1, command=origen)
Reset = Button(comandos, text="Reset", width = 30, height = 1, command = reset)
GOpen = Button(comandos, text="Abrir Pinza", width = 14, height = 1, command = gopen)
GClose = Button(comandos, text="Cerrar Pinza", width = 14, height = 1,command = gclose)

Nest.grid(row=0, column = 0, ipadx=1,ipady=1,pady=4,padx=1)
Orig.grid(row=0, column = 1, ipadx=1,ipady=1,pady=4,padx=1)
Reset.grid(row=1, column = 0, columnspan = 2, ipadx=1,ipady=1,pady=4,padx=1)
GOpen.grid(row=2, column = 0, ipadx=1,ipady=1,pady=4,padx=1)
GClose.grid(row=2, column = 1, ipadx=1,ipady=1,pady=4,padx=1)

"""
##############################################################################
Cuadro funciones predefinidas
##############################################################################
"""
RUNc = LabelFrame(FRAME2,text= "Ejecutar programas",pady=5,padx=5)  
RUNc.grid(row=4, column = 0,ipadx=1,ipady=1,pady=5,padx=5)

pickF = Button(RUNc, text="Pick", width = 30, height = 1, command = pick)
playF = Button(RUNc, text="Play", width = 30,height = 1, command = play)
writeF = Button(RUNc, text="Write", width = 30, height = 1, command = escribir)
Tpalabra = Label(RUNc, text="Palabra:", width = 15)
palabra = Entry(RUNc, width = 10)

pickF.grid(row=0, column = 0,columnspan = 2, ipadx=1,ipady=1,pady=4,padx=1)
playF.grid(row=1, column = 0,columnspan = 2, ipadx=1,ipady=1,pady=4,padx=1)
writeF.grid(row=2, column = 0, columnspan = 2, ipadx=1,ipady=1,pady=4,padx=1)
Tpalabra.grid(row=3, column = 0, ipadx=1,ipady=1,pady=4,padx=1)
palabra.grid(row=3, column = 1, ipadx=1,ipady=1,pady=4,padx=1)

"""
##############################################################################
Cuadro FILE
##############################################################################
"""
FILE = LabelFrame(FRAME2,text= "Enviar archivo de comandos",pady=1,padx=5)  
FILE.grid(row=5, column = 0,ipadx=1,ipady=1,pady=5,padx=5)

EnviarFile = Button(FILE, text="Enviar", width = 30, height = 1, command = SendFile)
TFileE = Label(FILE, text="Archivo", width = 15)
FileE = Entry(FILE, width = 15)

EnviarFile.grid(row=1, column = 0,columnspan = 2, ipadx=1,ipady=1,pady=4,padx=1)
TFileE.grid(row=0, column = 0, ipadx=1,ipady=1,pady=4,padx=1)
FileE.grid(row=0, column = 1, ipadx=1,ipady=1,pady=4,padx=1)


"""
##############################################################################
Cuadro de mover robot
##############################################################################
"""
movimientos = LabelFrame(FRAME1,text= "Funciones de movimiento",pady=5,padx=5)  
movimientos.grid(row=1, column = 0,rowspan = 4 , ipadx=1,ipady=1,pady=5,padx=5)

#############
# cuadro 1 #
#############
move = LabelFrame(movimientos,text= "Mover a una posicion guardada",pady=5,padx=5)  
move.grid(row=0, column = 0,ipadx=1,ipady=1,pady=5,padx=5)
############################################################################
moveB = Button(move, text="Mover", width = 25, height = 1, command= mover)
moveto = Entry(move, width = 4)
moveT = Label(move, text="Posicion destino:")
v1 = IntVar()
v1.set(0)
moveGopen = Radiobutton(move, text="Pinza Abierta", variable=v1, value=0)
moveGclose = Radiobutton(move, text="Pinza Cerrada", variable=v1, value=1)

moveB.grid(row=2, column = 0, columnspan = 2 , ipadx=2,ipady=2,pady=2,padx=2)
moveto.grid(row=0, column = 1 , ipadx=2,ipady=2,pady=2,padx=2)
moveT.grid(row=0, column = 0 , ipadx=2,ipady=2,pady=2,padx=2)
moveGopen.grid(row=1, column = 0 )
moveGclose.grid(row=1, column = 1 )
#############
# cuadro 2 #
#############
movesLine = LabelFrame(movimientos,text= "Mover en linea",pady=5,padx=5)  
movesLine.grid(row=1, column = 0,ipadx=1,ipady=1,pady=5,padx=5)
############################################################################
movesLineB = Button(movesLine, text="Mover", width = 25, height = 1, command = moverrecto)
movesLineto = Entry(movesLine, width = 4)
movesLineT = Label(movesLine, text="Posicion destino:")
movesSteps = Entry(movesLine, width = 4)
movesStepsT = Label(movesLine, text="Pasos:")
v2 = IntVar()
movesLineGopen = Radiobutton(movesLine, text="Pinza Abierta", variable=v2, value=0)
movesLineGclose = Radiobutton(movesLine, text="Pinza Cerrada", variable=v2, value=1)

movesLineB.grid(row=3, column = 0, columnspan = 2 , ipadx=2,ipady=2,pady=2,padx=2)
movesLineto.grid(row=0, column = 1 , ipadx=2,ipady=2,pady=2,padx=2)
movesLineT.grid(row=0, column = 0 , ipadx=2,ipady=2,pady=2,padx=2)
movesSteps.grid(row=1, column = 1 , ipadx=2,ipady=2,pady=2,padx=2)
movesStepsT.grid(row=1, column = 0 , ipadx=2,ipady=2,pady=2,padx=2)
movesLineGopen.grid(row=2, column = 0)
movesLineGclose.grid(row=2, column = 1)

#############
# cuadro 3 #
#############
movesCont = LabelFrame(movimientos,text= "Movimiento continuo",pady=5,padx=5)  
movesCont.grid(row=2, column = 0,ipadx=1,ipady=1,pady=5,padx=5)
############################################################################
movesContB = Button(movesCont, text="Mover", width = 25, height = 1, command = movercontinuo)
movesCont1 = Entry(movesCont, width = 4)
movesCont1T = Label(movesCont, text="Posicion inicial:")
movesCont2 = Entry(movesCont, width = 4)
movesCont2T = Label(movesCont, text="Posicion Final:")


movesContB.grid(row=2, column = 0, columnspan = 2 , ipadx=2,ipady=2,pady=2,padx=2)
movesCont1.grid(row=0, column = 1 , ipadx=2,ipady=2,pady=2,padx=2)
movesCont1T.grid(row=0, column = 0 , ipadx=2,ipady=2,pady=2,padx=2)
movesCont2.grid(row=1, column = 1 , ipadx=2,ipady=2,pady=2,padx=2)
movesCont2T.grid(row=1, column = 0 , ipadx=2,ipady=2,pady=2,padx=2)

"""
##############################################################################
Ver posicion actual
##############################################################################
"""
PosLabelFrame = LabelFrame(FRAME2,text= "Ver Posicion actual del robot",pady=5,padx=5)  
PosLabelFrame.grid(row=6, column = 0,rowspan = 4 , ipadx=1,ipady=1,pady=5,padx=5)

PosLabel = Label(PosLabelFrame,text = "Posicion sin definir")
updatePos = Button(PosLabelFrame, text="Actualizar", width = 6, height = 1, command = donde)
PosLabel.grid(row=0, column = 0 , ipadx=1,ipady=1,pady=1,padx=1)
updatePos.grid(row=0, column = 1 , ipadx=1,ipady=1,pady=1,padx=1)



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