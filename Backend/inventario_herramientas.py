from BD.conexion import conectar
import mysql.connector , datetime

class Herramientas:
    def __init__(self, id_herr=None, nombre=None, descripcion=None, cantidad=None, estado=None, usuario_id=None):
        self.conexion = conectar()
        self.cursor = self.conexion.cursor(dictionary=True)
        self.id_herr = id_herr
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.estado = estado
        self.usuario_id = usuario_id

    def insertar_herramienta(self):
        try:
            query = """
                INSERT INTO inventarioherramientas (nombre, descripcion, cantidad, estado, usuario_id)
                VALUES (%s, %s, %s, %s, %s);
            """
            values = (self.nombre, self.descripcion, self.cantidad, self.estado, self.usuario_id)
            self.cursor.execute(query, values)
            self.conexion.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error al registrar herramienta: {err}")
            return False

    def mostrar_herramientas(self):
        self.cursor.execute("SELECT * FROM inventarioherramientas")
        return self.cursor.fetchall()

    def buscar_herramienta(self, nombre):
        query = "SELECT * FROM inventarioherramientas WHERE nombre LIKE %s"
        self.cursor.execute(query, ('%' + nombre + '%',))
        return self.cursor.fetchall()
    
    def cantidad_actual(self,id_herr):
        try:
            self.cursor.execute("SELECT cantidad FROM inventarioherramientas WHERE id_herr = %s", (id_herr,))
            fila = self.cursor.fetchone()
            
            cantidad_actual = fila["cantidad"]
            
        except mysql.connector.Error as err:
            print(f"⚠️ Error al registrar salida: {err}")
            return cantidad_actual

    def salida(self, id_herr, cantidad_salida):
        try:
            self.cursor.execute("SELECT cantidad FROM inventarioherramientas WHERE id_herr = %s", (id_herr,))
            fila = self.cursor.fetchone()

            if not fila:
                print("❌ Herramienta no encontrada.")
                return False

            cantidad_actual = fila["cantidad"]

            if cantidad_salida > cantidad_actual:
                print("❌ No hay suficiente cantidad disponible.")
                return False

            nueva_cantidad = cantidad_actual - cantidad_salida

            query = "UPDATE inventarioherramientas SET cantidad = %s WHERE id_herr = %s"
            self.cursor.execute(query, (nueva_cantidad, id_herr))
            self.conexion.commit()
            
            query = "UPDATE inventarioherramientas SET cantidad_faltante = %s WHERE id_herr = %s"
            self.cursor.execute(query, (cantidad_salida, id_herr))
            self.conexion.commit()
            return True

        except mysql.connector.Error as err:
            print(f"⚠️ Error al registrar salida: {err}")
            return False

    def reintegro(self, id_herr, cantidad_reintegro):
        try:
            self.cursor.execute("SELECT cantidad_faltante FROM inventarioherramientas WHERE id_herr = %s", (id_herr,))
            fila = self.cursor.fetchone()

            if not fila:
                print("❌ Herramienta no encontrada.")
                return False

            faltante_actual = fila["cantidad_faltante"]
            nueva_cantidad = max(faltante_actual - cantidad_reintegro, 0)

            query = "UPDATE inventarioherramientas SET cantidad_faltante = %s WHERE id_herr = %s"
            self.cursor.execute(query, (nueva_cantidad, id_herr))
            self.conexion.commit()
            
            
            self.cursor.execute("SELECT cantidad FROM inventarioherramientas WHERE id_herr = %s", (id_herr,))
            fila = self.cursor.fetchone()
            
            
            cantidad_actualizada = fila["cantidad"]
            
            
            resultado = max(cantidad_actualizada + cantidad_reintegro, 0)
            
            query = "UPDATE inventarioherramientas SET cantidad = %s WHERE id_herr = %s"
            self.cursor.execute(query, (resultado, id_herr))
            self.conexion.commit()
            return True

        except mysql.connector.Error as err:
            print(f"Error al reintegrar herramienta: {err}")
            return False

    def eliminar_herramienta(self, id_herr):
        try:
            query = "DELETE FROM inventarioherramientas WHERE id_herr = %s"
            self.cursor.execute(query, (id_herr,))
            self.conexion.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error al eliminar herramienta: {err}")
            return False

    def historial_control(self):
        query = """
            SELECT ch.*, u.nombre AS usuario
            FROM control_herramienta ch
            INNER JOIN usuario u ON u.id_usuario = ch.usuario_id
            ORDER BY ch.fecha DESC;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def registrar_control(self, usuario_id):
        # Ya no es necesario obtener el 'nombre', solo se usa el 'usuario_id' para el registro.
        print(f"Acá llegó el usuario_id: {usuario_id}")
        
        try:
            # 1. Calcular el Total de Herramientas
            self.cursor.execute("SELECT SUM(cantidad) AS total FROM inventarioherramientas")
            # Manejamos el caso de que el resultado sea None
            total = self.cursor.fetchone()["total"] or 0

            # 2. Calcular la Cantidad Faltante
            self.cursor.execute("SELECT SUM(cantidad_faltante) AS faltante FROM inventarioherramientas")
            # Manejamos el caso de que el resultado sea None
            faltante = self.cursor.fetchone()["faltante"] or 0

            # 3. Preparar la Inserción de Control (usando NOW() y %s)
            query = """
                INSERT INTO Control_Herramienta (usuario_id, fecha, herramienta_total, herramienta_faltante)
                VALUES (%s, NOW(), %s, %s);
            """
            # IMPORTANTE: Pasamos la variable usuario_id como el primer parámetro
            self.cursor.execute(query, (usuario_id, total, faltante))
            self.conexion.commit()
            return True

        except mysql.connector.Error as err:
            print(f"Error al registrar control: {err}")
            return False

    def mostrar_control(self):
        self.cursor.execute("SELECT * FROM Control_Herramienta")
        return self.cursor.fetchall()

    def cerrar(self):
        self.cursor.close()
        self.conexion.close()
