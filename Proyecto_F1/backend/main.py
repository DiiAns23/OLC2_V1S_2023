# CORS -> Cross Origin Resource Sharing
# Si no existe el CORS, no se puede acceder a los recursos de un servidor desde otro servidor
from typing import Dict, List
from Analizador_Sintactico import parse as Analizar
from src.Tabla_Simbolos.arbol import Arbol
from src.Tabla_Simbolos.excepcion import Excepcion
from src.Tabla_Simbolos.tabla_simbolos import TablaSimbolos
from Analizador_Lexico import errores, tokens, lexer
from flask import Flask, request
import json
from flask_cors import CORS
from flask.helpers import url_for
from werkzeug.utils import redirect

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ["GET"])
def saludo():
    return {"mensaje": "Hola mundo!"}

@app.route('/compilar', methods = ["POST","GET"])
def compilar():
    if request.method == "POST":
        entrada = request.data.decode("utf-8")
        entrada = json.loads(entrada)
        global tmp_val
        tmp_val = entrada["codigo"]
        return redirect(url_for("salida"))
    else:
        return {"mensaje": "No compilado"}

@app.route('/salida')
def salida():
    global tmp_val
    global Tabla
    Tabla = {}
    instrucciones = Analizar(tmp_val)
    ast = Arbol(instrucciones)
    TsgGlobal = TablaSimbolos()
    ast.setTsglobal(TsgGlobal)
    for error in errores:
        ast.setExcepciones(error)

    for instruccion in ast.getInstr():
        value = instruccion.interpretar(ast, TsgGlobal)
        if isinstance(value, Excepcion):
            ast.setExcepciones(value)

    global Simbolos
    Simbolos = ast.getTsglobal().getTablaG()
    consola = str(ast.getConsola())
    print('Consola: ', consola)
    return json.dumps({'consola':consola, 'mensaje': 'Compilado :3'})


@app.route('/errores')
def getErrores():
    global Excepciones
    aux = []
    for x in Excepciones:
        aux.append(x.toString2())
    return {'valores': aux}

@app.route('/simbolos')
def getTabla():
    global Simbolos
    Dic = []
    for x in Simbolos:
        aux = Simbolos[x].getValor()
        tipo = Simbolos[x].getTipo()
        fila = Simbolos[x].getFila()
        colum = Simbolos[x].getColumna()
        if isinstance(aux, List):
            aux = getValores(aux)
            a = []
            a.append(str(x))
            a.append(str(aux))
            a.append('Array')
            a.append('Global')
            a.append(str(fila))
            a.append(str(colum))
            Dic.append(a)
        elif isinstance(aux, Dict):
            aux = getValores2(aux)
            a = []
            a.append(str(x))
            a.append(str(aux))
            a.append('Struct')
            a.append('Global')
            a.append(str(fila))
            a.append(str(colum))
            Dic.append(a)
        else:
            a = []
            a.append(str(x))
            a.append(str(aux))
            a.append(tipo)
            a.append('Global')
            a.append(str(fila))
            a.append(str(colum))
            Dic.append(a)
    return {'valores':Dic}

def getValores(anterior):
    actual = []
    for x in anterior:
        a = x.getValor()
        if isinstance(a, List):
            value = getValores(a)
            actual.append(value)
        elif isinstance(a, Dict):
            value = getValores2(a)
            actual.append(value)
        else:
            actual.append(x.getValor())
    return actual

def getValores2( dict):
    val = "("
    for x in dict:
        a = dict[x].getValor()
        if isinstance(a, List):
            value = getValores(a)
            val += str(value) + ", "
        elif isinstance(a, Dict):
            value = getValores2(a)
            val += str(value) + ", "
        else:
            val += str(dict[x].getValor()) + ", "
    val = val[:-2]  
    val += ")"
    return val


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False, port=5200)