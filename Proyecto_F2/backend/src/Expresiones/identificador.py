from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.simbolo import Simbolo
from ..Tabla_Simbolos.excepcion import Excepcion
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.return__ import Return

class Identificador(Abstract):
    def __init__(self, ide, fila, columna, tipo = None):
        self.ide = ide
        self.fila = fila
        self.columna = columna
        self.tipo = tipo

    def interpretar(self, arbol , tabla):
        genAux = Generador()
        generator = genAux.getInstance()

        generator.addComment("Compilacion de Acceso")

        simbolo = tabla.getTabla(self.ide)
        if simbolo == None:
            generator.addComment("Fin de compilacion de Acceso por error")
            return Excepcion("Semantico", "Variable no encontrada", self.fila, self.columna)
        # Temporal para guardar la variable
        temp = generator.addTemp()
        
        # Obtencion de posicion de la variable
        tempPos = simbolo.pos
        if not simbolo.isGlobal:
            tempPos = generator.addTemp()
            generator.addExpression(tempPos, 'P', simbolo.pos, '+')
        
        generator.getStack(temp, tempPos)
        generator.addComment("Fin de compilacion de Acceso")
        return Return(temp, simbolo.type, True)

    def getTipo(self):
        return self.tipo
    
    def getID(self):
        return self.ide