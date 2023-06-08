from ..Tabla_Simbolos.excepcion import Excepcion
from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.simbolo import Simbolo

class Declaracion_Variables(Abstract):

    def __init__(self, ide, tipo, valor, fila, columna):
        self.ide = ide # a
        self.tipo = tipo # Number, String, Boolean
        self.valor = valor # 4, 'hola', true
        super().__init__(fila, columna)
    
    def interpretar(self, arbol, tabla):
        value = self.valor.interpretar(arbol, tabla)
        if isinstance(value, Excepcion): return value # Analisis Semantico -> Error
        # Verificacion de tipos
        if str(self.tipo) == str(self.valor.tipo):
            simbolo = Simbolo(str(self.ide), self.valor.tipo, value, self.fila, self.columna)
            result = tabla.setTabla(simbolo)
            if isinstance(result, Excepcion): return result
            return None
        else:
            result = Excepcion("Semantico", "Tipo de dato diferente declarado.", self.fila, self.columna)
            return result