from BD.conexion import conectar
from datetime import datetime
import mysql.connector

class Guardar_material:
    def __init__(self):
        self.conexion = conectar()
        self.cursor = self.conexion.cursor(dictionary=True)

    def cerrar(self):
        self.cursor.close()
        self.conexion.close()
        

    def obtener_producto(self, id_producto):
        try:
            query = "SELECT * FROM producto WHERE id_producto = %s;"
            self.cursor.execute(query, (id_producto,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error al obtener producto: {err}")
            return None
        
        
    def sumar_cantidad(self, id_producto, cantidad_extra):
        try:
            query = """
                UPDATE producto
                SET cantidad = cantidad + %s
                WHERE id_producto = %s
            """
            self.cursor.execute(query, (cantidad_extra, id_producto))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar producto: {e}")
            return False
        
    