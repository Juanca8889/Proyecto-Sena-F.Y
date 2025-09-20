# ==========================================
# IMPORTACIÓN DE MÓDULOS DEL SISTEMA
# ==========================================

import sys      # Sirve para interactuar con el intérprete de Python y modificar rutas de búsqueda de módulos
import os       # Sirve para trabajar con rutas de archivos y carpetas de forma compatible en Windows, Linux y Mac
import logging  # Se usa para mostrar mensajes en consola (INFO, WARNING, ERROR) en lugar de usar print()


# ==========================================
# CONFIGURACIÓN DE RUTAS
# ==========================================

# Agregamos al "path" de Python la carpeta BD (donde está el archivo conexion.py).
# Así, cuando hagamos "from conexion import ConexionCompra", Python sabrá dónde buscarlo.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Backend')))

# Importamos la clase que maneja la conexión y las operaciones con la base de datos
from BD.conexion import  conectar
from Backend.Compra import ConexionCompra


# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================

# Configuramos logging para que muestre mensajes de información en la consola
logging.basicConfig(level=logging.INFO)

# Constantes que definen el nivel de stock
STOCK_MINIMO = 30    # Si un producto tiene 30 o menos unidades, se considera "bajo"
STOCK_OBJETIVO = 50  # Cuando hay poco stock, sugerimos pedir hasta llegar a 50 unidades


# ==========================================
# CLASE PRINCIPAL: GESTOR DE COMPRAS
# ==========================================
class GestorCompras:
    """
    Clase que contiene toda la lógica de negocio relacionada con compras:
    - Consultar productos, proveedores y pedidos desde la base de datos.
    - Generar sugerencias de pedido cuando el stock es bajo.
    - Insertar pedidos en la base de datos.
    """

    def __init__(self):
        """
        Constructor de la clase.
        Aquí se crea una conexión principal con la base de datos.
        """
        self.conexion_bd = ConexionCompra(None, None, None, None)

        # Si no se puede conectar, mostramos error y salimos del programa
        if not self.conexion_bd.conexion:
            logging.error("No se pudo conectar a la base de datos. Saliendo.")
            exit()

    # ==============================
    # MÉTODOS DE CONSULTA
    # ==============================

    def obtener_productos(self, filtro=None):
        """
        Devuelve la lista de productos, incluyendo cuántos se han vendido.

        Args:
            filtro (str): Permite ordenar la lista. Puede ser:
                          - "MAS VENDIDO"
                          - "MENOR CANTIDAD"
                          - "MAYOR CANTIDAD"

        Returns:
            list[tuple]: Cada producto como tupla con:
                         (id_producto, nombre, descripcion, cantidad, precio, vendidos)
        """
        try:
            # Consulta con JOIN a detalleventa para contar cuántas unidades se han vendido
            query_base = """
            SELECT p.id_producto, p.nombre, p.descripcion, p.cantidad, p.precio,
                   IFNULL(SUM(dv.cantidad), 0) AS vendidos
            FROM producto p
            LEFT JOIN detalleventa dv ON p.id_producto = dv.producto_id
            GROUP BY p.id_producto, p.nombre, p.descripcion, p.cantidad, p.precio
            """

            # Agregamos el orden según el filtro que eligió el usuario
            if filtro == "MENOR CANTIDAD":
                query = query_base + " ORDER BY p.cantidad ASC"
            elif filtro == "MAYOR CANTIDAD":
                query = query_base + " ORDER BY p.cantidad DESC"
            else:  # Por defecto "MAS VENDIDO"
                query = query_base + " ORDER BY vendidos DESC"

            # Ejecutamos la consulta y devolvemos los productos
            self.conexion_bd.cursor.execute(query)
            return self.conexion_bd.cursor.fetchall()

        except Exception as e:
            logging.error(f"Error al obtener productos: {e}")
            return []

    def obtener_proveedores(self):
        """
        Devuelve todos los proveedores registrados en la base de datos.

        Returns:
            list[tuple]: (id_proveedor, nombre)
        """
        try:
            self.conexion_bd.cursor.execute("SELECT id_proveedor, nombre FROM proveedor")
            return self.conexion_bd.cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener proveedores: {e}")
            return []

    def obtener_pedidos(self):
        """
        Devuelve la lista de pedidos ya realizados.

        Returns:
            list[tuple]: Cada pedido con:
                         (id_compra, proveedor_nombre, producto_nombre, descripcion, cantidad, fecha_pedido, fecha_entrega)
        """
        try:
            query = """
            SELECT c.id_compra, p.nombre AS proveedor_nombre, pr.nombre AS producto_nombre, 
                   c.descripcion, c.cantidad, c.fecha_pedido, c.fecha_entrega
            FROM compra c
            JOIN proveedor p ON c.proveedor_id = p.id_proveedor
            JOIN producto pr ON c.producto_id = pr.id_producto
            ORDER BY c.fecha_pedido DESC
            """
            self.conexion_bd.cursor.execute(query)
            return self.conexion_bd.cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener pedidos: {e}")
            return []

    # ==============================
    # MÉTODOS DE NEGOCIO
    # ==============================

    def sugerir_pedido_y_alertar(self):
        """
        Revisa el stock actual de todos los productos.
        Si un producto tiene menos de STOCK_MINIMO,
        sugiere cuántas unidades pedir para llegar a STOCK_OBJETIVO.

        Returns:
            list[dict]: Ejemplo:
                [{'id_producto': 1, 'nombre': 'Martillo', 'cantidad_sugerida': 20}]
        """
        try:
            # Traemos todos los productos con su stock actual
            self.conexion_bd.cursor.execute("SELECT id_producto, nombre, cantidad FROM producto")
            productos = self.conexion_bd.cursor.fetchall()

            sugerencias = []
            for id_producto, nombre, stock_actual in productos:
                if stock_actual <= STOCK_MINIMO:
                    cantidad_sugerida = max(0, STOCK_OBJETIVO - stock_actual)
                    sugerencias.append({
                        "id_producto": id_producto,
                        "nombre": nombre,
                        "cantidad_sugerida": cantidad_sugerida
                    })

            return sugerencias

        except Exception as err:
            logging.error(f"Error al generar sugerencias: {err}")
            return []

    def realizar_pedido(self, id_proveedor, id_producto, descripcion, cantidad, fecha_entrega):
        """
        Inserta un nuevo pedido en la base de datos.

        Args:
            id_proveedor (int): ID del proveedor
            id_producto (int): ID del producto
            descripcion (str): Texto opcional con detalles del pedido
            cantidad (int): Número de unidades
            fecha_entrega (str): Fecha de entrega (YYYY-MM-DD)

        Returns:
            bool: True si se insertó correctamente, False si hubo error
        """
        # Validamos que la cantidad sea válida
        if cantidad is None or cantidad <= 0:
            logging.warning("Cantidad inválida. Pedido no registrado.")
            return False
        # Validamos que la fecha no esté vacía
        if not fecha_entrega:
            logging.warning("Fecha de entrega vacía. Pedido no registrado.")
            return False

        try:
            # Creamos una conexión independiente para registrar el pedido
            compra = ConexionCompra(id_proveedor, id_producto, descripcion, cantidad)

            if not compra.conexion:
                logging.error("No se pudo abrir conexión para registrar el pedido.")
                return False

            try:
                exito = compra.insertar_compra(fecha_entrega)
                if exito:
                    logging.info(f"Pedido registrado: Producto {id_producto}, Cantidad {cantidad}, Proveedor {id_proveedor}")
                    return True
                else:
                    logging.warning("La inserción de la compra falló.")
                    return False
            finally:
                compra.cerrar()

        except Exception as e:
            logging.error(f"Error al registrar pedido: {e}")
            return False

    def cerrar(self):
        """
        Cierra la conexión principal con la base de datos.
        Esto libera los recursos y es buena práctica hacerlo
        cuando ya no necesitamos usar la conexión.
        """
        self.conexion_bd.cerrar()
        logging.info("Conexión a la base de datos cerrada.")
