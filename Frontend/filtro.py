from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuración de conexión a MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # cámbialo por tu usuario MySQL
        password="",        # cámbialo por tu contraseña MySQL
        database="montallantasfy"
    )

# Página principal: lista materiales con JOIN
@app.route("/")
def index():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    query = """
        SELECT p.id_producto, p.codigo, p.nombre, p.tipo, p.precio, 
               p.proveedor, p.estado, i.cantidad, c.nombre AS categoria, r.nombre AS rol
        FROM InventarioProductos i
        INNER JOIN Producto p ON i.producto_id = p.id_producto
        INNER JOIN categoriaProductos c ON i.categoria_id = c.id_categoria
        LEFT JOIN Rol r ON i.rol_id = r.id_rol;
    """
    cursor.execute(query)
    materiales = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("filtro2.html", materiales=materiales)

# Crear material
@app.route("/crear", methods=["POST"])
def crear():
    codigo = request.form["codigo"]
    nombre = request.form["nombre"]
    tipo = request.form["tipo"]
    precio = request.form["precio"]
    proveedor = request.form["proveedor"]
    estado = request.form["estado"]
    cantidad = request.form["cantidad"]
    categoria_id = request.form["categoria_id"]
    rol_id = request.form.get("rol_id")  # Puede ser opcional

    conexion = get_connection()
    cursor = conexion.cursor()

    # 1. Insertar en Producto
    query_producto = """
        INSERT INTO Producto (codigo, nombre, tipo, precio, proveedor, estado)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores_producto = (codigo, nombre, tipo, precio, proveedor, estado)
    cursor.execute(query_producto, valores_producto)
    producto_id = cursor.lastrowid  # Recuperamos el id_producto insertado

    # 2. Insertar en InventarioProductos
    query_inventario = """
        INSERT INTO InventarioProductos (producto_id, cantidad, categoria_id, rol_id)
        VALUES (%s, %s, %s, %s)
    """
    valores_inventario = (producto_id, cantidad, categoria_id, rol_id)
    cursor.execute(query_inventario, valores_inventario)

    conexion.commit()
    cursor.close()
    conexion.close()

    return render_template(url_for("filtro2.html"))

if __name__ == "__main__":
    app.run(debug=True)
