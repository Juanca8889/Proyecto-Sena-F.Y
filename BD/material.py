import mysql.connector

class ConexionMaterial:
    def __init__(self, nombre, descripcion, cantidad, categoria_id, precio):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            database="montallantasfy",
            charset="utf8mb4"
        )
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.categoria_id = categoria_id
        self.precio = precio
        self.cursor = self.conexion.cursor()

    def actualizar_material(self, id, new_nombre, new_cantidad,  new_precio):
        query = "UPDATE Producto SET nombre = %s, cantidad = %s, precio = %s WHERE id = %s"
        values = (new_nombre, new_cantidad, new_precio, id)
        self.cursor.execute(query, values)
        self.conexion.commit()
        


