from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.excepcion import Excepcion
from ..Tabla_Simbolos.tabla_simbolos import TablaSimbolos

class Return(Abstract):

    def __init__(self,expresion, fila, columna):
        self.expresion = expresion
        self.value = None
        self.tipo = None
        super().__init__(fila, columna)
    
    def interpretar(self, arbol, tabla):
        result = self.expresion.interpretar(arbol, tabla)
        if isinstance(result, Excepcion): return result
        self.tipo = self.expresion.tipo
        self.value = result
        return self