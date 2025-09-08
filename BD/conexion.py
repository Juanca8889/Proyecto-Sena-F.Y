import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="montallantasfy",
        charset="utf8mb4"
    )

class ConexionCompra:
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
        if not self.cursor:
            print("No hay conexión a la BD.")
            return False

        try:
            self.cursor.execute("""
                INSERT INTO compra (proveedor_id, producto_id, descripcion, cantidad, fecha_pedido, fecha_entrega)
                VALUES (%s, %s, %s, %s, CURDATE(), %s)
            """, (self.id_proveedor, self.id_producto, self.descripcion, self.cantidad, fecha_entrega))

            self.cursor.execute("""
                UPDATE producto
                SET cantidad = cantidad + %s
                WHERE id_producto = %s
            """, (self.cantidad, self.id_producto))

            self.conexion.commit()
            print("Compra insertada y stock actualizado correctamente.")
            return True
        except Exception as e:
            print(f"Error al insertar compra o actualizar stock: {e}")
            self.conexion.rollback()
            return False

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()
        print("Conexión a la base de datos cerrada.")
