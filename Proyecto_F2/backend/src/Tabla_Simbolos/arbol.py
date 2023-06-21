class Arbol:
    
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones
        self.funciones = {}
        self.excepciones = []
        self.consola = ""
        self.tsglobal = None
        self.tsgInterpretada = {}
    
    # Hacer los getters y setters de cada atributo

    def setTsgI(self, entorno, valor):
        self.tsgInterpretada[entorno] = valor
    
    def getTsgI(self):
        return self.tsgInterpretada # devolvemos el entorno global

    def getInstr(self):
        return self.instrucciones

    def setInstr(self, instrucciones):
        self.instrucciones = instrucciones
    
    def getFunciones(self):
        return self.funciones
    
    def setFunciones(self, id, function):
        if id in self.funciones.keys():
            return "error"
        else:
            self.funciones[id] = function

    def getFuncion(self, ide):
        actual = self
        if actual!=None:
            if ide in actual.funciones.keys():
                return actual.funciones[ide]
        return None

    def setStruct(self,id, struct):
        if id in self.structs.keys():
            return "error"
        else:
            self.structs[id] = struct

    def getStruct(self,id):
        actual = self
        if actual!=None:
            if id in actual.structs.keys():
                return actual.structs[id]
        return None
    
    def getExcepciones(self):
        return self.excepciones
    
    def setExcepciones(self, excepciones):
        self.excepciones.append(excepciones)
    
    def getConsola(self):
        return self.consola
    
    def setConsola(self, consola):
        self.consola = consola
    
    def updateConsola(self, consola):
        self.consola += consola + '\n'
    
    def getTsglobal(self):
        return self.tsglobal

    def setTsglobal(self, tsglobal):
        self.tsglobal = tsglobal
    
