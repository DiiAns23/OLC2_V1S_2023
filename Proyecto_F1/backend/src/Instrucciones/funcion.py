from ..Instrucciones._return import Return
from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.excepcion import Excepcion
from ..Tabla_Simbolos.tabla_simbolos import TablaSimbolos

class Funcion(Abstract):

    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.tipo = 'number'
        super().__init__(fila, columna)
    

    def interpretar(self, arbol, tabla):
        entorno = TablaSimbolos(tabla)
        for instruccion in self.instrucciones:
            value = instruccion.interpretar(arbol, entorno)
            if isinstance(value, Excepcion): return value
            if isinstance(value, Return):
                self.tipo = value.tipo
                return value.value
        return None