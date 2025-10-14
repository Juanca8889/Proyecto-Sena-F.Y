from BD.conexion import conectar 


class SalidaInventario:
    def __init__(self, cliente_id=None, cantidad=None, descripcion=None, fecha_venta=None, encargado_id=None, monto=None, id_venta=None):
        self.id_venta = id_venta
        self.cliente_id = cliente_id
        self.cantidad = cantidad
        self.descripcion = descripcion
        self.fecha_venta = fecha_venta
        self.encargado_id = encargado_id
        self.monto = monto

    # ---- Registrar una nueva salida ----
    def registrar(self):
        conn = conectar()
        cursor = conn.cursor()

        sql = """
        INSERT INTO salida_inventario (cliente_id, cantidad, descripcion, fecha_venta, encargado_id, monto)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (self.cliente_id, self.cantidad, self.descripcion, self.fecha_venta, self.encargado_id, self.monto)
        cursor.execute(sql, valores)
        conn.commit()

        self.id_venta = cursor.lastrowid  # obtener el ID generado automáticamente
        cursor.close()
        conn.close()
        return self.id_venta

    # ---- Listar todas las salidas ----
    def listar_todas(self):
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM salida_inventario")
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    # ---- Buscar una salida por ID ----
    def buscar_por_id(self, id_venta):
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM salida_inventario WHERE id_venta = %s", (id_venta,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado

    # ---- Actualizar una salida existente ----
    def actualizar(self):
        if not self.id_venta:
            raise ValueError("Debe establecer un ID de venta para actualizar el registro.")
        
        conn = conectar()
        cursor = conn.cursor()
        sql = """
        UPDATE salida_inventario
        SET cliente_id=%s, cantidad=%s, descripcion=%s, fecha_venta=%s, encargado_id=%s, monto=%s
        WHERE id_venta=%s
        """
        valores = (self.cliente_id, self.cantidad, self.descripcion, self.fecha_venta,
                   self.encargado_id, self.monto, self.id_venta)
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
        return True

    # ---- Eliminar una salida ----
    def eliminar(self, id_venta):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM salida_inventario WHERE id_venta = %s", (id_venta,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
