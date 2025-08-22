import mysql.connector
from datetime import datetime
from conexion import ConexionCompra

class GestorCompras:
   
    def __init__(self):
        
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
        
        print("--- Verificando niveles de stock y sugiriendo pedidos ---")
        try:
            
            self.conexion_bd.cursor.execute("SELECT id, nombre, cantidad FROM Producto")
            productos = self.conexion_bd.cursor.fetchall()
            
            sugerencias_encontradas = False
            for producto in productos:
                
                if producto[2] <= 30:
                    cantidad_sugerida = 50 - producto[2]
                    print(f"⚠️ ¡ALERTA! Stock bajo para '{producto[1]}' (ID: {producto[0]}).")
                    print(f"   Stock actual: {producto[2]} unidades. Se sugiere reponer {cantidad_sugerida} unidades.")
                    sugerencias_encontradas = True
            
            if not sugerencias_encontradas:
                print("✅ Todos los productos tienen un nivel de stock saludable. No hay sugerencias de pedidos.")

        except mysql.connector.Error as err:
            print(f"Error al obtener los datos de stock: {err}")
        finally:
            self.conexion_bd.cerrar() 

    def realizar_pedido(self, id_proveedor, id_producto, descripcion, cantidad, fecha_entrega):
        
        compra_nueva = ConexionCompra(id_proveedor, id_producto, descripcion, cantidad)
        if compra_nueva.conexion:
            compra_nueva.insertar_compra(fecha_entrega)
        compra_nueva.cerrar()

if __name__ == "__main__":
    
    gestor = GestorCompras()

    
    gestor.sugerir_pedido_y_alertar()

