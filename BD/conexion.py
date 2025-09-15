# ==========================================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================================
import mysql.connector  # Librería oficial de MySQL para conectarse desde Python
from datetime import datetime


# ==========================================
# FUNCIÓN DE CONEXIÓN GENERAL
# ==========================================
def conectar():
    """
    Crea y devuelve una conexión a la base de datos MySQL.
    """
    return mysql.connector.connect(
        host="localhost",          # Dirección del servidor MySQL (local)
        user="root",               # Usuario de MySQL
        password="",               # Contraseña del usuario (vacía por defecto en tu caso)
        database="montallantasfy", # Nombre de la base de datos
        charset="utf8mb4"          # Codificación recomendada para acentos y caracteres especiales
    )


# ==========================================
# CLASE: MANEJO DE COMPRAS
# ==========================================
class ConexionCompra:
    """
    Clase que maneja las operaciones de la tabla 'compra'.
    """

    def __init__(self, id_proveedor=None, id_producto=None, descripcion=None, cantidad=None):
        self.id_proveedor = id_proveedor
        self.id_producto = id_producto
        self.descripcion = descripcion
        self.cantidad = cantidad

        try:
            self.conexion = conectar()
            self.cursor = self.conexion.cursor()
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.conexion = None
            self.cursor = None

    def insertar_compra(self, fecha_entrega):
        """
        Inserta una compra en la tabla y actualiza el stock del producto.
        """
        if not self.cursor:
            print("No hay conexión a la BD.")
            return False

        try:
            # Insertar en la tabla compra
            self.cursor.execute("""
                INSERT INTO compra (proveedor_id, producto_id, descripcion, cantidad, fecha_pedido, fecha_entrega)
                VALUES (%s, %s, %s, %s, CURDATE(), %s)
            """, (self.id_proveedor, self.id_producto, self.descripcion, self.cantidad, fecha_entrega))

            # Actualizar el stock en la tabla producto
            self.cursor.execute("""
                UPDATE producto
                SET cantidad = cantidad + %s
                WHERE id_producto = %s
            """, (self.cantidad, self.id_producto))

            # Guardar cambios
            self.conexion.commit()
            print("Compra insertada y stock actualizado.")
            return True

        except Exception as e:
            print(f"Error al insertar compra o actualizar stock: {e}")
            self.conexion.rollback()
            return False

    def cerrar(self):
        """
        Cierra la conexión a la base de datos.
        """
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()
        print("Conexión a la base de datos cerrada.")


