import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
<<<<<<< HEAD
        database="montallantasfy",
        charset="utf8mb4"
    )

class ConexionUsuario:
    def __init__(self,  nombre, apellido, celular, correo, usuario, clave ):
        self.conexion = conectar()
        self.nombre = nombre
        self.apellido = apellido
        self.celular = celular
        self.usuario = usuario
        self.clave =  clave
        self.correo = correo
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
        
    def eliminar_usuario(self, nombre):
        query = "DELETE FROM Usuarios WHERE Nombre = %s"
        self.cursor.execute(query, (nombre,))
        self.conexion.commit()
        
        
    
    def cerrar(self):
        self.cursor.close()
        self.conexion.close()
=======
        database="montallantasfy1",
        charset="utf8mb4"
    )

>>>>>>> 8f4524cf1af715343c67c28340670e4c18aa869f


def verificar_usuario(username, password):
    conexion = conectar()
    try:
        cursor = conexion.cursor(dictionary=True)
        query = """
            SELECT u.id_usuario, u.nombre, u.correo, u.rol_id, r.nombre AS rol_nombre
            FROM `Usuario` AS u
            JOIN `Rol` AS r ON u.rol_id = r.id_rol
            WHERE u.usuario = %s AND u.clave = UNHEX(SHA2(%s, 512))
            LIMIT 1
        """
        cursor.execute(query, (username, password))
        usuario = cursor.fetchone()
        return usuario
    finally:
        if cursor:
            cursor.close()
        conexion.close()
