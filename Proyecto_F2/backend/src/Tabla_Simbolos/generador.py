
class Generador:

    generator = None

    def __init__(self):
        # Contadores
        self.countTemp = 0

        # Codigo
        self.codigo = ""

        # Lista de temporales
        self.temps = []

        # Lista de Nativas


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
        return f'{self.getHeader()}\nfunc main(){{\n{self.codigo}\n}}'

    def addComment(self, comment):
        self.codigo += f'/* {comment} */\n'
    
    def addSpace(self):
        self.codigo += '\n'

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


    ###################
    # GOTO
    ###################


    ###################
    # IF
    ###################

    ###################
    # EXPRESIONES
    ###################
    def addExp(self, result, left, right, op):
        self.codigo += f'{result} = {left} {op} {right};\n'
    
    def addAsig(self, result, left):
        self.codigo += f'{result} = {left};\n'

    ###############
    # STACK
    ###############

    def setStack(self,pos, value):
        self.codigo += f'stack[int({pos})] = {value};\n'
    
    def getStack(self, place, pos):
        self.codigo += f'{place} = stack[int({pos})];\n'
    
    #############
    # ENTORNO
    #############

    def newEnv(self, size):
        self.codigo += '/* --- NUEVO ENTORNO --- */\n'
        self.codigo += f'P = P + {size};\n'
    
    def callFun(self, id):
        self.codigo += f'{id}();\n'
    
    def retEnv(self, size):
        self.codigo += f'P = P - {size};\n'
        self.codigo += '/* --- RETORNO DE ENTORNO --- */\n'

    ###############
    # HEAP
    ###############

    def setHeap(self, pos, value):
        self.codigo += f'heap[int({pos})] = {value};\n'

    def getHeap(self, place, pos):
        self.codigo += f'{place} = heap[int({pos})];\n'

    def nextHeap(self):
        self.codigo += 'H = H + 1;\n'

    ###############
    # INSTRUCCIONES
    ###############

    def addPrint(self, type, value):
        self.setImport('fmt')
        self.codigo += f'fmt.Printf("%{type}", {value});\n' # %d %f %c %s
    

# console.log(4+5*6);