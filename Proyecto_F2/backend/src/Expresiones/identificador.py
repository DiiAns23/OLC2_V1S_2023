from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.simbolo import Simbolo
from ..Tabla_Simbolos.excepcion import Excepcion
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.return__ import Return

class Identificador(Abstract):
    def __init__(self, ide, fila, columna, tipo = None):
        self.ide = ide
        self.fila = fila
        super().__init__(fila, columna)
        

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
            generator.addExp(tempPos, 'P', simbolo.pos, '+')
        generator.getStack(temp, tempPos)
            
        
        if simbolo.type != 'boolean':
            generator.addComment("Fin de compilacion de Acceso")
            generator.addSpace()
            return Return(temp, simbolo.type, True)
        
        if self.trueLbl == '':
            self.trueLbl = generator.newLabel()
        if self.falseLbl == '':
            self.falseLbl = generator.newLabel()

        generator.addIf(temp,'1', '==', self.trueLbl)
        generator.addGoto(self.falseLbl)

        generator.addComment("Fin de compilacion de Acceso")
        generator.addSpace()

        ret = Return(None, 'boolean', True)
        ret.setTrueLbl(self.trueLbl)
        ret.setFalseLbl(self.falseLbl)
        return ret



    def getTipo(self):
        return self.tipo
    
    def getID(self):
        return self.ide