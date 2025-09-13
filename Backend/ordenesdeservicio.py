from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # cambia si tu usuario es distinto
        password="",        # pon tu contraseña si tienes
        database="montallantasfy"
    )

@app.route("/", methods=["GET", "POST"])
def ordenes_servicio():
    if request.method == "POST":
        # Obtener datos del formulario
        modelo = request.form.get("modelo")
        servicio = request.form.get("servicio")
        fecha_hora = request.form.get("fecha_hora")
        responsable = request.form.get("responsable")
        detalles = request.form.get("detalles")
        garantia = request.form.get("garantia")

        # Guardar en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO OrdenesServicio (modelo, servicio, fecha_hora, responsable, detalles, garantia)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (modelo, servicio, fecha_hora, responsable, detalles, garantia))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("ordenes_servicio"))

    # Consultar órdenes desde la base de datos
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM OrdenesServicio ORDER BY fecha_hora DESC")
    ordenes = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("ordenes.html", ordenes=ordenes)

if __name__ == "__main__":
    app.run(debug=True)
