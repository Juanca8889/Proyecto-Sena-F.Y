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

    def obtener_precio_producto(self, id_producto):
        try:
            query = "SELECT precio FROM producto WHERE id_producto = %s;"
            self.cursor.execute(query, (id_producto,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error al obtener producto: {err}")
            return None
    
    def obtener_producto(self, id_producto):
        try:
            query = "SELECT * FROM producto WHERE id_producto = %s;"
            self.cursor.execute(query, (id_producto,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error al obtener producto: {err}")
            return None

    def registrar_venta(self, cliente_id, id_producto, cantidad, encargado_id, descripcion, garantia, descuento):
        try:
            producto = self.obtener_producto(id_producto)
            
            if not producto:
                print("Producto no encontrado.")
                return False

            precio_unitario = producto["precio"]
            fecha_actual = datetime.now().date()

            # Calcular subtotal sin descuento
            subtotal = precio_unitario * cantidad

            # Aplicar descuento al Monto (NO al inventario)
            if descuento and descuento > 0:
                monto_descuento = subtotal * (descuento / 100)
                monto_final = subtotal - monto_descuento
            else:
                monto_final = subtotal

            # Registrar la venta con el monto final ya descontado
            query = """
                INSERT INTO Venta (cliente_id, cantidad, descripcion, fecha_venta, encargado_id, monto, garantias)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            values = (cliente_id, cantidad, descripcion, fecha_actual, encargado_id, monto_final, garantia)
            self.cursor.execute(query, values)
            self.conexion.commit()

            # Actualizar inventario (solo resta cantidad vendida)
            nueva_cantidad = producto["cantidad"] - cantidad

            query_update = "UPDATE producto SET cantidad = %s WHERE id_producto = %s;"
            self.cursor.execute(query_update, (nueva_cantidad, id_producto))
            self.conexion.commit()

            print(f"✅ Venta registrada | Total: {monto_final} | Descuento aplicado: {descuento}%")
            return True

        except mysql.connector.Error as err:
            print(f"❌ Error al registrar venta: {err}")
            return False

    def obtener_venta_detallada(self, id_venta):
        try:
            query = """
                SELECT v.*, p.precio, p.cantidad AS cantidad_inventario, p.id_producto
                FROM venta v
                JOIN producto p ON v.id_producto = p.id_producto
                WHERE v.id_venta = %s
            """
            self.cursor.execute(query, (id_venta,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error al obtener detalles de venta: {err}")
            return None
        
    def actualizar_venta(self, id_venta, cliente_id, nueva_cantidad, nueva_garantia):
        try:
            # 1. Obtener la venta original
            venta_actual = self.obtener_venta(id_venta)
            if not venta_actual:
                print("❌ Venta no encontrada.")
                return False

            cantidad_original = venta_actual["cantidad"]
            monto_original = venta_actual["monto"]

            # 2. Calcular precio unitario
            if cantidad_original > 0:
                precio_unitario = monto_original / cantidad_original
            else:
                print("❌ Error: cantidad original es 0, no se puede dividir.")
                return False

            # 3. Recalcular monto si cambia la cantidad
            nuevo_monto = precio_unitario * nueva_cantidad

            # 4. Guardar cambios
            query = """
                UPDATE venta
                SET cliente_id = %s,
                    cantidad = %s,
                    garantias = %s,
                    monto = %s
                WHERE id_venta = %s
            """

            values = (cliente_id, nueva_cantidad, nueva_garantia, nuevo_monto, id_venta)

            self.cursor.execute(query, values)
            self.conexion.commit()

            print("✅ Venta actualizada correctamente (monto recalculado).")
            return True

        except mysql.connector.Error as err:
            print("❌ Error:", err)
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

    def obtener_venta_por_id(self, id_venta):
        try:
            query = "SELECT * FROM venta WHERE id_venta = %s LIMIT 1;"
            self.cursor.execute(query, (id_venta,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error al obtener venta: {err}")
            return None

    def obtener_venta(self, id_venta):
        try:
            query = "SELECT * FROM venta WHERE id_venta = %s LIMIT 1;"
            self.cursor.execute(query, (id_venta,))
            return self.cursor.fetchone()
        except:
            return None


        
    def actualizar_venta(self, id_venta, cliente_id, cantidad, garantia, monto_nuevo):
        try:
            query = """
                UPDATE venta
                SET cliente_id = %s,
                    cantidad = %s,
                    garantias = %s,
                    monto = %s
                WHERE id_venta = %s;
            """
            self.cursor.execute(query, (cliente_id, cantidad, garantia, monto_nuevo, id_venta))
            self.conexion.commit()
            return True

        except mysql.connector.Error as err:
            print("❌ Error al actualizar:", err)
            return False





    def contar_ventas(self):
        try:
            self.cursor.execute("SELECT COUNT(*) AS total FROM venta;")
            return self.cursor.fetchone()["total"]
        except mysql.connector.Error:
            return 0


