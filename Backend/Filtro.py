from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # cámbialo si tu usuario es diferente
        password="",       # tu contraseña de MySQL
        database="montallantasfy"
    )

#listar materiales desde la BD
@app.route("/")
def index():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Producto")  # trae todos los registros
    materiales = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("filtro2.html", materiales=materiales)

#Ruta para crear un material
@app.route("/crear", methods=["POST"])
def crear():
    codigo = request.form["codigo"]
    nombre = request.form["nombre"]
    tipo = request.form["tipo"]
    precio = request.form["precio"]
    proveedor = request.form["proveedor"]
    estado = request.form["estado"]

    conexion = get_connection()
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

    return redirect(url_for("index"))
class BusquedaInventario:
    def __init__(self):
        self.conexion = get_connection()
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
