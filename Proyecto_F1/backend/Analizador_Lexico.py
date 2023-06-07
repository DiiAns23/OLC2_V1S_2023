import re
import ply.lex as lex

errores = []

reserved = {
    'console'     :   'RCONSOLE',
    'log'         :   'RLOG',
    'let'         :   'RLET',
    'string'      :   'RSTRING',
    'number'      :   'RNUMBER',
    'boolean'     :   'RBOOLEAN',
    'true'        :   'RTRUE',
    'false'       :   'RFALSE',
    'if'          :   'RIF',
    'else'        :   'RELSE',

}

tokens  = [
    'PUNTO',
    'DPUNTOS',
    'PTCOMA',
    'PARI',
    'PARD',
    'LLAVEIZQ',
    'LLAVEDER',
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'IGUAL',
    'ENTERO',
    'DECIMAL',
    'CADENA',
    'ID',
]+ list(reserved.values())
# Tokens
t_PUNTO         = r'\.'
t_DPUNTOS       = r'\:'
t_PTCOMA        = r'\;'
t_PARI          = r'\('
t_PARD          = r'\)'
t_LLAVEIZQ      = r'\{'
t_LLAVEDER      = r'\}'
t_MAS           = r'\+'
t_MENOS         = r'\-'
t_POR           = r'\*'
t_DIV           = r'\/'
t_IGUAL         = r'\='

#Decimal
def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

#Entero
def t_ENTERO(n):
    r'\d+'
    try:
        if(n.value != None):
            n.value = int(n.value)
        else:
            n.value = 'nothing'
    except ValueError:
        print("Valor del entero demasiado grande %d", n.value)
        n.value = 0
    return n

#Cadena
def t_CADENA(t):
    r'(\".*?\")'
    t.value = t.value[1:-1] #Se remueven las comillas de la entrada
    t.value = t.value.replace('\\t','\t')
    t.value = t.value.replace('\\n','\n')
    t.value = t.value.replace('\\"','\"')
    t.value = t.value.replace("\\'","\'")
    t.value = t.value.replace('\\\\','\\')
    return t

#Identificador
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')# Check for reserved words
    return t

#Comentario de Una Linea
def t_Com_Simple(t):
    r'\/\/.*'
    t.lexer.lineno += 1

#Comentario Multilinea
def t_Com_Multiple(t):
    r'\/\*(.|\n)*?\*\/'
    t.lexer.lineno += t.value.count('\n')
    
#Nueva Linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Caracteres ignorados
t_ignore = " \t"

#Error
def t_error(t):
    t.lexer.skip(1)

def find_column(inp, tk):
    line_start = inp.rfind('\n', 0, tk.lexpos) + 1
    return (tk.lexpos - line_start) + 1

def test_lexer(lexer):
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)

lexer = lex.lex(reflags = re.IGNORECASE)