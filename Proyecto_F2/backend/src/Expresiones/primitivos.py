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
        return Return(str(self.valor), self.tipo, False)

    def getTipo(self):
        return self.tipo
