from ..Abstract.abstract import Abstract

class Aritmetica(Abstract):

    def __init__(self, op_izq, op_der, op, fila, columna):
        self.op_izq = op_izq # <<Class.Primitivos>>
        self.op_der = op_der # <<Class.Primitivos>>
        self.op = op # *
        super().__init__(fila, columna)
    
    def interpretar(self, tree, table):
        izq = self.op_izq.interpretar(tree, table)
        tipo_izq = self.op_izq.getTipo()
        der = self.op_der.interpretar(tree, table)
        tipo_der = self.op_der.getTipo()
        if self.op == '+':
            if tipo_izq == 'number' and tipo_der == 'number':
                return izq + der
            elif tipo_izq == 'string' and tipo_der == 'string':
                return izq + der
            elif tipo_izq == 'string' and tipo_der == 'number':
                return 'Error: No se puede sumar un string con un number'
            elif tipo_izq == 'number' and tipo_der == 'string':
                return 'Error: No se puede sumar un number con un string'
            else:
                return 'Error: Tipo de dato invalido en suma'
        elif self.op == '-':
            return izq - der
        elif self.op == '*':
            return izq * der
        elif self.op == '/':
            if der == 0:
                return 'Error: Division entre 0'
            return izq / der
