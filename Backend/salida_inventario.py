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
        
    def registrar_venta_multiple(self, cliente_id, encargado_id, garantia_global,
                                descripcion_global, items_de_venta, estado="COMPLETA"):
        try:
            # ---------------- VALIDACIONES ----------------
            if not cliente_id:
                return False, "Falta ID del cliente"

            if garantia_global is None:
                return False, "Falta garantía"

            if not items_de_venta:
                return False, "La venta no tiene ítems"

            self.conexion.autocommit = False
            self.cursor = self.conexion.cursor()

            # ---------------------------------------------------------
            # PASO 0: CALCULAR MONTO TOTAL
            # ---------------------------------------------------------
            monto_total = sum(item['monto_final'] for item in items_de_venta)

            # ---------------------------------------------------------
            # PASO 1: INSERTAR CABECERA (venta)
            # ---------------------------------------------------------
            query_venta = """
                INSERT INTO venta
                (cliente_id, descripcion, fecha_venta, encargado_id, monto, garantias, estado)
                VALUES (%s, %s, NOW(), %s, %s, %s, %s);
            """
            values_venta = (
                cliente_id,
                descripcion_global,
                encargado_id,
                monto_total,
                garantia_global,
                estado
            )

            self.cursor.execute(query_venta, values_venta)
            id_venta = self.cursor.lastrowid

            # ---------------------------------------------------------
            # PASO 2: INSERTAR DETALLEVENTA
            # ---------------------------------------------------------
            query_detalle = """
                INSERT INTO detalleventa
                (venta_id, producto_id, cantidad, precio_unitario, descuento, monto_item)
                VALUES (%s, %s, %s, %s, %s, %s);
            """

            for item in items_de_venta:
                # A. Verificar stock
                producto_bd = self.obtener_producto_por_id_transaccion(item['id_producto'])

                if not producto_bd or producto_bd["cantidad"] < item['cantidad']:
                    self.conexion.rollback()
                    return False, f"Stock insuficiente para producto ID {item['id_producto']}"

                # B. Insertar detalle
                values_detalle = (
                    id_venta,
                    item['id_producto'],
                    item['cantidad'],
                    item['precio_unitario'],
                    item['descuento'],
                    item['monto_final']
                )

                self.cursor.execute(query_detalle, values_detalle)

                # C. Actualizar stock
                nueva_cantidad = producto_bd["cantidad"] - item['cantidad']
                query_update = """
                    UPDATE producto
                    SET cantidad = %s
                    WHERE id_producto = %s;
                """
                self.cursor.execute(query_update, (nueva_cantidad, item['id_producto']))

            # ---------------------------------------------------------
            # PASO 3: CONFIRMAR TRANSACCIÓN
            # ---------------------------------------------------------
            self.conexion.commit()
            return True, "Venta registrada exitosamente"

        except Exception as e:
            if self.conexion:
                self.conexion.rollback()
            print(f"Error en transacción: {e}")
            return False, str(e)

        finally:
            if self.conexion:
                self.conexion.autocommit = True


    def obtener_producto_por_id_transaccion(self, id_producto):
        try:
            query = "SELECT id_producto, cantidad FROM producto WHERE id_producto = %s;"
            self.cursor.execute(query, (id_producto,))
            resultado = self.cursor.fetchone()

            if resultado:
                return {
                    "id_producto": resultado[0],
                    "cantidad": resultado[1]
                }
            return None
        except Exception as e:
            print(f"Error al obtener producto: {e}")
            return None


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

