class Arbol:
    
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones
        self.funciones = []
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
    
    def setFunciones(self, funciones):
        self.funciones.append(funciones)

    def getFuncion(self, ide):
        for funcion in self.funciones:
            if funcion.nombre == ide:
                return funcion
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
    
