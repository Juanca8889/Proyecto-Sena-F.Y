from BD.conexion import conectar

class ConexionProveedor:
    def __init__(self, nombre=None, telefono=None, correo=None):
        self.conexion = conectar()
        self.cursor = self.conexion.cursor(dictionary=True)
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo


    def agregar_proveedor(self):
        query = """
            INSERT INTO proveedor (nombre, telefono, correo)
            VALUES (%s, %s, %s)
        """
        values = (self.nombre, self.telefono, self.correo)
        self.cursor.execute(query, values)
        self.conexion.commit()
        return True

    def obtener_proveedores(self):
        query = "SELECT * FROM proveedor"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def obtener_proveedor_por_id(self, id_proveedor):
        query = "SELECT * FROM proveedor WHERE id_proveedor = %s"
        self.cursor.execute(query, (id_proveedor,))
        return self.cursor.fetchone()


    def actualizar_proveedor(self, id_proveedor, new_nombre, new_telefono, new_correo):
        query = """
            UPDATE proveedor
            SET nombre = %s, telefono = %s, correo = %s
            WHERE id_proveedor = %s
        """
        values = (new_nombre, new_telefono, new_correo, id_proveedor)
        self.cursor.execute(query, values)
        self.conexion.commit()
        return self.cursor.rowcount

    def eliminar_proveedor(self, id_proveedor):
        query = "DELETE FROM proveedor WHERE id_proveedor = %s"
        self.cursor.execute(query, (id_proveedor,))
        self.conexion.commit()
        return self.cursor.rowcount
