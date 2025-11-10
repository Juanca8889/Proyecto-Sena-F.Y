import mysql.connector

class GestorProveedores:
    def __init__(self):
      
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="sistema_inventario"
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def obtener_proveedores(self):
        query = "SELECT * FROM Proveedor"
        self.cursor.execute(query)
        proveedores = self.cursor.fetchall()
        return proveedores

    def obtener_proveedor_por_id(self, id_proveedor):
        query = "SELECT * FROM Proveedor WHERE id_proveedor = %s"
        self.cursor.execute(query, (id_proveedor,))
        proveedor = self.cursor.fetchone()
        return proveedor
    
    def registrar_proveedor(self, nombre, telefono, correo, direccion, tipo, nit):
        try:
        
            sql = "CALL RegistrarProveedor(%s, %s, %s, %s, %s, %s)"
            valores = (nombre, telefono, correo, direccion, tipo, nit)
            self.cursor.execute(sql, valores)
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error al registrar proveedor: {err}")
            self.conn.rollback()


    def actualizar_proveedor(self, id_proveedor, nombre, telefono, correo, direccion, tipo, nit):
        try:
            sql = "CALL ActualizarProveedor(%s, %s, %s, %s, %s, %s, %s)"
            valores = (id_proveedor, nombre, telefono, correo, direccion, tipo, nit)
            self.cursor.execute(sql, valores)
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error al actualizar proveedor: {err}")
            self.conn.rollback()


    def eliminar_proveedor(self, id_proveedor):
        try:
            sql = "CALL EliminarProveedor(%s)"
            self.cursor.execute(sql, (id_proveedor,))
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error al eliminar proveedor: {err}")
            self.conn.rollback()


    def verificar_nit_existente(self, nit):
        query = "SELECT COUNT(*) AS total FROM Proveedor WHERE nit = %s"
        self.cursor.execute(query, (nit,))
        resultado = self.cursor.fetchone()
        return resultado["total"] > 0


    def __del__(self):
        self.cursor.close()
        self.conn.close()
