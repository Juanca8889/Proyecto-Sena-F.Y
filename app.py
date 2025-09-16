from flask import Flask, render_template, request, redirect, url_for, flash
from BD.conexion import conectar
from datetime import date

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Ruta principal: mostrar referencias
@app.route("/referencias")
def referencias():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM referencias ORDER BY nombre ASC")
    referencias = cursor.fetchall()
    conn.close()

    return render_template("referencias.html", referencias=referencias, fecha_actual=date.today())

# Ruta para registrar un producto nuevo
@app.route("/referencias/crear", methods=["POST"])
def crear_referencia():
    nombre = request.form["nombre"]
    cantidad = request.form["cantidad"]
    codigo = request.form["codigo"]
    fecha = request.form["fecha"]

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO referencias (nombre, cantidad, codigo, fecha) VALUES (%s, %s, %s, %s)",
        (nombre, cantidad, codigo, fecha)
    )
    conn.commit()
    conn.close()

    flash(f"Se han registrado {cantidad} unidades de '{nombre}' en el inventario.")
    return redirect(url_for("referencias"))

if __name__ == "__main__":
    app.run(debug=True)



from flask import Flask, render_template, request, redirect, url_for
from BD.conexion import conectar

app = Flask(__name__)

# -----------------------
# RUTA: REPORTE DE VENTAS
# -----------------------
@app.route("/reporte_ventas", methods=["GET"])
def reporte_ventas():
    fecha = request.args.get("fecha")
    orden = request.args.get("orden")

    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    # Consulta base: solo transacciones completadas y sin duplicados
    query = """
        SELECT DISTINCT id_venta, cantidad, producto, servicio, fecha, hora, responsable, descripcion
        FROM ventas
        WHERE estado = 'completada'
    """
    valores = []

    # Si hay filtro por fecha
    if fecha:
        query += " AND fecha = %s"
        valores.append(fecha)

    # Ordenar según filtro
    if orden == "recientes":
        query += " ORDER BY fecha DESC, hora DESC"
    elif orden == "antiguos":
        query += " ORDER BY fecha ASC, hora ASC"

    cursor.execute(query, valores)
    ventas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("reporte_ventas.html", ventas=ventas)

# -----------------------
# EXPORTAR A EXCEL (ejemplo simple)
# -----------------------
@app.route("/exportar_excel")
def exportar_excel():
    return "Aquí implementas exportación a Excel"

# -----------------------
# EXPORTAR A CSV (ejemplo simple)
# -----------------------
@app.route("/exportar_csv")
def exportar_csv():
    return "Aquí implementas exportación a CSV"

# -----------------------
# LOGOUT
# -----------------------
@app.route("/logout")
def logout():
    return redirect(url_for("reporte_ventas"))


if __name__ == "__main__":
    app.run(debug=True)



from flask import Flask, render_template
import mysql.connector
from BD.conexion import conectar

app = Flask(__name__)

@app.route("/detalle_compra")
def detalle_compra():
    # Conexión a la BD
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    # Consulta de pedidos (ejemplo)
    cursor.execute("""
        SELECT id_pedido, producto, descripcion, cantidad, monto, estado, fecha
        FROM pedidos
        ORDER BY fecha DESC
    """)
    pedidos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("detalle_compra.html", pedidos=pedidos)

if __name__ == "__main__":
    app.run(debug=True)



from flask import Flask, render_template
import mysql.connector
from BD.conexion import conectar

app = Flask(__name__)

@app.route("/detalle_compra")
def detalle_compra():
    # Conexión a la BD
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    # Consulta de pedidos (ejemplo)
    cursor.execute("""
        SELECT id_pedido, producto, descripcion, cantidad, monto, estado, fecha
        FROM pedidos
        ORDER BY fecha DESC
    """)
    pedidos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("detalle_compra.html", pedidos=pedidos)

if __name__ == "__main__":
    app.run(debug=True)

