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

'''
1 paso: debe en la termnal instalar mysql-connector-python con el siguiente comando:
pip install mysql-connector-python

2 paso: deben poner el imporrt mysql.connector al inicio del archivo guardenlo aprte del backend

3 paso: deben crear una clase respectiva a lo que esten haciendo ejemplo si su desarrolo pide guardar herramientas
deben hacer la conexion con la bd del proyecto con la tabla correspondiente '''

class ConexionUsuario:
    def __init__(self, nombre, contrasena, correo):
        self.conexion = mysql.connector.connect(
            host="localhost", # esto siempre deben dejarlo igual 
            user="root", # esto tambien siempre deben dejarlo igual
            database="bd", # deben poner el nombre de la base de datos que crearon ejm:montallantasf.y como aparece en worbench
            charset="utf8mb4"# esto es para que no les de error con los acentos y caracteres especiales
        )
        #aca deben poner los datos que van a insertar, consultar , etc en la tabla de la base de datos osea las columnas de esa tabla
        self.nombre = nombre
        self.contrasena = contrasena
        self.correo = correo
        self.cursor = self.conexion.cursor()#este cursor es para que puedan ejecutar las consultas a la base de datos, osea las instrucciones que van a hacer
        
#yo cree cada metodo para que cada uno haga una funcion diferente ejemplo: insertar, consultar, actualizar, eliminar, etc
    def insertar_usuario(self):#pomgan el nombre correcto
        query = "INSERT INTO Usuarios (Nombre, `contraseña`, correo) VALUES (%s, %s, %s)"# yo le puse query pero es la instruccion
        values = (self.nombre, self.contrasena, self.correo)#los valores "%s" son estos metalos en el orden que utt ponen en la instruccion
        self.cursor.execute(query, values)# aca hace la ejecucion de la consulta a la base de datos completa
        self.conexion.commit()# el commit deben de ponerlo siempre que hagan una insercion, actualizacion o eliminacion para que se guarden los cambios en la base de datos
                        # si no lo ponen no se guardan los cambios y no se actualiza la base de datos
                        
    def obtener_usuarios(self):
        self.cursor.execute("SELECT * FROM Usuarios")
        return self.cursor.fetchall()#el fetchall() es para que obtengan todos los datos de la tabla Usuarios, si quieren un solo dato pueden usar fetchone()

    def buscar_usuario(self, nombre):
        query = "SELECT * FROM Usuarios WHERE Nombre = %s"
        self.cursor.execute(query, (nombre,))
        return print(self.cursor.fetchall())

    def actualizar_usuario(self, nombre, nueva_contrasena, nuevo_correo):
        query = "UPDATE Usuarios SET `contraseña` = %s, correo = %s WHERE Nombre = %s"
        values = (nueva_contrasena, nuevo_correo, nombre) #en los de actualizar obviamente deben poner los nuevos datos que van a actualizar
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
#primero obviamente deben crear el objeto de la clase con los datos 
#ejemplo persona
persona = ConexionUsuario("Juan", "1234", "juanito@gmail.com")
persona.insertar_usuario()
usuarios = persona.obtener_usuarios()