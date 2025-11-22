import sys
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from BD.conexion import conectar

class Historial:
    def __init__(self, id_historial=None, tabla=None, operacion=None,
                 registro_id=None, old_data=None, new_data=None, fecha=None):
        
        self.id_historial = id_historial
        self.tabla = tabla
        self.operacion = operacion
        self.registro_id = registro_id
        self.old_data = old_data
        self.new_data = new_data
        self.fecha = fecha

        try:
            self.conexion = conectar()
            self.cursor = self.conexion.cursor(dictionary=True)
        except Exception as e:
            print(f"Error al conectar a la BD: {e}")
            self.conexion = None
            self.cursor = None

    def listar_historial(self):
        """Devuelve todos los registros del historial"""
        if not self.cursor:
            return []

        try:
            self.cursor.execute("SELECT * FROM historial ORDER BY fecha DESC")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener historial: {e}")
            return []
        
    @staticmethod
    def traducir_operacion(op):
        if op == "INSERT":
            return "Ingreso"
        if op == "UPDATE":
            return "Actualización"
        if op == "DELETE":
            return "Eliminación"
        return op

    def cerrar(self):
        if self.cursor: self.cursor.close()
        if self.conexion: self.conexion.close()
