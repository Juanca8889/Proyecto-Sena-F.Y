import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from BD.bda import conectar


class Material:
    def __init__(self):
        try:
            self.conexion = conectar()
            self.cursor = self.conexion.cursor(dictionary=True)
        except Exception as e:
            print(f"Error al conectar con la base de datos: {e}")
            self.conexion = None
            self.cursor = None


    def consultar_todas_las_categorias(self):
        try:
            self.cursor.callproc("ConsultarTodasLasCategoriasProductos")
            for result in self.cursor.stored_results():
                return result.fetchall()
        except Exception as e:
            print(f"Error al consultar categorías: {e}")
            return []


    def obtener_producto_por_id(self, id_producto):
        try:
            self.cursor.callproc("ConsultarProductoPorId", (id_producto,))
            for result in self.cursor.stored_results():
                return result.fetchone()
        except Exception as e:
            print(f"Error al obtener producto por ID: {e}")
            return None


    def actualizar_producto(self, id_producto, nombre, descripcion, cantidad, categoria_id, precio):
        try:
            self.cursor.callproc("ActualizarProducto", (
                id_producto,
                nombre,
                descripcion,
                cantidad,
                categoria_id,
                precio
            ))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar producto: {e}")
            self.conexion.rollback()
            return False


    def listar_materiales(self):
        try:
            self.cursor.callproc("ConsultarTodosLosProductos")
            for result in self.cursor.stored_results():
                return result.fetchall()
        except Exception as e:
            print(f"Error al listar materiales: {e}")
            return []


    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()
