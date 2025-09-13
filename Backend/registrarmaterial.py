from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# 🔹 Conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # cambia por tu usuario
        password="",        # cambia por tu contraseña
        database="montallantasfy"
    )

@app.route("/")
def registrar():
    """
    Página principal: muestra el formulario y el historial desde la DB.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM InventarioProductos ORDER BY id_inve_produ DESC")
    historial = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("registrarmat2.html", historial=historial)


@app.route("/agregar", methods=["POST"])
def agregar():
    """
    Procesa el formulario y guarda un nuevo material en la DB.
    """
    nombre = request.form.get("nombre")
    codigo = request.form.get("codigo")
    tipo = request.form.get("tipo")
    fecha = request.form.get("fecha")
    descripcion = request.form.get("descripcion")
    cantidad = request.form.get("cantidad")
    precio = request.form.get("precio")

    conn = get_db_connection()
    cursor = conn.cursor()

    
    cursor.execute("""
        INSERT INTO InventarioProductos (producto_id, cantidad, categoria_id, rol_id)
        VALUES (%s, %s, %s, %s)
    """, (codigo, cantidad, tipo, None))  

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("registrar"))


@app.errorhandler(404)
def pagina_no_encontrada(error):
    """
    Manejo de errores: ruta no encontrada.
    """
    return "Página no encontrada. Verifica la URL.", 404


if __name__ == "__main__":
    app.run(debug=True)
