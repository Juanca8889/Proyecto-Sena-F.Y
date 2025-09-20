from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "clave_secreta"

def get_db_connection():
    conn = sqlite3.connect("inventario.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    salidas = conn.execute("SELECT * FROM salidas ORDER BY fecha DESC").fetchall()
    conn.close()
    return render_template("Index.html", salidas=salidas)

@app.route("/registrar", methods=["POST"])
def registrar():
    fecha = request.form["fecha"]
    codigo = request.form["codigo"]
    nombre = request.form["nombre"]
    cantidad = request.form["cantidad"]
    motivo = request.form["motivo"]
    responsable = request.form["responsable"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO salidas (fecha, codigo, nombre, cantidad, motivo, responsable) VALUES (?, ?, ?, ?, ?, ?)",
        (fecha, codigo, nombre, cantidad, motivo, responsable)
    )
    conn.commit()
    conn.close()

    flash("¡Salida registrada exitosamente!", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
