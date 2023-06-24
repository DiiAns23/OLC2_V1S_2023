from ..Tabla_Simbolos.excepcion import Excepcion
from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.return__ import Return

class Relacional_Logica(Abstract):

    def __init__(self, op_izq, op_der, op, fila, columna):
        self.op_izq = op_izq #
        self.op_der = op_der #
        self.op = op # *
        self.tipo = 'boolean'
        super().__init__(fila, columna)
    
    def interpretar(self, arbol, tabla):
        genAux = Generador()
        generador = genAux.getInstance()

        if (self.op != '&&' and self.op != '||' and self.op != '!'):
            generador.addComment("Compilacion de Expresion Relacional")

            left = self.op_izq.interpretar(arbol, tabla)
            if isinstance(left, Excepcion): return left
            right = None
            result = Return(None, 'boolean', False)

            if left.getTipo() != 'boolean':
                right = self.op_der.interpretar(arbol, tabla)
                if isinstance(right, Excepcion): return right
                if (left.getTipo() == 'number') and (right.getTipo() == 'number'):
                    self.checkLabels()
                    generador.addIf(left.getValue(), right.getValue(), self.getOperador(), self.getTrueLbl())
                    generador.addGoto(self.getFalseLbl())
                elif (left.getTipo() == 'string') and (right.getTipo() == 'string'):
                    if self.op == '===' or self.op == '!==':
                        generador.fcompareString()
                        paramTemp = generador.addTemp()

                        generador.addExp(paramTemp, 'P', tabla.size, '+')
                        generador.addExp(paramTemp, paramTemp, '1', '+')
                        generador.setStack(paramTemp, left.getValue())

                        generador.addExp(paramTemp, paramTemp, '1', '+')
                        generador.setStack(paramTemp, right.getValue())

                        generador.newEnv(tabla.size)
                        generador.callFun('compareString')

                        temp = generador.addTemp()
                        generador.getStack(temp, 'P')
                        generador.retEnv(tabla.size)

                        self.checkLabels()
                        generador.addIf(temp, self.getNum(), "==", self.trueLbl)
                        generador.addGoto(self.falseLbl)

                        result.setTrueLbl(self.trueLbl)
                        result.setFalseLbl(self.falseLbl)
                        return result
                

            generador.addComment("Fin de compilacion de Expresion Relacional")
            generador.addSpace()
            
            result.setTrueLbl(self.trueLbl)
            result.setFalseLbl(self.falseLbl)
            return result
        else:
            generador.addComment("Compilacion de Expresion Relacional")
            self.checkLabels()
            lblAndOr = ''
            if self.op == '&&':
                lblAndOr =  generador.newLabel()

                self.op_izq.setTrueLbl(lblAndOr) 
                self.op_der.setTrueLbl(self.trueLbl)
                self.op_izq.falseLbl = self.op_der.falseLbl = self.falseLbl

            elif self.op == '||':
                self.op_izq.setTrueLbl(self.trueLbl) 
                self.op_der.setTrueLbl(self.trueLbl)

                lblAndOr =  generador.newLabel()

                self.op_izq.setFalseLbl(lblAndOr)
                self.op_der.setFalseLbl(self.falseLbl)
                
            elif self.op == '!':
                self.op_izq.setFalseLbl(self.trueLbl) 
                self.op_izq.setTrueLbl(self.falseLbl)
                lblNot = self.op_izq.compilar( arbol, tabla)
                if isinstance(lblNot, Excepcion): return lblNot

                if lblNot.getTipo() != 'boolean':
                    return Excepcion("Semantico", "No se puede utilizar la expresion booleana en: ", self.fila, self.colum)
                
                lbltrue = lblNot.getTrueLbl()
                lblfalse = lblNot.getFalseLbl()
                lblNot.setTrueLbl(lblfalse)
                lblNot.setFalseLbl(lbltrue)
                self.setTipo('boolean')
                
                return lblNot

            left = self.op_izq.interpretar( arbol, tabla)
            if isinstance(left, Excepcion): return left

            if left.getTipo() != 'boolean':
                return Excepcion("Semantico", "No se puede utilizar la expresion booleana en: ", self.fila, self.colum)

            generador.putLabel(lblAndOr)
            right = self.op_der.interpretar( arbol, tabla)
            if isinstance(right, Excepcion): return right

            if right.getTipo() != 'boolean':
                return Excepcion("Semantico", "No se puede utilizar la expresion booleana en: ", self.fila, self.colum)
            
            generador.addComment("Fin de compilacion de Expresion Logica")
            generador.addSpace()

            ret = Return(None, 'boolean', False)
            ret.setTrueLbl(self.trueLbl)
            ret.setFalseLbl(self.falseLbl)
            return ret

    def checkLabels(self):
        genAux = Generador()
        generador = genAux.getInstance()
        if self.trueLbl == '':
            self.trueLbl = generador.newLabel()
        if self.falseLbl == '':
            self.falseLbl = generador.newLabel()

    def getTipo(self):
        return self.tipo

    def getNum(self):
        if self.op == '===':
            return '1'
        if self.op == '!==':
            return '0'

    def getOperador(self):
        if self.op == '===':
            return '=='
        if self.op == '!==':
            return '!='
        return self.op