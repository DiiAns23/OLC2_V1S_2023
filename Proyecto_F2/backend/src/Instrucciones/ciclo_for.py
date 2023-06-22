from ..Tabla_Simbolos.simbolo import Simbolo
from ..Instrucciones._return import Return
from ..Tabla_Simbolos.generador import Generador
from ..Abstract.abstract import Abstract
from ..Tabla_Simbolos.excepcion import Excepcion
from ..Tabla_Simbolos.tabla_simbolos import TablaSimbolos

class For(Abstract):

    def __init__(self, inicio, condicion, aumento, bloqueFor, fila, columna):
        self.inicio = inicio
        self.condicion = condicion
        self.aumento = aumento
        self.bloqueFor = bloqueFor
        super().__init__(fila, columna)
    
    def interpretar(self, arbol, tabla):
        genAux = Generador()
        generador = genAux.getInstance()
        generador.addComment('Compilacion de un for')

        bandera = True
        entorno = tabla
        if tabla.findTabla(self.inicio.ide):
            bandera = False


        nuevaTabla = TablaSimbolos(tabla)  # NUEVO ENTORNO

        inicio = self.inicio.interpretar(arbol, nuevaTabla)
        if isinstance(inicio, Excepcion): return inicio

        condicion = self.condicion.interpretar(arbol, nuevaTabla)
        if isinstance(condicion, Excepcion): return condicion
        # Validar que el tipo sea booleano
        if self.condicion.tipo != 'boolean':
            return Excepcion("Semantico", "Tipo de dato no booleano en FOR.", self.fila, self.columna)
        # Recorriendo las instrucciones
        while condicion:
            for instruccion in self.bloqueFor:
                result = instruccion.interpretar(arbol, nuevaTabla)
                if isinstance(result, Excepcion):
                    arbol.excepciones.append(result)
            
            nuevo_valor = self.aumento.interpretar(arbol, nuevaTabla)
            if isinstance(nuevo_valor, Excepcion): return nuevo_valor
            
            simbolo = Simbolo(self.inicio.ide, self.inicio.tipo, nuevo_valor, self.fila, self.columna)

            # Actualizando el valor de la variable en la tabla de simbolos
            valor = nuevaTabla.updateTabla(simbolo)

            if isinstance(valor, Excepcion): return valor

            condicion = self.condicion.interpretar(arbol, nuevaTabla)
            if isinstance(condicion, Excepcion): return condicion
            if self.condicion.tipo != 'boolean':
                return Excepcion("Semantico", "Tipo de dato no booleano en FOR.", self.fila, self.columna)
        return None
            



