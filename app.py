from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# -----------------------------------------
# Conexión a la base de datos
# -----------------------------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # cambia por tu usuario
        password="",        # cambia por tu contraseña
        database="montallantasfy"
    )

# -----------------------------------------
# REGISTRAR MATERIALES
# -----------------------------------------
@app.route("/registrarmat", methods=["GET", "POST"])
def registrarmat():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.form.get("nombre")
        codigo = request.form.get("codigo")
        tipo = request.form.get("tipo")
        fecha = request.form.get("fecha")
        descripcion = request.form.get("descripcion")
        cantidad = request.form.get("cantidad")
        precio = request.form.get("precio")

        cursor.execute("""
            INSERT INTO InventarioProductos 
            (producto_id, nombre, categoria_id, descripcion, fecha, cantidad, precio, rol_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (codigo, nombre, tipo, descripcion, fecha, cantidad, precio, None))
        conn.commit()

    cursor.execute("SELECT * FROM InventarioProductos ORDER BY id_inve_produ DESC")
    historial = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("registrarmat.html", historial=historial)


# -----------------------------------------
# ÓRDENES DE SERVICIO
# -----------------------------------------
@app.route("/ordenes", methods=["GET", "POST"])
def ordenes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        modelo = request.form["modelo"]
        servicio = request.form["servicio"]
        fecha_hora = request.form["fecha_hora"]
        responsable = request.form["responsable"]
        detalles = request.form["detalles"]
        garantia = request.form["garantia"]

        cursor.execute("""
            INSERT INTO OrdenServicio (modelo, servicio, fecha_hora, responsable, detalles, garantia)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (modelo, servicio, fecha_hora, responsable, detalles, garantia))
        conn.commit()

    cursor.execute("SELECT * FROM OrdenServicio ORDER BY id_orden DESC")
    ordenes = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("ordenes.html", ordenes=ordenes)


# -----------------------------------------
# FILTRO DE PRODUCTOS
# -----------------------------------------
@app.route("/filtro", methods=["GET", "POST"])
def filtro():
    materiales = []
    if request.method == "POST":
        criterio = request.form.get("criterio")
        valor = request.form.get("valor")
        busqueda = BusquedaInventario()
        materiales = busqueda.buscar(**{criterio: valor})
        busqueda.cerrar()
    else:
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Producto")
        materiales = cursor.fetchall()
        cursor.close()
        conexion.close()

    return render_template("filtro.html", materiales=materiales)


# -----------------------------------------
# CREAR PRODUCTO
# -----------------------------------------
@app.route("/crear", methods=["POST"])
def crear():
    codigo = request.form["codigo"]
    nombre = request.form["nombre"]
    tipo = request.form["tipo"]
    precio = request.form["precio"]
    proveedor = request.form["proveedor"]
    estado = request.form["estado"]

    conexion = get_db_connection()
    cursor = conexion.cursor()

    query = """
        INSERT INTO Producto (codigo, nombre, tipo, precio, proveedor, estado)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (codigo, nombre, tipo, precio, proveedor, estado)
    cursor.execute(query, valores)

    conexion.commit()
    cursor.close()
    conexion.close()

    return redirect(url_for("filtro"))


# -----------------------------------------
# CLASE DE BÚSQUEDA
# -----------------------------------------
class BusquedaInventario:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor(dictionary=True)

    def buscar(self, **criterios):
        query = "SELECT * FROM Producto WHERE 1=1"
        valores = []
        for campo, valor in criterios.items():
            query += f" AND {campo} LIKE %s"
            valores.append(f"%{valor}%")
        self.cursor.execute(query, valores)
        resultados = self.cursor.fetchall()
        return resultados

    def cerrar(self):
        self.cursor.close()
        self.conexion.close()


# -----------------------------------------
# ERRORES
# -----------------------------------------
@app.errorhandler(404)
def pagina_no_encontrada(error):
    return "Página no encontrada. Verifica la URL.", 404


# -----------------------------------------
# MAIN
# -----------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
