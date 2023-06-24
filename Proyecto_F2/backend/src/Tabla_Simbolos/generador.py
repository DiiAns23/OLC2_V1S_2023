
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
        self.compareString = False
        self.boundError = False
        self.upper = False
        self.lower = False

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
        self.codeIn('return;\n}\n');
        if(not self.inNatives):
            self.inFunc = False
        
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
        self.codeIn(f'P = P + {size};\n')
    
    def callFun(self, id):
        self.codeIn(f'{id}();\n')
    
    def retEnv(self, size):
        self.codeIn(f'P = P - {size};\n')

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
        self.codeIn(f'fmt.Printf("%{type}", {value});\n')
    
    def addPrintChar(self, value):
        self.setImport('fmt')
        self.codeIn(f'fmt.Printf("%c", int({value}));\n')
    

    def printTrue(self):
        self.setImport('fmt')
        self.addIdent()
        self.addPrint("c", 116)
        self.addIdent()
        self.addPrint("c", 114)
        self.addIdent()
        self.addPrint("c", 117)
        self.addIdent()
        self.addPrint("c", 101)
    
    def printFalse(self):
        self.setImport('fmt')
        self.addIdent()
        self.addPrint("c", 102)
        self.addIdent()
        self.addPrint("c", 97)
        self.addIdent()
        self.addPrint("c", 108)
        self.addIdent()
        self.addPrint("c", 115)
        self.addIdent()
        self.addPrint("c", 101)
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
        self.addPrintChar(tempC)
        self.addIdent()
        self.addExp(tempH, tempH, '1', '+')
        self.addIdent()
        self.addGoto(compareLbl)
        self.putLabel(returnLbl)
        self.addEndFunc()
        self.inNatives = False

    def fcompareString(self):
        if self.compareString:
            return
        self.compareString = True
        self.inNatives = True

        self.addBeginFunc("compareString")
        # Label para salir de la funcion
        returnLbl = self.newLabel()

        t2 = self.addTemp()
        self.addExp(t2, 'P', '1', '+')
        t3 = self.addTemp()
        self.getStack(t3, t2)
        self.addExp(t2,t2,'1', '+')
        t4 = self.addTemp()
        self.getStack(t4, t2)

        l1 = self.newLabel()
        l2 = self.newLabel()
        l3 = self.newLabel()
        self.putLabel(l1)

        t5 = self.addTemp()
        self.addIdent()
        self.getHeap(t5,t3)

        t6 = self.addTemp()
        self.addIdent()
        self.getHeap(t6,t4)

        self.addIdent()
        self.addIf(t5,t6,'!=', l3)
        self.addIdent()
        self.addIf(t5,'-1', '==', l2)

        self.addIdent()
        self.addExp(t3, t3,'1', '+')
        self.addIdent()
        self.addExp(t4, t4,'1','+')
        self.addIdent()
        self.addGoto(l1)

        self.putLabel(l2)
        self.addIdent()
        self.setStack('P', '1')
        self.addIdent()
        self.addGoto(returnLbl)
        self.putLabel(l3)
        self.addIdent()
        self.setStack('P', '0')
        self.putLabel(returnLbl)
        self.addEndFunc()
        self.inNatives = False
    
    def fboundError(self):
        if self.boundError:
            return
        self.boundError = True
        self.inNatives = True
        self.addBeginFunc('BoundsError')
        error = "Bounds Error \n"
        for char in error:
            self.addPrint("c",ord(char))
        self.addEndFunc()
        self.addSpace()
        self.inNatives = False

    def fUpperCase(self):
        if self.upper:
            return
        self.upper = True
        self.inNatives = True
        
        self.addBeginFunc('uppercase')
        
        t1 = self.addTemp()
        t2 = self.addTemp()
        t3 = self.addTemp()

        Lbl0 = self.newLabel()
        Lbl1 = self.newLabel()
        Lbl2 = self.newLabel()

        self.addAsig(t1, 'H')
        self.addExp(t2, 'P', '1','+')
        self.getStack(t2, t2)
        self.putLabel(Lbl0)

        self.getHeap(t3, t2)
        self.addIf(t3, '-1', '==', Lbl2)
        self.addIf(t3, '97', '<', Lbl1)
        self.addIf(t3, '122', '>', Lbl1)
        self.addExp(t3, t3,'32', '-')
        self.putLabel(Lbl1)
    
        self.setHeap('H', t3)
        self.nextHeap()
        self.addExp(t2, t2, '1','+')
        self.addGoto(Lbl0)

        self.putLabel(Lbl2)
        self.setHeap('H', '-1')
        self.nextHeap()
        self.setStack('P', t1)
        self.addEndFunc()

        self.inNatives = False

    def fLowerCase(self):
        if self.lower:
            return
        self.lower = True
        self.inNatives = True
        
        self.addBeginFunc('lowercase')
        
        t1 = self.addTemp()
        t2 = self.addTemp()
        t3 = self.addTemp()

        Lbl0 = self.newLabel()
        Lbl1 = self.newLabel()
        Lbl2 = self.newLabel()

        self.addAsig(t1, 'H')
        self.addExp(t2, 'P', '1','+')
        self.getStack(t2, t2)
        self.putLabel(Lbl0)

        self.getHeap(t3, t2)
        self.addIf(t3, '-1', '==', Lbl2)
        self.addIf(t3, '65', '<', Lbl1)
        self.addIf(t3, '90', '>', Lbl1)
        self.addExp(t3, t3,'32', '+')
        self.putLabel(Lbl1)
    
        self.setHeap('H', t3)
        self.nextHeap()
        self.addExp(t2, t2, '1','+')
        self.addGoto(Lbl0)

        self.putLabel(Lbl2)
        self.setHeap('H', '-1')
        self.nextHeap()
        self.setStack('P', t1)
        self.addEndFunc()

        self.inNatives = False
# console.log(4+5*6);