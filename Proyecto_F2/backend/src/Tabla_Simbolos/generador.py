
class Generador:

    generator = None

    def __init__(self):
        # Contadores
        self.countTemp = 0
        self.countLabel = 0

        # Codigo
        self.codigo = ""
        self.funcs = ''
        self.natives = ''
        self.inFunc = False
        self.inNatives = False

        # Lista de temporales
        self.temps = []

        # Lista de Nativas
        self.printString = False

        # Listas de imports
        self.imports = []
        self.imports2 =['fmt', 'math']

    def getInstance(self):
        if Generador.generator == None:
            Generador.generator = Generador()
        return Generador.generator    

    def cleanAll(self):
        # Contadores
        self.countTemp = 0

        # Codigo
        self.codigo = ""

        # Lista de temporales
        self.temps = []

        # Lista de Nativas
        self.printString = False

        self.imports = []
        self.imports2 =['fmt', 'math']
        Generador.generador = Generador()

    #############
    # IMPORTS
    #############

    def setImport(self, lib):
        if lib in self.imports2:
            self.imports2.remove(lib)
        else:
            return
        
        code = f'import(\n\t"{lib}"\n)\n'
    
    #############
    # CODE
    #############

    def getHeader(self):
        code = '/* ---- HEADER ----- */\npackage main;\n\n'
        if len(self.imports) > 0:
            for temp in self.imports:
                code += temp
        if len(self.temps) > 0:
            code += 'var '
            for temp in self.temps:
                code += temp + ','
            code = code[:-1]
            code += " float64;\n\n"
        code += "var P, H float64;\nvar stack[30101999] float64;\nvar heap[30101999] float64;\n\n"

        return code

    def getCode(self):
        return f'{self.getHeader()}{self.natives}{self.funcs}\nfunc main(){{\n{self.codigo}\n}}'

    def codeIn(self, code, tab="\t"):
        if self.inNatives:
            if  self.natives == '':
                self.natives = self.natives + '/* --- NATIVAS --- */\n'
            self.natives = self.natives + tab + code
        elif self.inFunc:
            if self.funcs == '':
                self.funcs = self.funcs + '/* --- FUNCION --- */\n'
            self.funcs = self.funcs + tab + code
        else:
            self.codigo = self.codigo + tab + code

    def addComment(self, comment):
        self.codeIn(f'/* {comment} */\n')
    
    def addSpace(self):
        self.codeIn('\n')

    ########################
    # Manejo de Temporales
    ########################

    def addTemp(self):
        temp = f't{self.countTemp}'
        self.countTemp += 1
        self.temps.append(temp)
        return temp  # t1 t2 t3 t4 t5
    

    #####################
    # Manejo de Labels
    #####################

    def newLabel(self):
        label = f'L{self.countLabel}'
        self.countLabel += 1
        return label # Agregamos un nuevo label L1 L2 L3 L4 L5

    def putLabel(self, label):
        self.codeIn(f'{label}:\n')  # Lo definimos en el codigo -> L1: L2: L3:
    
    def addIdent(self):
        self.codeIn("")
    
    
    def addSpace(self):
        self.codeIn("\n")

    ###################
    # GOTO
    ###################
    def addGoto(self, label):
        self.codeIn(f'goto {label};\n')
    
    ###################
    # IF
    ###################
    def addIf(self, left, right, op, label):
        self.codeIn(f'if {left} {op} {right} {{goto {label};}}\n')

    ###################
    # EXPRESIONES
    ###################
    def addExp(self, result, left, right, op):
        self.codeIn(f'{result} = {left} {op} {right};\n')
    
    def addAsig(self, result, left):
        self.codeIn(f'{result} = {left};\n')

    ###############
    # FUNCS
    ###############

    def addBeginFunc(self, id):
        if not self.inNatives:
            self.inFunc = True
        self.codeIn(f'func {id}(){{\n')
    
    def addEndFunc(self):
        if not self.inNatives:
            self.inFunc = False
        self.codeIn('}\n')
        
    ###############
    # STACK
    ###############

    def setStack(self,pos, value):
        self.codeIn(f'stack[int({pos})] = {value};\n')
    
    def getStack(self, place, pos):
        self.codeIn(f'{place} = stack[int({pos})];\n')
    
    #############
    # ENTORNO
    #############

    def newEnv(self, size):
        self.codeIn(f'/* --- NUEVO ENTORNO --- */\n')
        self.codeIn(f'P = P + {size};\n')
    
    def callFun(self, id):
        self.codigo += f'{id}();\n'
    
    def retEnv(self, size):
        self.codigo += f'P = P - {size};\n'
        self.codigo += '/* --- RETORNO DE ENTORNO --- */\n'

    ###############
    # HEAP
    ###############

    def setHeap(self, pos, value):
        self.codeIn(f'heap[int({pos})] = {value};\n')

    def getHeap(self, place, pos):
        self.codeIn(f'{place} = heap[int({pos})];\n')

    def nextHeap(self):
        self.codeIn('H = H + 1;\n')

    ###############
    # INSTRUCCIONES
    ###############

    def addPrint(self, type, value):
        self.setImport('fmt')
        self.codeIn(f'fmt.Printf("%{type}", int({value}));\n')
    

    ###############
    # NATIVAS
    ###############

    def fPrintString(self):
        self.setImport('fmt')
        if(self.printString):
            return
        self.printString = True
        self.inNatives = True

        self.addBeginFunc('printString')
        # Label para salir de la funcion
        returnLbl = self.newLabel()
        # Label para la comparacion para buscar fin de cadena
        compareLbl = self.newLabel()
        # Temporal puntero a Stack
        tempP = self.addTemp()
        # Temporal puntero a Heap
        tempH = self.addTemp()
        self.addExp(tempP, 'P', '1', '+')
        self.getStack(tempH, tempP)
        # Temporal para comparar
        tempC = self.addTemp()
        self.putLabel(compareLbl)
        self.addIdent()
        self.getHeap(tempC, tempH)
        self.addIdent()
        self.addIf(tempC, '-1', '==', returnLbl)
        self.addIdent()
        self.addPrint('c', tempC)
        self.addIdent()
        self.addExp(tempH, tempH, '1', '+')
        self.addIdent()
        self.addGoto(compareLbl)
        self.putLabel(returnLbl)
        self.addEndFunc()
        self.inNatives = False

        
# console.log(4+5*6);