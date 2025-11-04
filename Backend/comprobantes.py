
from datetime import datetime
from BD.conexion import conectar 

# --- LÓGICA DE PLANTILLAS DE COMPROBANTE ---

class ConexionUsuario:
    def __init__(self, id_venta, cliente_id, cantidad, descripcion, fecha_venta, encargado_id, monto):
        self.conexion= conectar()
        self.id_venta= id_venta
        self.cliente_id = cliente_id
        self.cantidad = apellido
        self.descripcion = celular
        self.fecha_venta = usuario
        self.encargado_id =  clave
        self.monto = correo
        self.cursor = self.conexion.cursor()

    def insertar_usuario(self):
        query2 = "INSERT INTO Usuario (nombre, apellido, celular, correo, usuario, clave) VALUES (%s,%s,%s,%s,%s, UNHEX(SHA2(%s, 512)));"
        # query = "INSERT INTO Usuario (Nombre, `contraseña`, correo)VALUES (%s, UNHEX(SHA2(%s, 512)), %s)"
        values = (self.nombre, self.apellido, self.celular,self.correo, self.usuario, self.clave)
        self.cursor.execute(query2, values)
        self.conexion.commit()

    def obtener_usuarios(self):
        self.cursor.execute("SELECT * FROM Usuarios")
        return self.cursor.fetchall()

    def buscar_usuario(self, nombre):
        query = "SELECT * FROM Usuarios WHERE Nombre = %s"
        self.cursor.execute(query, (nombre,))
        return self.cursor.fetchall()

    
    def actualizar_usuario(self, nombre, nueva_contrasena, nuevo_correo):
        query = "UPDATE Usuarios SET `contraseña` = %s, correo = %s WHERE Nombre = %s"
        values = (nueva_contrasena, nuevo_correo, nombre)
        self.cursor.execute(query, values)
        self.conexion.commit()
    
    
    









