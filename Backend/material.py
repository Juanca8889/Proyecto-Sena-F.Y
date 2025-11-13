from BD.conexion import conectar
from datetime import datetime
import mysql.connector


class ConexionMaterial:
    def __init__(self, nombre=None, descripcion=None, cantidad=None, categoria_id=None, precio=None):
        self.conexion = conectar()
        self.cursor = self.conexion.cursor(dictionary=True)
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.categoria_id = categoria_id
        self.precio = precio


    def obtener_producto(self, id_producto):
        try:
            query = "SELECT * FROM producto WHERE id_producto = %s;"
            self.cursor.execute(query, (id_producto,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error al obtener producto: {err}")
            return None
        


    def actualizar_material(self, id_producto, nombre_nuevo, descripcion_nueva, precio_nuevo):
        try:
            # 1) Obtener el producto actual
            producto = self.obtener_producto(id_producto)
            if not producto:
                print("❌ Producto no encontrado.")
                return False

            # 2) Preparar consulta de actualización
            query = """
                UPDATE producto
                SET nombre = %s,
                    descripcion = %s,
                    precio = %s
                WHERE id_producto = %s;
            """

            values = (nombre_nuevo, descripcion_nueva, precio_nuevo, id_producto)

            # 3) Ejecutar actualización
            self.cursor.execute(query, values)
            self.conexion.commit()

            print(f"✅ Producto actualizado correctamente: {nombre_nuevo}")
            return True

        except mysql.connector.Error as err:
            print(f"❌ Error al actualizar material: {err}")
            return False
        
        
    def cerrar(self):
        self.cursor.close()
        self.conexion.close()
