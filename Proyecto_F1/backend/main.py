# CORS -> Cross Origin Resource Sharing
# Si no existe el CORS, no se puede acceder a los recursos de un servidor desde otro servidor
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
        print(entrada)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False, port=4000)