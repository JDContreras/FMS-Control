# -*- coding: utf-8 -*-

from opcua import Client, Server
from opcua import ua


"""
################################################################################
Inicio del programa
################################################################################
"""

Cordinator = Client("opc.tcp://192.168.43.176:4000/Control/") #cuadrar tambien esta ip

"""
################################################################################

################################################################################
"""

Cordinator.connect()
CordinatorRoot = Cordinator.get_root_node()
OPCpedidos = CordinatorRoot.get_child(["0:Objects", "2:Variables", "2:pedidos"])
OPCfabricando = CordinatorRoot.get_child(["0:Objects", "2:Variables", "2:fabricando"])
OPCterminadas = CordinatorRoot.get_child(["0:Objects", "2:Variables", "2:terminadas"])
pedir = CordinatorRoot.get_child(["0:Objects", "2:Services"])


#corres este archivo y  utilizas esta funcion para crear pedidos antes de madar el pallet, esto tambien se puede hacer desde el celular , bleider sabe como.
def pedir3(n):
    pedir.call_method("2:Ordenar",n)
    
pedir3(1)
pedir3(1)
pedir3(1)
pedir3(1)
pedir3(1)
pedir3(1)
pedir3(1)
pedir3(1)
#para usar la funcion en el Shell escribes pedir3(#) donde # es 1 o 2, te dejo que se me descargo el pc