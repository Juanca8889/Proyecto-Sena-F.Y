
from BD.conexion import conectar

class Database:
    def __init__(self, host="localhost", user="root", password="", database="inventario"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conectar = conectar()


    # Obtener todas las herramientas
    def get_herramientas(self):
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM herramientas")
        herramientas = cursor.fetchall()
        cursor.close()
        conn.close()
        return herramientas

    # Registrar una herramienta
    def registrar_herramienta(self, nombre, descripcion, codigo, cantidad):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO herramientas (nombre, descripcion, codigo, cantidad, estado, fechaIngreso) "
                "VALUES (%s, %s, %s, %s, %s, NOW())",
                (nombre, descripcion, codigo, cantidad, "Nuevo")
            )
            conn.commit()
            return True, "Herramienta registrada con éxito"
        except Exception as e:
            return False, "Error: ya existe una herramienta con ese código"
        finally:
            cursor.close()
            conn.close()

    # Retirar una herramienta
    def retirar_herramienta(self, codigo, cantidad, usuario, fecha):
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM herramientas WHERE codigo = %s", (codigo,))
        herramienta = cursor.fetchone()

        if herramienta:
            if cantidad <= herramienta["cantidad"]:
                nueva_cantidad = herramienta["cantidad"] - cantidad
                estado = "En uso" if nueva_cantidad > 0 else "Dañado"
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE herramientas SET cantidad=%s, estado=%s, fechaSalida=%s WHERE codigo=%s",
                    (nueva_cantidad, estado, fecha, codigo)
                )
                conn.commit()
                cursor.close()
                conn.close()
                return True, f"Retiro realizado por {usuario}"
            else:
                cursor.close()
                conn.close()
                return False, "Cantidad insuficiente"
        else:
            cursor.close()
            conn.close()
            return False, "Herramienta no encontrada"

    # Reintegrar herramienta
    def reintegrar_herramienta(self, codigo, cantidad, usuario):
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM herramientas WHERE codigo = %s", (codigo,))
        herramienta = cursor.fetchone()

        if herramienta:
            nueva_cantidad = herramienta["cantidad"] + cantidad
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE herramientas SET cantidad=%s, estado=%s, fechaSalida=NULL WHERE codigo=%s",
                (nueva_cantidad, "Disponible", codigo)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True, f"Reintegro realizado por {usuario}"
        else:
            cursor.close()
            conn.close()
            return False, "Herramienta no encontrada"