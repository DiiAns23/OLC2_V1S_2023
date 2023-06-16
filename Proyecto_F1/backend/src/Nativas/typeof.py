from ..Tabla_Simbolos.excepcion import Excepcion
from ..Instrucciones.funcion import Funcion

class Typeof(Funcion):

    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.tipo = "any"
        super().__init__(nombre, parametros, instrucciones, fila, columna)
    
    def interpretar(self, arbol, tabla):
        simbolo = tabla.getTabla("typeof##Param1")
        if simbolo == None: return Excepcion("Semantico", "No se encontro el parametro de Typeof", self.fila, self.columna)

        self.tipo = self.calcularTipo(simbolo.getValor())
        return self.tipo

    def calcularTipo(self, valor):
        # Reconocer el tipo de dato del valor 
        if (type(valor) == int):
            return 'number'
        elif (type(valor) == float):
            return  'number'
        elif (type(valor) == str):
            return 'string'
        elif (type(valor) == bool):
            return 'boolean'