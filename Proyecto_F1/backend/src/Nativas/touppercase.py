from ..Tabla_Simbolos.excepcion import Excepcion
from ..Instrucciones.funcion import Funcion

class ToUpperCase(Funcion):

    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.tipo = "any"
        super().__init__(nombre, parametros, instrucciones, fila, columna)
    
    def interpretar(self, arbol, tabla):
        simbolo = tabla.getTabla("toUpperCase##Param1")
        if simbolo == None: return Excepcion("Semantico", "No se encontro el parametro de toUpperCase", self.fila, self.columna)

        self.tipo = simbolo.getTipo()
        return simbolo.getValor().upper()
