from ..Tabla_Simbolos.excepcion import Excepcion
from ..Abstract.abstract import Abstract

class Relacional_Logica(Abstract):

    def __init__(self, op_izq, op_der, op, fila, columna):
        self.op_izq = op_izq #
        self.op_der = op_der #
        self.op = op # *
        self.tipo = 'boolean'
        super().__init__(fila, columna)
    
    def interpretar(self, tree, table):
        izq = self.op_izq.interpretar(tree, table)
        if isinstance(izq, Excepcion): return izq
        if self.op != '!':
            der = self.op_der.interpretar(tree, table)
            if isinstance(der, Excepcion): return der
        if self.op == '<':
            return izq < der
        elif self.op == '>':
            return izq > der
        elif self.op == '===':
            return izq == der
        elif self.op == '!==':
            return izq != der
        elif self.op == '<=':
            return izq <= der
        elif self.op == '>=':
            return izq >= der
        elif self.op == '&&':
            return izq and der
        elif self.op == '||':
            return izq or der
        elif self.op == '!':
            return not izq
        else:
            return Excepcion("Semantico", "Operacion no valida.", self.fila, self.columna)

    def getTipo(self):
        return self.tipo
    
    def getValor(self, tipo, val):
        # aqui hacen validacion del tipo de dato
        return str(val)