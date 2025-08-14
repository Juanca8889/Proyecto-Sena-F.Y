import mysql.connector
'''
#prueba de conexion a la base de datos jcgs

datos de conexion
conexion = mysql.connector.connect(
    host="localhost",
    user= "root",
    database="bd",
)

Verificar si la conexión fue exitosa
cursor=conexion.cursor()

Ejecutar una consulta en la base de datos
cursor.execute("select * from Usuarios")


Imprimir los resultados o que salgan los datos
for fila in cursor.fetchall():
print(fila)

insertar datos a la base de datos
cursor.execute("insert into Usuarios (Nombre, contraseña,correo) values ('Juan', '124','juan@gmail.com')")

cursor.execute("select * from Usuarios")
for fila in cursor.fetchall():
    print(fila)

cerrar la conexión
cursor.close()
conexion.close()

'''
class ConexionUsuario:
    def __init__(self, nombre, contrasena, correo):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            database="bd",
            charset="utf8mb4"
        )
        self.nombre = nombre
        self.contrasena = contrasena
        self.correo = correo
        self.cursor = self.conexion.cursor()

    def insertar_usuario(self):
        query = "INSERT INTO Usuarios (Nombre, `contraseña`, correo) VALUES (%s, %s, %s)"
        values = (self.nombre, self.contrasena, self.correo)
        self.cursor.execute(query, values)
        self.conexion.commit()

    def obtener_usuarios(self):
        self.cursor.execute("SELECT * FROM Usuarios")
        return self.cursor.fetchall()

    def buscar_usuario(self, nombre):
        query = "SELECT * FROM Usuarios WHERE Nombre = %s"
        self.cursor.execute(query, (nombre,))
        return print(self.cursor.fetchall())

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


# Ejemplo de uso
persona = ConexionUsuario("Juan", "1234", "juanito@gmail.com")
persona.insertar_usuario()
usuarios = persona.obtener_usuarios()