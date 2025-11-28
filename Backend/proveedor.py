# proveedor.py
from BD.conexion import conectar

class Proveedor:
    def __init__(self, id_proveedor=None, nombre=None, celular=None, correo=None):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.celular = celular
        self.correo = correo

    
    def insertar(self):
        conexion = conectar()
        cursor = conexion.cursor()
        sql = "INSERT INTO proveedores (nombre, celular, correo) VALUES (%s, %s, %s)"
        valores = (self.nombre, self.celular, self.correo)
        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()

    
    @staticmethod
    def obtener_todos():
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)  
        cursor.execute("SELECT * FROM proveedores")
        proveedores = cursor.fetchall()
        conexion.close()
        return proveedores


    @staticmethod
    def obtener_por_id(id_proveedor):
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM proveedores WHERE id_proveedor = %s", (id_proveedor,))
        proveedor = cursor.fetchone()
        conexion.close()
        return proveedor


    def actualizar(self):
        conexion = conectar()
        cursor = conexion.cursor()
        sql = "UPDATE proveedores SET nombre=%s, celular=%s, correo=%s WHERE id_proveedor=%s"
        valores = (self.nombre, self.celular, self.correo, self.id_proveedor)
        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()








