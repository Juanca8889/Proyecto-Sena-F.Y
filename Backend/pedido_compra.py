import sys
import os

# Asegura que BD esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'BD')))

from conexion import ConexionCompra  # Importa desde BD/conexion.py

class GestorCompras:
    def __init__(self):
        # Para consultas generales, instancia sin datos de compra
        self.conexion_bd = ConexionCompra(
            id_proveedor=None,
            id_producto=None,
            descripcion=None,
            cantidad=None
        )
        if not self.conexion_bd.conexion:
            print("No se pudo conectar a la base de datos. Saliendo del programa.")
            exit()

    def sugerir_pedido_y_alertar(self):
        try:
            self.conexion_bd.cursor.execute("SELECT id_producto, nombre, cantidad FROM producto")
            productos = self.conexion_bd.cursor.fetchall()

            sugerencias = []
            for producto in productos:
                if producto[2] <= 30:
                    cantidad_sugerida = 50 - producto[2]
                    sugerencias.append({
                        'id_producto': producto[0],
                        'nombre': producto[1],
                        'cantidad_sugerida': cantidad_sugerida
                    })
            return sugerencias

        except Exception as err:
            print(f"Error al obtener los datos de stock: {err}")
            return []

    def realizar_pedido(self, id_proveedor, id_producto, descripcion, cantidad, fecha_entrega):
        compra_nueva = ConexionCompra(id_proveedor, id_producto, descripcion, cantidad)
        if compra_nueva.conexion:
            compra_nueva.insertar_compra(fecha_entrega)
        compra_nueva.cerrar()

    def cerrar(self):
        self.conexion_bd.cerrar()
        print("Conexión a la base de datos cerrada.")
