import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        database="bd",
        charset="utf8mb4"
    )

class ConexionUsuario:
    def __init__(self, nombre, contrasena, correo, ):
        self.conexion = conectar()
        self.nombre = nombre
        self.contrasena = contrasena
        self.correo = correo
        self.cursor = self.conexion.cursor()

    def insertar_usuario(self):
        query = "INSERT INTO Usuarios (Nombre, `contraseña`, correo)VALUES (%s, UNHEX(SHA2(%s, 512)), %s)"
        values = (self.nombre, self.contrasena, self.correo, )
        self.cursor.execute(query, values)
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



def verificar_usuario(username, password):
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.idusua, u.Nombre, u.correo, u.id_rol, r.Nombre as rol
            FROM Usuarios u
            JOIN rol r ON u.id_rol = r.idrol
            WHERE u.Nombre=%s AND u.contraseña=UNHEX(SHA2(%s, 512))
            LIMIT 1
        """, (username, password))
        usuario = cursor.fetchone()
        conexion.close()
        return usuario