from ..Tabla_Simbolos.excepcion import Excepcion
from ..Tabla_Simbolos.simbolo import Simbolo
class TablaSimbolos:

    def __init__(self, anterior = None):
        self.tabla = {} # Al inicio la tabla esta vacia
        self.anterior = anterior # Apuntador al entorno anterior
        ### NUEVO PARA FASE 2 ###
        self.breakLbl = ''
        self.continueLbl = ''
        self.returnLbl = ''
        self.recTemps = False
        self.size = 0
        if anterior != None:
            self.size = self.anterior.size

    def setTabla(self, id, tipo, inHeap, find = True):
        if find:
            tablaActual = self
            while tablaActual != None:
                if id in tablaActual.tabla:
                    tablaActual.tabla[id].setTipo(tipo)
                    tablaActual.tabla[id].setInHeap(inHeap)
                    return tablaActual.tabla[id]
                else:
                    tablaActual = tablaActual.anterior
        if id in self.tabla:
            self.tabla[id].setTipo(tipo)
            self.tabla[id].setInHeap(inHeap)
            return self.tabla[id]
        else:
            simbolo = Simbolo(id,tipo,self.size,self.anterior == None, inHeap)
            self.size += 1
            self.tabla[id] = simbolo
            return self.tabla[id]
    
    def getTablaG(self):
        return self.tabla
    
    def setTablaFuncion(self, simbolo):
        self.tabla[simbolo.getID()] = simbolo
    
    def getTabla(self, ide): # Aqui manejamos los entornos :3
        tablaActual = self
        while tablaActual != None:
            if ide in tablaActual.tabla:
                return tablaActual.tabla[ide]
            else:
                tablaActual = tablaActual.anterior
        return None
    
    def updateTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None:
            if simbolo.getID() in tablaActual.tabla:
                tablaActual.tabla[simbolo.getID()].setValor(simbolo.getValor())
                return None
                # Si necesitan cambiar el tipo de dato
                # tablaActual.tabla[simbolo.getID()].setTipo(simbolo.getTipo())
            else:
                tablaActual = tablaActual.anterior
        return Excepcion("Semantico", "Variable no encontrada.", simbolo.getFila(), simbolo.getColumna())



