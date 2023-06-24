from typing import List
from ..Instrucciones._return import Return
from ..Abstract.return__ import Return as Return2
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.excepcion import Excepcion
from ..Tabla_Simbolos.tabla_simbolos import TablaSimbolos


class Llamada_Funcion(Abstract):

    def __init__(self, nombre, parametros, fila, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.trueLbl = ''
        self.falseLbl = ''
        super().__init__(fila, columna)
    
    def interpretar(self, arbol, tabla):
        genAux = Generador()
        generador = genAux.getInstance()
        funcion = arbol.getFuncion(self.nombre)

        if funcion != None:
            generador.addComment(f'Llamada a la funcion {self.nombre}')
            paramValues = []
            temps = []
            size = tabla.size

            for parametros in self.parametros:
                if isinstance(parametros, Llamada_Funcion):
                    self.guardarTemps(generador, tabla, temps)
                    a = parametros.interpretar(arbol, tabla)
                    if isinstance(a, Excepcion): return a
                    paramValues.append(a)
                    self.recuperarTemps(generador, tabla, temps)
                else:
                    value = parametros.interpretar(arbol, tabla)
                    if isinstance(value, Excepcion):
                        return value
                    paramValues.append(value)
                    temps.append(value.getValue())
            
            temp = generador.addTemp()

            generador.addExp(temp,'P',size+1, '+')
            aux = 0
            if len(funcion.getParams()) == len(paramValues):
                for param in paramValues:
                    if funcion.parametros[aux]['tipo'] == param.getTipo():
                        aux += 1
                        generador.setStack(temp,param.getValue())
                        if aux != len(paramValues):
                            generador.addExp(temp,temp,1,'+')
                    else:
                        generador.addComment(f'Fin de la llamada a la funcion {self.nombre} por error, consulte la lista de errores')
                        return Excepcion("Semantico", f"El tipo de dato de los parametros no coincide con la funcion {self.nombre}", self.fila, self.columna)

            generador.newEnv(size)
            self.getFuncion(generator=generador) # Sirve para llamar a una funcion nativa
            generador.callFun(funcion.nombre)
            generador.getStack(temp,'P')
            generador.retEnv(size)
            generador.addComment(f'Fin de la llamada a la funcion {self.nombre}')
            generador.addSpace()

            if funcion.getTipo() != 'boolean':
                return Return2(temp, funcion.getTipo(), True)
            else:
                generador.addComment('Recuperacion de booleano')
                if self.trueLbl == '':
                    self.trueLbl = generador.newLabel()
                if self.falseLbl == '':
                    self.falseLbl = generador.newLabel()
                generador.addIf(temp,1,'==',self.trueLbl)
                generador.addGoto(self.falseLbl)
                ret = Return(temp, funcion.getTipo(), True)
                ret.trueLbl = self.trueLbl
                ret.falseLbl = self.falseLbl
                generador.addComment('Fin de recuperacion de booleano')
                return ret

    def guardarTemps(self, generador, tabla, tmp2):
        generador.addComment('Guardando temporales')
        tmp = generador.addTemp()
        for tmp1 in tmp2:
            generador.addExp(tmp, 'P', tabla.size, '+')
            generador.setStack(tmp, tmp1)
            tabla.size += 1
        generador.addComment('Fin de guardado de temporales')
    
    def recuperarTemps(self, generador, tabla, tmp2):
        generador.addComment('Recuperando temporales')
        tmp = generador.addTemp()
        for tmp1 in tmp2:
            tabla.size -= 1
            generador.addExp(tmp, 'P', tabla.size, '+')
            generador.getStack(tmp1, tmp)
        generador.addComment('Fin de recuperacion de temporales')

    def getFuncion(self, generator):
        if self.nombre == 'length':
            generator.fLength()
        elif self.nombre == 'trunc':
            generator.fTrunc()
        elif self.nombre == 'float':
            generator.fFloat()
        elif self.nombre == 'uppercase':
            generator.fUpperCase()
        elif self.nombre == 'lowercase':
            generator.fLowerCase()
        return