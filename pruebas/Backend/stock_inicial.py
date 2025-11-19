# ==========================================
# IMPORTACIONES
# ==========================================
import os
import sys

# Asegurar que la raíz del proyecto esté en sys.path para poder importar BD.conexion
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from BD.conexion import conectar

# ==========================================
# CLASE PARA GESTIONAR EL STOCK INICIAL
# ==========================================
class GestorStock:
    def __init__(self):
        try:
            self.conexion = conectar()
            self.cursor = self.conexion.cursor(dictionary=True)
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.conexion = None
            self.cursor = None

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()

    # ==========================================
    # OBTENER TODOS LOS PRODUCTOS (con paginación, orden, búsqueda)
    # ==========================================
    def obtener_productos(self, busqueda="", pagina=1, limite=20, ordenar_por="nombre", orden="asc"):
        if not self.cursor:
            return [], 0

        try:
            offset = (pagina - 1) * limite
            like = f"%{busqueda}%"

            campos_permitidos = {
                "codigo": "p.id_producto",
                "nombre": "p.nombre",
                "tipo": "c.nombre",
                "precio": "p.precio",
                "stock": "p.cantidad"
            }

            orden_columna = campos_permitidos.get(ordenar_por, "p.nombre")
            orden_tipo = "ASC" if orden.lower() == "asc" else "DESC"

            query = f"""
                SELECT 
                    p.id_producto AS codigo,
                    p.nombre,
                    c.nombre AS tipo,
                    p.precio,
                    p.cantidad AS stock
                FROM producto p
                LEFT JOIN categoriaProductos c ON p.categoria_id = c.id_categoria
                WHERE p.nombre LIKE %s
                ORDER BY {orden_columna} {orden_tipo}
                LIMIT %s OFFSET %s
            """

            self.cursor.execute(query, (like, limite, offset))
            productos = self.cursor.fetchall()

            # Total de productos para paginación
            self.cursor.execute("SELECT COUNT(*) AS total FROM producto WHERE nombre LIKE %s", (like,))
            total = self.cursor.fetchone()["total"]

            return productos, total
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return [], 0

    # ==========================================
    # OBTENER STOCK ACTUAL (nombre, id y cantidad)
    # ==========================================
    def obtener_stock(self):
        if not self.cursor:
            return []

        try:
            self.cursor.execute("""
                SELECT id_producto, nombre, cantidad
                FROM producto
                ORDER BY nombre ASC
            """)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener stock: {e}")
            return []

    # ==========================================
    # ACTUALIZAR STOCK DE UN PRODUCTO
    # ==========================================
    def actualizar_stock_inicial(self, id_producto, cantidad):
        if not self.cursor:
            return False

        try:
            self.cursor.execute("""
                UPDATE producto
                SET cantidad = %s,
                    updated_at = NOW()
                WHERE id_producto = %s
            """, (cantidad, id_producto))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar stock: {e}")
            self.conexion.rollback()
            return False

    # ==========================================
    # OPCIONES PARA FILTROS DE BÚSQUEDA
    # ==========================================
    def obtener_opciones_filtros(self):
        if not self.cursor:
            return {"tipos": [], "nombres": []}

        try:
            self.cursor.execute("SELECT nombre FROM categoriaProductos ORDER BY nombre ASC")
            tipos = [r["nombre"] for r in self.cursor.fetchall() if r.get("nombre")]

            self.cursor.execute("SELECT DISTINCT nombre FROM producto ORDER BY nombre ASC")
            nombres = [r["nombre"] for r in self.cursor.fetchall() if r.get("nombre")]

            return {"tipos": tipos, "nombres": nombres}
        except Exception as e:
            print(f"Error al obtener opciones de filtros: {e}")
            return {"tipos": [], "nombres": []}

    # ==========================================
    # CREAR CATEGORÍA SI NO EXISTE
    # ==========================================
    def crear_categoria_si_no_existe(self, nombre_categoria):
        if not self.cursor:
            return None

        nombre_categoria = (nombre_categoria or "").strip()
        if not nombre_categoria:
            return None

        try:
            self.cursor.execute("SELECT id_categoria FROM categoriaProductos WHERE nombre = %s", (nombre_categoria,))
            row = self.cursor.fetchone()
            if row:
                return row.get("id_categoria")

            self.cursor.execute("INSERT INTO categoriaProductos (nombre) VALUES (%s)", (nombre_categoria,))
            self.conexion.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error al crear/consultar categoría: {e}")
            self.conexion.rollback()
            return None

    # ==========================================
    # CREAR PRODUCTO (sin requerir código)
    # ==========================================
    def crear_producto(self, nombre, categoria_nombre, precio, stock, descripcion=""):
        if not self.cursor:
            return False

        try:
            nombre = (nombre or "").strip()
            categoria_nombre = (categoria_nombre or "").strip()
            descripcion = (descripcion or "").strip()
            precio = float(precio)
            stock = int(stock)

            if not nombre or precio < 0 or stock < 0:
                return False

            categoria_id = self.crear_categoria_si_no_existe(categoria_nombre) if categoria_nombre else None

            self.cursor.execute(
                """
                INSERT INTO producto (nombre, descripcion, cantidad, precio, categoria_id, updated_at)
                VALUES (%s, %s, %s, %s, %s, NOW())
                """,
                (nombre, descripcion, stock, precio, categoria_id),
            )
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al crear producto: {e}")
            self.conexion.rollback()
            return False

    # ==========================================
    # OBTENER PRODUCTOS CON FILTROS AVANZADOS
    # ==========================================
    def obtener_productos_con_filtros(
        self,
        filtro_codigo="",
        filtro_nombre="",
        filtro_tipo="",
        filtro_precio="",
        filtro_stock="",
        filtro_fecha="",
        pagina=1,
        limite=20,
        ordenar_por="codigo",
        orden="asc"
    ):
        if not self.cursor:
            return [], 0

        try:
            offset = (pagina - 1) * limite
            condiciones = []
            params = []

            if filtro_codigo:
                condiciones.append("p.id_producto LIKE %s")
                params.append(f"%{filtro_codigo}%")
            if filtro_nombre:
                condiciones.append("p.nombre LIKE %s")
                params.append(f"%{filtro_nombre}%")
            if filtro_tipo:
                condiciones.append("c.nombre LIKE %s")
                params.append(f"%{filtro_tipo}%")
            if filtro_precio:
                condiciones.append("CAST(p.precio AS CHAR) LIKE %s")
                params.append(f"%{filtro_precio}%")
            if filtro_stock:
                condiciones.append("CAST(p.cantidad AS CHAR) LIKE %s")
                params.append(f"%{filtro_stock}%")
            if filtro_fecha:
                condiciones.append("DATE(p.updated_at) = %s")
                params.append(filtro_fecha)

            where_sql = " AND ".join(condiciones) if condiciones else "1"

            campos_permitidos = {
                "codigo": "p.id_producto",
                "nombre": "p.nombre",
                "tipo": "c.nombre",
                "precio": "p.precio",
                "stock": "p.cantidad",
                "fecha": "p.updated_at"
            }

            orden_columna = campos_permitidos.get(ordenar_por, "p.id_producto")
            orden_tipo = "ASC" if orden.lower() == "asc" else "DESC"

            sql_query = f"""
                SELECT 
                    p.id_producto AS codigo,
                    p.nombre,
                    c.nombre AS tipo,
                    p.precio,
                    p.cantidad AS stock,
                    DATE_FORMAT(p.updated_at, '%Y-%m-%d') AS updated_at
                FROM producto p
                LEFT JOIN categoriaProductos c ON p.categoria_id = c.id_categoria
                WHERE {where_sql}
                ORDER BY {orden_columna} {orden_tipo}
                LIMIT %s OFFSET %s
            """

            params.extend([limite, offset])
            self.cursor.execute(sql_query, params)
            productos = self.cursor.fetchall()

            count_query = f"""
                SELECT COUNT(*) AS total
                FROM producto p
                LEFT JOIN categoriaProductos c ON p.categoria_id = c.id_categoria
                WHERE {where_sql}
            """
            self.cursor.execute(count_query, params[:-2])
            total = self.cursor.fetchone()["total"]

            return productos, total
        except Exception as e:
            print(f"Error al obtener productos con filtros: {e}")
            return [], 0