import mysql.connector
from datetime import datetime

class ConexionCompra:
    
    def __init__(self, id_proveedor, id_producto, descripcion, cantidad):

        try:
            self.conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                database="montallantasfy",
                password="1234", 
                charset="utf8mb4"
            )
            self.cursor = self.conexion.cursor()
            
           
            self.id_proveedor = id_proveedor
            self.id_producto = id_producto
            self.descripcion = descripcion
            self.cantidad = cantidad
            
            self.fecha_pedido = datetime.now().strftime("%Y-%m-%d") #Este crea la fecha automaticamente

        except mysql.connector.Error as err:
            print(f"Error de conexión: {err} ")
            self.conexion = None
            self.cursor = None

    def insertar_compra(self, fecha_entrega):
       
        if not self.conexion:
            print("No se pudo insertar. No hay conexión a la base de datos.")
            return

        try:
            query = "CALL ingresar_comprar(%s, %s, %s, %s, %s, %s)"
            values = (
                self.id_proveedor,
                self.id_producto,
                self.descripcion,
                self.cantidad,
                self.fecha_pedido,
                fecha_entrega
            )
            self.cursor.execute(query, values)
            self.conexion.commit() 
            print("¡Compra insertada con éxito! ")
            
        except mysql.connector.Error as err:
            print(f"Error al insertar la compra: {err} ")
            self.conexion.rollback() 
    def cerrar(self):
        """Cierra la conexión a la base de datos de forma segura."""
        if self.conexion and self.conexion.is_connected():
            self.cursor.close()
            self.conexion.close()
            print("Conexión cerrada.")


if __name__ == "__main__":

    compra = ConexionCompra(
        id_proveedor=2,
        id_producto=9,
        descripcion="Tornillos lws",
        cantidad=25
    )

    
    if compra.conexion:
        compra.insertar_compra(fecha_entrega="2025-06-14")

    compra.cerrar()