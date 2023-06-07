import ply.yacc as yacc
from Analizador_Lexico import tokens, lexer, errores, find_column
from src.Expresiones.aritmetica import Aritmetica
from src.Expresiones.primitivos import Primitivos
from src.Instrucciones.imprimir import Imprimir

precedence = (
    ('left','MAS','MENOS'),
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
                    | condicional_if PTCOMA'''
    t[0] = t[1]

def p_imprimir(t):
    'imprimir : RCONSOLE PUNTO RLOG PARI expresion PARD'
    t[0] = Imprimir(t[5], t.lineno(1), find_column(input, t.slice[1]))

def p_declaracion_normal(t):
    'declaracion_normal : RLET ID DPUNTOS tipo IGUAL expresion'
    print('Variable:',t[2],'Tipo de dato:',t[4],'Expresion:',t[6])
    t[0] = [t[2], t[4], t[6]]

def p_condicional_if(t):
    'condicional_if : RIF PARI expresion PARD LLAVEIZQ LLAVEDER'
    print('Expresion:',t[3])
    t[0] = t[3]

def p_tipo(t):
    '''tipo : RSTRING
            | RNUMBER
            | RBOOLEAN'''
    t[0] = t[1]

def p_expresion_binaria(t):
    '''expresion : expresion MAS expresion
                | expresion MENOS expresion
                | expresion POR expresion
                | expresion DIV expresion'''
    if t[2] == '+'  : 
        t[0] = Aritmetica(t[1], t[3], '+', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Aritmetica(t[1], t[3], '-', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*': 
        t[0] = Aritmetica(t[1], t[3], '*', t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/': 
        t[0] = Aritmetica(t[1], t[3], '/', t.lineno(2), find_column(input, t.slice[2]))

def p_expresion_unaria(t):
    'expresion : MENOS expresion %prec UMENOS'
    t[0] = -t[2]

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
console.log("Hola, estoy siendo interpretado");
console.log(4+"Hola"); // No la camioneta vaconsole.log(4+2-6*3);
console.log(4/0);
'''

def test_lexer(lexer):
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)

# lexer.input(entrada)
# test_lexer(lexer)
instrucciones = parse(entrada)
for instr in instrucciones:
    instr.interpretar(None, None)


