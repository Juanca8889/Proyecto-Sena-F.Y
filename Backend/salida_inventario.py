from BD.conexion import conectar
from datetime import datetime
import mysql.connector

class Venta:
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

    def registrar_venta(self, cliente_id, id_producto, cantidad, encargado_id, descripcion, garantia):
        try:
            producto = self.obtener_producto(id_producto)
            
            if not producto:
                print("Producto no encontrado.")
                return False

            precio_unitario = producto["precio"]
            monto = precio_unitario * cantidad
            fecha_actual = datetime.now().date()

            query = """
            
                
                INSERT INTO Venta (cliente_id, cantidad, descripcion, fecha_venta, encargado_id, monto, garantias)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            values = (cliente_id, cantidad, descripcion, fecha_actual, encargado_id, monto, garantia)
            self.cursor.execute(query, values)
            self.conexion.commit()

            nueva_cantidad = producto["cantidad"] - cantidad
            query_update = "UPDATE producto SET cantidad = %s WHERE id_producto = %s;"
            self.cursor.execute(query_update, (nueva_cantidad, id_producto))
            self.conexion.commit()

            print(f"✅ Venta registrada: {producto['nombre']} - Total: {monto} garantia de {garantia} dias")
            
            return True
        except mysql.connector.Error as err:
            print(f"❌ Error al registrar venta: {err}")
            return False
        
    def ver_ventas(self, limit=None, offset=None, filtro='recientes'):
        try:
            # Ordenar según el filtro
            order = "DESC" if filtro == 'recientes' else "ASC"
            query = f"SELECT * FROM venta ORDER BY fecha_venta {order}"
            
            if limit is not None and offset is not None:
                query += " LIMIT %s OFFSET %s"
                self.cursor.execute(query, (limit, offset))
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error al obtener ventas: {err}")
            return []


    def contar_ventas(self):
        try:
            self.cursor.execute("SELECT COUNT(*) AS total FROM venta;")
            return self.cursor.fetchone()["total"]
        except mysql.connector.Error:
            return 0


