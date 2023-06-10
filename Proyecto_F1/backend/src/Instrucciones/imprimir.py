from ..Abstract.abstract import Abstract

class Imprimir(Abstract):

    def __init__(self, expresion, fila, columna):
        self.expresion = expresion # <<Class.Primitivos>>
        super().__init__(fila, columna)
    
    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table)
        print(value)
        tree.updateConsola(str(value))
        return value