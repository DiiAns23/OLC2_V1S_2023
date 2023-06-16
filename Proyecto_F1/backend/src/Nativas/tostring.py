from ..Tabla_Simbolos.excepcion import Excepcion
from ..Instrucciones.funcion import Funcion

class String(Funcion):

    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.tipo = "string"
        super().__init__(nombre, parametros, instrucciones, fila, columna)
    
    def interpretar(self, arbol, tabla):
        simbolo = tabla.getTabla("toString##Param1")
        if simbolo == None: return Excepcion("Semantico", "No se encontro el parametro de toUpperCase", self.fila, self.columna)
        simbolo.setTipo("string")
        return str(simbolo.getValor())
