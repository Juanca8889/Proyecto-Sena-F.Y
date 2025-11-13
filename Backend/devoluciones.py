import sys
import os
from datetime import date

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from BD.conexion import conectar


class Devolucion:
    def __init__(self, id_devolucion=None, compra_id=None, fecha=None, estado=None, razon=None):
        self.id_devolucion = id_devolucion
        self.compra_id = compra_id
        self.fecha = fecha
        self.estado = estado
        self.razon = razon

        try:
            self.conexion = conectar()
            self.cursor = self.conexion.cursor(dictionary=True)
        except Exception as e:
            print(f"Error al conectar a la BD: {e}")
            self.conexion = None
            self.cursor = None

   
   
    def registrar_devolucion(self):
        conexion = conectar()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO devoluciones (compra_id, razon, estado, fecha)
        VALUES (%s, %s, %s, %s)
        """
        valores = (self.compra_id, self.razon, self.estado, self.fecha)

        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()
        conexion.close()

    def listar_devoluciones(self):
        if not self.cursor:
            return []
        try:
            self.cursor.callproc("ConsultarDevoluciones")
            resultados = []
            for result in self.cursor.stored_results():
                resultados.extend(result.fetchall())
            return resultados
        except Exception as e:
            print(f"Error al obtener devoluciones: {e}")
            return []

    def obtener_por_id(self):
        if not self.cursor or not self.id_devolucion:
            return None
        try:
            self.cursor.callproc("ConsultarDevolucionPorId", (self.id_devolucion,))
            for result in self.cursor.stored_results():
                return result.fetchone()
        except Exception as e:
            print(f"Error al consultar devolución por ID: {e}")
            return None

    def actualizar_devolucion(self):
        if not self.cursor:
            return False
        try:
            self.cursor.callproc("ActualizarDevolucion", (
                self.id_devolucion,
                self.compra_id,
                self.fecha,
                self.estado,
                self.razon
            ))
            self.conexion.commit()
            print("Devolución actualizada correctamente.")
            return True
        except Exception as e:
            print(f"Error al actualizar devolución: {e}")
            self.conexion.rollback()
            return False

    def eliminar_devolucion(self):
        if not self.cursor or not self.id_devolucion:
            return False
        try:
            self.cursor.callproc("EliminarDevolucion", (self.id_devolucion,))
            self.conexion.commit()
            print("Devolución eliminada correctamente.")
            return True
        except Exception as e:
            print(f"Error al eliminar devolución: {e}")
            self.conexion.rollback()
            return False

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()

    def p(self):
        if not self.cursor:
            return False
        try:
            self.cursor.callproc("InsertarDevolucion", (
                self.compra_id,
                self.fecha,
                self.estado,
                self.razon
            ))
            self.conexion.commit()
            print("Devolución registrada correctamente (p).")
            return True
        except Exception as e:
            print(f"Error al registrar devolución (p): {e}")
            self.conexion.rollback()
            return False