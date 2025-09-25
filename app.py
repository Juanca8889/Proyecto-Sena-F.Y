from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # cambia por tu usuario
        password="",        # cambia por tu contraseña
        database="montallantasfy"
    )

# Ruta principal
@app.route("/registrarmat")# Busca en templates
def registrarmat():
    return render_template("registrarmat.html")  
@app.route("/registrarmat")
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

    return render_template("registrarmat.html", historial=historial)


@app.route("../templates/registrarmat", methods=["POST"])
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

    return redirect(url_for("../templates/registrarmat"))




















@app.route("/ordenes")
def ordenes():
    return render_template("ordenes.html")
@app.route("/registrarmat")
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

    return render_template("registrarmat.html", historial=historial)


@app.route("../templates/registrarmat", methods=["POST"])
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

    return redirect(url_for("../templates/registrarmat"))


@app.errorhandler(404)
def pagina_no_encontrada(error):
    """
    Manejo de errores: ruta no encontrada.
    """
    return "Página no encontrada. Verifica la URL.", 404















@app.route("/filtro")
def filtro():
    return render_template("filtro.html")
@app.route("/")
def filtrar():
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Producto")  # trae todos los registros
    materiales = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("filtro.html", materiales=materiales)

#Ruta para crear un material
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

    return redirect(url_for("filtrar"))
class BusquedaInventario:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor(dictionary=True)

    def buscar(self, **criterios):
        """
        Permite buscar productos en la tabla Producto filtrando por:
        nombre, codigo, categoria_id, precio, etc.
        """
        query = "SELECT * FROM Producto WHERE 1=1"
        valores = []

        for campo, valor in criterios.items():
            query += f" AND {campo} LIKE %s"
            valores.append(f"%{valor}%")

        self.cursor.execute(query, valores)
        resultados = self.cursor.fetchall()
        return resultados






if __name__ == "__main__":
    app.run(debug=True)
