from BD.conexion import conectar
from datetime import datetime
import mysql.connector

class Agenda:
    def __init__(self):
        self.conexion = conectar()
        self.cursor = self.conexion.cursor(dictionary=True)

    def cerrar(self):
        self.cursor.close()
        self.conexion.close()

    # 🔹 Ver mantenimientos
    def ver_mantenimientos(self):
        try:
            query = "SELECT * FROM mantenimiento;"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"❌ Error al obtener mantenimientos: {err}")
            return []

    # 🔹 Buscar máquina por ID (tabla: maquinaria)
    def obtener_maquina(self, id_maquina):
        try:
            query = "SELECT * FROM maquinaria WHERE id_maquina = %s;"
            self.cursor.execute(query, (id_maquina,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"❌ Error al obtener máquina: {err}")
            return None

    # 🔹 Registrar mantenimiento
    def registrar_mantenimiento(self, descripcion, personal, dia, maquina_id, usuario_id, costo):
        try:
            # Generar fecha con el día seleccionado + mes/año actual
            fecha = datetime.now().replace(day=int(dia)).date()

            query = """
                INSERT INTO mantenimiento (descripcion, fecha, personal, maquina_id, usuario_id, costo)
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            values = (descripcion, fecha, personal, maquina_id, usuario_id, costo)
            self.cursor.execute(query, values)
            self.conexion.commit()

            print(f"✅ Mantenimiento registrado para la máquina {maquina_id} el {fecha}")
            return True
        except mysql.connector.Error as err:
            print(f"❌ Error al registrar mantenimiento: {err}")
            return False
