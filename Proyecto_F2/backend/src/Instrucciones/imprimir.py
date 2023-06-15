from ..Tabla_Simbolos.excepcion import Excepcion
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.abstract import Abstract

class Imprimir(Abstract):

    def __init__(self, expresion, fila, columna):
        self.expresion = expresion # <<Class.Primitivos>>
        super().__init__(fila, columna)
    
    def interpretar(self, tree, table):
        genAux = Generador()
        generator = genAux.getInstance()

        value = self.expresion.interpretar(tree, table)

        if isinstance(value, Excepcion): return value

        if value.getTipo() == 'number':
            generator.addPrint('f', value.getValue())