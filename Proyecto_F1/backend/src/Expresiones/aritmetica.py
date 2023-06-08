from ..Abstract.abstract import Abstract

class Aritmetica(Abstract):

    def __init__(self, op_izq, op_der, op, fila, columna):
        self.op_izq = op_izq #
        self.op_der = op_der #
        self.op = op # *
        self.tipo = None
        super().__init__(fila, columna)
    
    def interpretar(self, tree, table):
        izq = self.op_izq.interpretar(tree, table)
        der = self.op_der.interpretar(tree, table)
        if self.op == '+':
            self.tipo = 'number'
            return izq + der
        elif self.op == '-':
            self.tipo = 'number'
            return izq - der
        elif self.op == '*':
            self.tipo = 'number'
            return izq * der
        elif self.op == '/':
            self.tipo = 'number'
            if der == 0:
                return 'Error: Division entre 0'
            return izq / der

    def getTipo(self):
        return self.tipo