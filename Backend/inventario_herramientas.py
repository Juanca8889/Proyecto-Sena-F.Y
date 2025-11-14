from BD.conexion import conectar
import mysql.connector

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
        herramientas = self.cursor.fetchall()
        return herramientas

    def buscar_herramienta(self, nombre):
        query = "SELECT * FROM inventarioherramientas WHERE nombre LIKE %s"
        self.cursor.execute(query, ('%' + nombre + '%',))
        herramienta = self.cursor.fetchall()
        return herramienta

    def salida(self, id_herr, cantidad_salida):
        try:

            query_select = "SELECT cantidad FROM inventarioherramientas WHERE id_herr = %s;"
            self.cursor.execute(query_select, (id_herr,))
            result = self.cursor.fetchone()
            
            if result:
                cantidad_actual = result["cantidad"]
                if cantidad_actual >= cantidad_salida:
                    nueva_cantidad = cantidad_actual - cantidad_salida
                    query_update = "UPDATE inventarioherramientas SET cantidad_faltante = %s WHERE id_herr = %s;"
                    self.cursor.execute(query_update, (nueva_cantidad, id_herr))
                    self.conexion.commit()
                    return True
                else:
                    print("❌ No hay suficiente cantidad disponible para salida.")
                    return False
            else:
                print("❌ Herramienta no encontrada.")
                return False
        except mysql.connector.Error as err:
            print(f"⚠️ Error al registrar salida: {err}")
            return False


    def reintegro(self, id_herr, cantidad_reintegro):
        try:
            query_select = "SELECT cantidad_faltante FROM inventarioherramientas WHERE id_herr = %s;"
            self.cursor.execute(query_select, (id_herr,))
            result = self.cursor.fetchone()

            if result:
                cantidad_actual = result["cantidad_faltante"]
                nueva_cantidad = cantidad_actual - cantidad_reintegro
                query_update = "UPDATE inventarioherramientas SET cantidad_faltante = %s WHERE id_herr = %s;"
                self.cursor.execute(query_update, (nueva_cantidad, id_herr))
                self.conexion.commit()
                return True
            else:
                print("Herramienta no encontrada.")
                return False
        except mysql.connector.Error as err:
            print(f"Error al reintegrar herramienta: {err}")
            return False


    def eliminar_herramienta(self, id_herr):
        try:
            query = "DELETE FROM inventarioherramientas WHERE id_herr = %s;"
            self.cursor.execute(query, (id_herr,))
            self.conexion.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error al eliminar herramienta: {err}")
            return False

    def cerrar(self):
        self.cursor.close()
        self.conexion.close()