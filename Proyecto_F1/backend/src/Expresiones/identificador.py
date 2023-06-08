from ..Tabla_Simbolos.excepcion import Excepcion
from ..Abstract.abstract import Abstract

class Identificador(Abstract):
    def __init__(self, ide, fila, columna, tipo = None):
        self.ide = ide
        self.fila = fila
        self.columna = columna
        self.tipo = tipo

    def interpretar(self, arbol , tabla):
        simbolo = tabla.getTabla(self.ide)
        if simbolo == None:
            return Excepcion("Semantico", "Variable no encontrada", self.fila, self.colum)
        self.tipo = simbolo.getTipo()
        return simbolo.getValor()

    def getTipo(self):
        return self.tipo
    
    def getID(self):
        return self.ide