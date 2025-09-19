import sys
import os
from flask import Flask, render_template, request, redirect, url_for, flash

# Ajustamos el path para que encuentre la carpeta BD
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Importamos Database desde BD/conexion.py
from BD.conexion import conectar 

# Conexión a la BD
db = conectar(host="localhost", user="root", password="", database="inventario")

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "clave_secreta"

# Página principal
@app.route("/inventario_herramientas/")
def inventario():
    herramientas = db.get_herramientas()
    return render_template("inventario_herramientas.html", herramientas=herramientas)

# Registrar herramienta
@app.route("/registrar_herramienta", methods=["POST"])
def registrar_herramienta():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    codigo = request.form["codigo"]
    cantidad = request.form["cantidad"]

    ok, msg = db.registrar_herramienta(nombre, descripcion, codigo, cantidad)
    flash(msg, "success" if ok else "error")

    return redirect(url_for("inventario"))

# Retirar herramienta
@app.route("/retiro", methods=["POST"])
def retiro():
    codigo = request.form["codigo"]
    cantidad = int(request.form["cantidad"])
    usuario = request.form["usuario"]
    fecha = request.form["fecha"]

    ok, msg = db.retirar_herramienta(codigo, cantidad, usuario, fecha)
    flash(msg, "success" if ok else "error")
    return redirect(url_for("inventario"))

# Reintegrar herramienta
@app.route("/reintegro", methods=["POST"])
def reintegro():
    codigo = request.form["codigo"]
    cantidad = int(request.form["cantidad"])
    usuario = request.form["usuario"]

    ok, msg = db.reintegrar_herramienta(codigo, cantidad, usuario)
    flash(msg, "success" if ok else "error")
    return redirect(url_for("inventario"))

# Salida inventario
@app.route("/salida_inventario")
def salida_inventario():
    salidas = db.get_salidas()  # asegúrate de definirlo en Database
    return render_template("salida_inventario.html", salidas=salidas)

@app.route("/registrar_salida", methods=["POST"])
def registrar_salida():
    fecha = request.form["fecha"]
    codigo = request.form["codigo"]
    nombre = request.form["nombre"]
    cantidad = request.form["cantidad"]
    motivo = request.form["motivo"]
    responsable = request.form["responsable"]

    ok, msg = db.registrar_salida(fecha, codigo, nombre, cantidad, motivo, responsable)
    flash(msg, "success" if ok else "error")

    return redirect(url_for("salida_inventario"))

if __name__ == "__main__":
    app.run(debug=True)
