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
        
    def ver_ventas(self):
        try:
            query = "SELECT * FROM venta;"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error al obtener ventas: {err}")
            return []

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
        
    def registrar_venta(self, cliente_id, id_producto, cantidad, encargado_id, descripcion, garantia_dias):
        try:
            producto = self.obtener_producto(id_producto)
            if not producto:
                print("Producto no encontrado.")
                return False

            precio_unitario = producto["precio"]
            monto = precio_unitario * cantidad
            fecha_actual = datetime.now().date()

            query = """
                INSERT INTO venta (cliente_id, cantidad, descripcion, fecha_venta, encargado_id, monto)
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            values = (cliente_id, cantidad, descripcion, fecha_actual, encargado_id, monto)
            self.cursor.execute(query, values)
            self.conexion.commit()

            nueva_cantidad = producto["cantidad"] - cantidad
            query_update = "UPDATE producto SET cantidad = %s WHERE id_producto = %s;"
            self.cursor.execute(query_update, (nueva_cantidad, id_producto))
            self.conexion.commit()

            print(f"✅ Venta registrada: {producto['nombre']} - Total: {monto}")
            return True
        except mysql.connector.Error as err:
            print(f"❌ Error al registrar venta: {err}")
            return False
