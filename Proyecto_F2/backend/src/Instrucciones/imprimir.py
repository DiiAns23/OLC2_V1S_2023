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
        elif value.getTipo() == 'string':
            generator.fPrintString()

            paramTemp = generator.addTemp()
            
            generator.addExp(paramTemp, 'P', table.size, '+')
            generator.addExp(paramTemp, paramTemp, '1', '+')
            generator.setStack(paramTemp, value.value)
            
            generator.newEnv(table.size)
            generator.callFun('printString')

            temp = generator.addTemp()
            generator.getStack(temp, 'P')
            generator.retEnv(table.size)