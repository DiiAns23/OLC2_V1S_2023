from src.Nativas.uppercase import UpperCase
from src.Tabla_Simbolos.generador import Generador
from src.Instrucciones._return import Return
from src.Instrucciones.llamada_funcion import Llamada_Funcion
from src.Instrucciones.funcion import Funcion
from src.Instrucciones.ciclo_for import For
from src.Instrucciones.condicional_if import If
from src.Expresiones.relacional_logica import Relacional_Logica
from src.Expresiones.identificador import Identificador
from src.Tabla_Simbolos.arbol import Arbol
from src.Tabla_Simbolos.excepcion import Excepcion
import ply.yacc as yacc
from Analizador_Lexico import tokens, lexer, errores, find_column
from src.Expresiones.aritmetica import Aritmetica
from src.Expresiones.primitivos import Primitivos
from src.Expresiones.array import Array
from src.Instrucciones.imprimir import Imprimir
from src.Instrucciones.declaracion_variables import Declaracion_Variables
from src.Tabla_Simbolos.tabla_simbolos import TablaSimbolos
from src.Instrucciones.declaracion_arrays import Declaracion_Arrays
import sys
sys.setrecursionlimit(10000000)
# Definicion de la jerarquia de operadores
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right','UNOT'),
    ('left', 'COMPARE', 'DIFERENTE'),
    ('left', 'MENOR', 'MAYOR', 'MAYORIGUAL', 'MENORIGUAL'),
    ('left','MAS','MENOS', 'COMA'),
    ('left','POR','DIV'),
    ('left','PARI', 'PARD'),
    ('right','UMENOS'),
    )

# Definicion de la Gramatica
def p_init(t):
    'init : instrucciones'
    t[0] = t[1]

def p_instrucciones_lista(t):
    'instrucciones    : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_2(t):
    'instrucciones : instruccion'
    if t[1] == "":
        t[0] = []
    else:
        t[0] = [t[1]]

def p_instrucciones_evaluar(t):
    '''instruccion : imprimir PTCOMA
                    | declaracion_normal PTCOMA
                    | declaracion_arrays PTCOMA
                    | condicional_ifs PTCOMA
                    | cliclo_for PTCOMA
                    | funcion PTCOMA
                    | llamada_funcion PTCOMA
                    | r_return PTCOMA'''
    t[0] = t[1]

def p_instrucciones_evaluar_1(t):
    '''instruccion : imprimir
                    | declaracion_normal
                    | declaracion_arrays
                    | condicional_ifs
                    | cliclo_for
                    | funcion
                    | llamada_funcion
                    | r_return
                    '''
    t[0] = t[1]

def p_imprimir(t):
    'imprimir : RCONSOLE PUNTO RLOG PARI parametros_ll PARD'
    t[0] = Imprimir(t[5], t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_normal(t):
    'declaracion_normal : RLET ID DPUNTOS tipo IGUAL expresion'
    t[0] = Declaracion_Variables(t[2], t[4], t[6], t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_arrays(t):
    'declaracion_arrays : RLET ID DPUNTOS tipo IGUAL CORI parametros_ll CORD'
    t[0] = Declaracion_Arrays(t[2], t.lineno(1), find_column(input, t.slice[1]), t[7], t[4])


def p_condicional_ifs(t):
    'condicional_ifs : RIF condicional_if'
    t[0] = t[2]

def p_condicional_if(t):
    'condicional_if : PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER'
    t[0] = If(t[2], t[5], None, None, t.lineno(1), find_column(input, t.slice[1]))

def p_condicional_if_else(t):
    'condicional_if : PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER RELSE LLAVEIZQ instrucciones LLAVEDER'
    t[0] = If(t[2], t[5], t[9], None, t.lineno(1), find_column(input, t.slice[1]))

def p_condicional_if_else_if(t):
    'condicional_if : PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER RELSE RIF condicional_if'
    t[0] = If(t[2], t[5], None, t[9], t.lineno(1), find_column(input, t.slice[1]))

def p_ciclo_for(t):
    'cliclo_for : RFOR PARI declaracion_normal PTCOMA expresion PTCOMA expresion PARD LLAVEIZQ instrucciones LLAVEDER'
    t[0] = For(t[3], t[5], t[7], t[10], t.lineno(1), find_column(input, t.slice[1]))

def p_funcion(t):
    '''funcion : RFUNCTION ID PARI PARD LLAVEIZQ instrucciones LLAVEDER
                | RFUNCTION ID PARI parametros PARD LLAVEIZQ instrucciones LLAVEDER'''
    if len(t) == 6:
        t[0] = Funcion(t[2],None,t[6], t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Funcion(t[2], t[4], t[7], t.lineno(1), find_column(input, t.slice[1]))

def p_llamada_funcion(t):
    '''llamada_funcion : ID PARI PARD
                        | ID PARI parametros_ll PARD''' 
    # (let nombre: string, let apellido: string, let edad: number)
    if len(t) == 3:
        t[0] = Llamada_Funcion(t[1],None,t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Llamada_Funcion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_parametros(t):
    'parametros : parametros COMA parametro'
    t[1].append(t[3])
    t[0] = t[1]

def p_parametros_2(t):
    'parametros : parametro'
    t[0] = [t[1]]

def p_parametro(t):
    '''parametro : RLET ID DPUNTOS tipo  
                | ID DPUNTOS tipo
                | ID'''
    if len(t) == 2:
        t[0] = {'tipo': 'any', 'id': t[1]}
    elif len(t) == 4:
        t[0] = {'tipo': t[3], 'id': t[1]}
    else:
        t[0] = {'tipo': t[4], 'id': t[2]}

def p_parametros_ll(t):
    'parametros_ll : parametros_ll COMA parametro_ll'
    t[1].append(t[3])
    t[0] = t[1]

def p_parametros_ll_2(t):
    'parametros_ll : parametro_ll'
    t[0] = [t[1]]

def p_parametro_ll(t):
    '''parametro_ll : expresion'''
    t[0] = t[1]


def p_tipo(t):
    '''tipo : RSTRING
            | RNUMBER
            | RBOOLEAN'''
    t[0] = t[1]

def p_expresion_binaria(t):
    '''expresion : expresion MAS expresion
                | expresion MENOS expresion
                | expresion POR expresion
                | expresion DIV expresion
                | expresion COMPARE expresion
                | expresion DIFERENTE expresion
                | expresion MAYOR expresion
                | expresion MENOR expresion
                | expresion MAYORIGUAL expresion
                | expresion MENORIGUAL expresion
                | expresion AND expresion
                | expresion OR expresion
                '''
    if t[2] == '+'  : 
        t[0] = Aritmetica(t[1], t[3], '+', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Aritmetica(t[1], t[3], '-', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*': 
        t[0] = Aritmetica(t[1], t[3], '*', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/': 
        t[0] = Aritmetica(t[1], t[3], '/', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '===':
        t[0] = Relacional_Logica(t[1], t[3], '===', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '!==':
        t[0] = Relacional_Logica(t[1], t[3], '!==', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>':
        t[0] = Relacional_Logica(t[1], t[3], '>', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<':
        t[0] = Relacional_Logica(t[1], t[3], '<', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>=':
        t[0] = Relacional_Logica(t[1], t[3], '>=', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<=':
        t[0] = Relacional_Logica(t[1], t[3], '<=', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '&&':
        t[0] = Relacional_Logica(t[1], t[3], '&&', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '||':
        t[0] = Relacional_Logica(t[1], t[3], '||', t.lineno(2), find_column(input, t.slice[2]))
    
def p_expresion_unaria(t):
    '''expresion : MENOS expresion %prec UMENOS
                | NOT expresion %prec UNOT'''
    if t[1] == '-':
        t[0] = Aritmetica(0, t[2], '-', t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == '!':
        t[0] = Relacional_Logica(t[2], None, '!', t.lineno(1), find_column(input, t.slice[1]))

def p_params_arrays(t):
    'arrays_1 : arrays_1 CORI arrays_2 CORD'
    t[1].append(t[3])
    t[0] = t[1]

def p_params_arrays_2(t):
    'arrays_1 : CORI arrays_2 CORD'
    t[0] = [t[2]]

def p_params_arrays_3(t):
    'arrays_2 : expresion'
    t[0] = t[1]

def p_params_arrays_4(t):
    'expresion : ID arrays_1'
    t[0] = Array(t[1], t[2], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_array(t):
    'expresion : CORI parametros_ll CORD'
    t[0] = Declaracion_Arrays('', t.lineno(1), find_column(input, t.slice[1]), t[2])

def p_expresion_agrupacion(t):
    'expresion : PARI expresion PARD'
    t[0] = t[2]

def p_identificador(t):
    'expresion : ID'
    t[0] = Identificador(t[1], t.lineno(1), find_column(input, t.slice[1]), None)

def p_expresion_entero(t):
    'expresion : ENTERO'
    t[0] = Primitivos('number', int(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_decimal(t):
    'expresion : DECIMAL'
    t[0] = Primitivos('number', float(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_cadena(t):
    'expresion : CADENA'
    t[0] = Primitivos('string', str(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_boolean(t):
    '''expresion : RTRUE
                | RFALSE'''
    if t[1] == 'true':
        t[0] = Primitivos('boolean', True, t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Primitivos('boolean', False, t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_incrementable(t):
    '''expresion : expresion MAS MAS
                | expresion MENOS MENOS'''
    if t[2] == '+':
        incrementable = Primitivos('number', 1, t.lineno(2), find_column(input, t.slice[2]))
        t[0] = Aritmetica(t[1],incrementable, '+', t.lineno(2), find_column(input, t.slice[2]))
    else:
        incrementable = Primitivos('number', 1, t.lineno(2), find_column(input, t.slice[2]))
        t[0] = Aritmetica(t[1],incrementable, '-', t.lineno(2), find_column(input, t.slice[2]))


def p_expresion_funcion(t):
    'expresion : llamada_funcion'
    t[0] = t[1]
    
def p_return(t):
    'r_return : RRETURN expresion'
    t[0] = Return(t[2], t.lineno(1), find_column(input, t.slice[1]))

def agregarNativas(ast):
    nombre = "uppercase"
    params = [{'tipo':'string', 'ide':'uppercase##Param1'}]
    inst = []
    upper = UpperCase(nombre, params, inst, 'string', -1, -1)
    ast.setFunciones('uppercase',upper)

def p_error(t):
    print(" Error sintáctico en '%s'" % t.value)

input = ''

def parse(inp):
    global errores
    global parser
    errores = []
    parser = yacc.yacc()
    global input
    input = inp
    lexer.lineno = 1
    return parser.parse(inp)

entrada = '''
let a:string = "hola";

console.log(uppercase(a));
'''

def test_lexer(lexer):
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)

# lexer.input(entrada)
# test_lexer(lexer)

genAux = Generador()
genAux.cleanAll(); # Limpia todos los archivos anteriores
generador = genAux.getInstance()

instrucciones = parse(entrada)
ast = Arbol(instrucciones)
tsg = TablaSimbolos()
ast.setTsglobal(tsg)

agregarNativas(ast)

for instruccion in ast.getInstr():
    value = instruccion.interpretar(ast,tsg)
    if isinstance(value, Excepcion):
        ast.setExcepciones(value)
print(generador.getCode())

