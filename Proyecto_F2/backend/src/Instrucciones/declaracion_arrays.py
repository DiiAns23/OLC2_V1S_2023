from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.simbolo import Simbolo
from ..Tabla_Simbolos.excepcion import Excepcion
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.return__ import Return
from typing import List

class Declaracion_Arrays(Abstract):

    def __init__(self,id, fila, columna, values = None, tipoAux = None):
        self.id = id
        self.values = values
        self.tipoAux = tipoAux
        self.tipo = 'array'
        self.length = len(values)
        self.multiDim = False
        self.isinStruct = False
        super().__init__(fila, columna)

    def interpretar(self, arbol, tabla):
        genAux = Generador()
        generator = genAux.getInstance()

        if self.values:
            if isinstance(self.tipoAux, List):
                if self.tipo == self.tipoAux[0]:
                    generator.addComment('Compilacion del Array')
                    t0 = generator.addTemp()
                    t1 = generator.addTemp()
                    generator.addAsig(t0,'H')
                    generator.addExp(t1,t0,'1','+')
                    generator.setHeap('H', len(self.values))
                    apuntador = str(len(self.values)+1)
                    generator.addExp('H','H',apuntador,'+')
                    generator.addSpace()
                    length = 0
                    for value in self.values:
                        if not isinstance(Declaracion_Arrays):
                            val = value.interpretar(arbol, tabla)
                            if isinstance(val, Excepcion): return val
                            try:
                                # if val.getTipo() == Tipo.STRUCT:
                                #     if [val.getTipo(), val.getTipoAux()] == self.tipoAux[1]:
                                #         generator.setHeap(t1,val.getValue())
                                #         generator.addExp(t1,t1,'1','+')
                                #         generator.addSpace()
                                #         length += 1    
                                #     else:
                                #         return Excepcion("Semantico", "Tipos no coinciden en declaracion o asignacion del array", self.fila, self.colum)    
                                #elif 
                                if val.getTipo() == self.tipoAux[1]:
                                    generator.setHeap(t1,val.getValue())
                                    generator.addExp(t1,t1,'1','+')
                                    generator.addSpace()
                                    length += 1.
                                else:
                                    return Excepcion("Semantico", "Tipos no coinciden en declaracion o asignacion del array", self.fila, self.columna)
                            except:
                                'Error'
                    simbolo = tabla.setTabla(self.id,self.tipo,True)
                    simbolo.setTipoAux(self.tipoAux[1])
                    simbolo.setLength(length)
                    tempPos = simbolo.pos
                    if not simbolo.isGlobal:
                        tempPos = generator.addTemp()
                        generator.addExp(tempPos, 'P', simbolo.pos, "+")
                    generator.setStack(tempPos, t0)
                    generator.addComment('Fin de la compilacion del Array')
            else:
                generator.addComment('Compilacion del Array')
                t0 = generator.addTemp()
                t1 = generator.addTemp()
                generator.addAsig(t0,'H')
                generator.addExp(t1,t0,'1','+')
                generator.setHeap('H', len(self.values))
                apuntador = str(len(self.values)+1)
                generator.addExp('H','H',apuntador,'+')
                generator.addSpace()
                length = 0
                tipoAux = []
                tipoAux.append('array')
                aux = ''
                for value in self.values:
                    if not isinstance(value, Declaracion_Arrays):
                        val = value.interpretar(arbol,tabla)
                        if isinstance(val, Excepcion): return val
                        aux = val.getTipo()
                        generator.setHeap(t1,val.getValue())
                        generator.addExp(t1,t1,'1','+')
                        generator.addSpace()
                        length += 1
                    else:
                        value.multiDim = True
                        value.tipoAux = value.getTipo()
                        val = value.interpretar(arbol,tabla)
                        if isinstance(val, Excepcion): return val
                        tipoAux.append(val.getTipoAux())
                        generator.setHeap(t1,val.getValue())
                        generator.addExp(t1,t1,'1','+')
                        generator.addSpace()
                        length += 1
                tipoAux.append(aux)
                if self.multiDim:
                    return Return(t0, 'array', True, tipoAux)
                if self.isinStruct == False:
                    simbolo = tabla.setTabla(self.id,self.tipo,True)
                    simbolo.setTipoAux(tipoAux)
                    simbolo.setLength(length)
                    tempPos = simbolo.pos
                    if not simbolo.isGlobal:
                        tempPos = generator.addTemp()
                        generator.addExp(tempPos, 'P', simbolo.pos, "+")
                    generator.setStack(tempPos, t0)
                    generator.addComment('Fin de la compilacion del Array')
                else:
                    return Return(t0, 'array', True, tipoAux)
    def getTipoAux(self):
        return self.tipoAux
    
    def setTipoAux(self, tipo):
        self.tipoAux = tipo

    def getTipo(self):
        return self.tipo
    
    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id
    
    def getLength(self):
        return self.length