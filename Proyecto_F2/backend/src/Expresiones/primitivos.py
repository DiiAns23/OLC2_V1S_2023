from ..Tabla_Simbolos.generador import Generador
from ..Abstract.abstract import Abstract
from ..Abstract.return__ import Return

class Primitivos(Abstract):

    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo # Number, String, Boolean
        self.valor = valor # 4, 'hola', true
        self.tipoAux = ''
        super().__init__(fila, columna)
    
    def interpretar(self, tree, table):
        genAux = Generador()
        generador = genAux.getInstance()
        if self.tipo == 'number':
            return Return(str(self.valor), self.tipo, False)
        elif self.tipo == 'string':
            temporal = generador.addTemp()
            generador.addAsig(temporal, 'H')

            for char in str(self.valor):
                generador.setHeap('H', ord(char))
                generador.nextHeap()
            generador.setHeap('H', -1)
            generador.nextHeap()

            return Return(temporal, self.tipo, True)
        
        elif self.tipo == 'boolean':
            if self.trueLbl == '':
                self.trueLbl = generador.newLabel()
            if self.falseLbl == '':
                self.falseLbl = generador.newLabel()
            
            if self.valor:
                generador.addGoto(self.trueLbl)
                generador.addComment("GOTO PARA EVITAR ERROR DE GO")
                generador.addGoto(self.falseLbl)
            else:
                generador.addGoto(self.falseLbl)
                generador.addComment("GOTO PARA EVITAR ERROR DE GO")
                generador.addGoto(self.trueLbl)
            
            ret = Return(self.valor, self.tipo, False)
            ret.trueLbl = self.trueLbl
            ret.falseLbl = self.falseLbl
            return ret

    def getTipo(self):
        return self.tipo
