from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.excepcion import Excepcion
from ..Tabla_Simbolos.tabla_simbolos import TablaSimbolos

class If(Abstract):

    def __init__(self, condicion, bloqueIf, bloqueElse, bloqueElseif, fila, columna):
        self.condicion = condicion
        self.bloqueIf = bloqueIf
        self.bloqueElse = bloqueElse
        self.bloqueElseif = bloqueElseif
        super().__init__(fila, columna)
    

    def interpretar(self, arbol, tabla):
        condicion = self.condicion.interpretar(arbol, tabla)
        if isinstance(condicion, Excepcion): return condicion
        # Validar que el tipo sea booleano
        if bool(condicion) == True:
            entorno = TablaSimbolos(tabla)  #NUEVO ENTORNO - HIJO - Vacio
            for instruccion in self.bloqueIf:
                result = instruccion.interpretar(arbol, entorno) 
                if isinstance(result, Excepcion) :
                    arbol.setExcepcion(result)
        elif self.bloqueElse != None:
            entorno = TablaSimbolos(tabla)
            for instruccion in self.bloqueElse:
                result = instruccion.interpretar(arbol, entorno) 
                if isinstance(result, Excepcion) :
                    arbol.setExcepcion(result)
        elif self.bloqueElseif != None:
            result = self.bloqueElseif.interpretar(arbol, tabla)
