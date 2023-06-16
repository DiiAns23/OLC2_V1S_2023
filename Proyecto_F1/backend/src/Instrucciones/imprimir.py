from ..Abstract.abstract import Abstract

class Imprimir(Abstract):

    def __init__(self, expresion, fila, columna):
        self.expresion = expresion # <<Class.Primitivos>>
        super().__init__(fila, columna)
    
    def interpretar(self, tree, table):
        value = ''
        for expresion in self.expresion:
            value += str(expresion.interpretar(tree, table))
            value += ' '
        tree.updateConsola(str(value))
        return None