class Simbolo():

    def __init__(self, ide, tipo, valor, fila, columna):
        self.ide = ide
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna
    
    def getID(self):
        return self.ide

    def setID(self, ide):
        self.ide = ide

    def getTipo(self):
        return self.tipo
    
    def setTipo(self, tipo):
        self.tipo = tipo
    
    def getValor(self):
        return self.valor
    
    # Aqui va lo del array :3
    
    def setValor(self, valor):
        self.valor = valor
    
    def getFila(self):
        return self.fila
    
    def setFila(self, fila):
        self.fila = fila
    
    def getColumna(self):
        return self.columna

    def setColumna(self, columna):
        self.columna = columna