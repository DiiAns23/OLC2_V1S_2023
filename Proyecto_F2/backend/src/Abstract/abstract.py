from abc import ABC, abstractmethod

class Abstract(ABC):
    
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.trueLbl = ''
        self.falseLbl = ''
    
    @abstractmethod
    def interpretar(self, arbol, tabla):
        pass

    def getTrueLbl(self):
        return self.trueLbl
    
    def getFalseLbl(self):
        return self.falseLbl
    
    def setTrueLbl(self, trueLbl):
        self.trueLbl = trueLbl
    
    def setFalseLbl(self, falseLbl):
        self.falseLbl = falseLbl