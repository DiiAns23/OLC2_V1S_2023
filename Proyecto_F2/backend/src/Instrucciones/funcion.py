from typing import List
from ..Instrucciones._return import Return
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.excepcion import Excepcion
from ..Tabla_Simbolos.tabla_simbolos import TablaSimbolos

class Funcion(Abstract):

    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.tipo = 'string'
        self.recTemp = True
        super().__init__(fila, columna)
    

    def interpretar(self, arbol, tabla):
        funcion = arbol.setFunciones(self.nombre, self)
        if funcion == 'error':
            error = Excepcion("Semantico", f"Ya existe la funcion {self.nombre}", self.fila, self.columna)
            return error
        
        genAux = Generador()
        generador = genAux.getInstance()
        generador.addComment(f'Compilacion de la funcion {self.nombre}')

        entorno = TablaSimbolos(tabla)

        Lblreturn = generador.newLabel()
        entorno.returnLbl = Lblreturn
        entorno.size = 1

        if self.parametros != None:
            for parametro in self.parametros:
                if parametro['tipo'] == 'struct':
                    simbolo = entorno.setTabla(parametro['id'], parametro['tipo'], True)
                elif not isinstance(parametro['tipo'], List):
                    simbolo = entorno.setTabla(parametro['id'], parametro['tipo'], (parametro['tipo'] == 'string' or parametro['tipo'] == 'array' or parametro['tipo'] == 'struct'))
                else:
                    simbolo = entorno.setTabla(parametro['id'], parametro['tipo'][0], True)
                    simbolo.setTipoAux(parametro['tipo'][1])
                    if parametro['tipo'][0] == 'struct':
                        struct = arbol.getStruct(parametro['tipo'][1])
                        simbolo.setParams(struct.getParams())
            
        
        generador.addBeginFunc(self.nombre)

        for instruccion in self.instrucciones:
            value = instruccion.interpretar(arbol, entorno)
            if isinstance(value, Excepcion):
                arbol.setExcepcion(value)
            if isinstance(value, Return):
                if value.getTrueLbl() == '':
                    generador.addComment('Resultado a retornar en la funcion')
                    generador.setStack('P',value.getValor())
                    generador.addGoto(entorno.returnLbl)
                    generador.addComment('Fin del resultado a retornar')
                else:
                    generador.addComment('Resultado a retornar en la funcion')
                    generador.putLabel(value.getTrueLbl())
                    generador.setStack('P', '1')
                    generador.addGoto(entorno.returnLbl)
                    generador.putLabel(value.getFalseLbl())
                    generador.setStack('P', '0')
                    generador.addGoto(entorno.returnLbl)
                    generador.addComment('Fin del resultado a retornar')

        generador.addGoto(Lblreturn)
        generador.putLabel(Lblreturn)

        generador.addComment(f'Fin de la compilacion de la funcion {self.nombre}')
        generador.addEndFunc()
        generador.addSpace()
        return


    def getParams(self):
        return self.parametros

    def getTipo(self):
        return self.tipo