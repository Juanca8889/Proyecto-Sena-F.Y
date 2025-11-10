import sys      
import os       
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from BD.bda import conectar


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
            print(f"Error al conectar a la base de datos: {e}")
            self.conexion = None
            self.cursor = None


    def listar_devoluciones(self):
        if not self.cursor:
            return []
        try:
            self.cursor.callproc("ConsultarDevoluciones")
            for result in self.cursor.stored_results():
                return result.fetchall()
        except Exception as e:
            print(f"Error al listar devoluciones: {e}")
            return []


    def obtener_por_id(self, id_devolucion):
        if not self.cursor:
            return None
        try:
            self.cursor.callproc("ConsultarDevolucionPorId", (id_devolucion,))
            for result in self.cursor.stored_results():
                return result.fetchone()
        except Exception as e:
            print(f"Error al obtener devolución por ID: {e}")
            return None


    def registrar_devolucion(self):
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
            print(" Devolución registrada correctamente.")
            return True
        except Exception as e:
            print(f"Error al registrar devolución: {e}")
            self.conexion.rollback()
            return False


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


    def eliminar_devolucion(self, id_devolucion):
        if not self.cursor:
            return False
        try:
            self.cursor.callproc("EliminarDevolucion", (id_devolucion,))
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
