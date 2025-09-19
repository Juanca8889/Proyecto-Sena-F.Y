# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from backend import Database

app = Flask(__name__)
app.secret_key = "clave_secreta"

db = Database(host="localhost", user="root", password="", database="inventario")

# Página principal
@app.route("/inventario_herramientas/")
def inventario():
    herramientas = db.get_herramientas()
    return render_template("Index.html", herramientas=herramientas)

# Registrar herramienta
@app.route("/registrar", methods=["POST"])
def registrar():
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

if __name__ == "__main__":
    app.run(debug=True)
