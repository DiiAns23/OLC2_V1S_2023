from ..Abstract.abstract import Abstract

class Primitivos(Abstract):

    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo # Number, String, Boolean
        self.valor = valor # 4, 'hola', true
        super().__init__(fila, columna)
    
    def interpretar(self, tree, table):
        return self.valor # 4

    def getTipo(self):
        return self.tipo
