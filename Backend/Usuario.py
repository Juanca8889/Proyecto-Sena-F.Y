from BD.conexion import conectar

class ConexionUsuario:
    def __init__(self,  nombre = None, apellido= None, celular=None, correo= None, usuario= None, clave=None ):
        self.conexion = conectar()
        self.nombre = nombre
        self.apellido = apellido
        self.celular = celular
        self.usuario = usuario
        self.clave =  clave
        self.correo = correo
        self.cursor = self.conexion.cursor(dictionary=True)

    def insertar_usuario(self):
        query2 = "INSERT INTO Usuario (nombre, apellido, celular, correo, usuario, clave) VALUES (%s,%s,%s,%s,%s, UNHEX(SHA2(%s, 512)));"
        # query = "INSERT INTO Usuario (Nombre, `contraseña`, correo)VALUES (%s, UNHEX(SHA2(%s, 512)), %s)"
        values = (self.nombre, self.apellido, self.celular,self.correo, self.usuario, self.clave)
        self.cursor.execute(query2, values)
        self.conexion.commit()

    def obtener_usuarios(self):
        self.cursor.execute("SELECT * FROM Usuarios")
        return self.cursor.fetchall()

    def obtener_nombre(self, id):
        query = "SELECT nombre FROM usuario WHERE id_usuario = %s LIMIT 1"
        self.cursor.execute(query, (id,))
        resultado = self.cursor.fetchone()
        return resultado['nombre'] if resultado else None

    
    def buscar_usuario(self, nombre):
        query = "SELECT * FROM Usuarios WHERE id_usuario = %s"
        self.cursor.execute(query, (nombre,))
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
        
    def actualizar_contacto(self, id_usuario, nuevo_celular, nuevo_correo):
        query = """
            UPDATE Usuario
            SET celular = %s, correo = %s
            WHERE id_usuario = %s
        """
        valores = (nuevo_celular, nuevo_correo, id_usuario)
        self.cursor.execute(query, valores)
        self.conexion.commit()
        return True

        
    def obtener_por_id(self, id_usuario):
        query = "SELECT * FROM usuario WHERE id_usuario = %s"
        self.cursor.execute(query, (id_usuario,))
        return self.cursor.fetchone()

    
    
    def eliminar_usuario(self, nombre):
        query = "DELETE FROM Usuarios WHERE Nombre = %s"
        self.cursor.execute(query, (nombre,))
        self.conexion.commit()
        
        
    
    def cerrar(self):
        self.cursor.close()
        self.conexion.close()
        
    def obtener_usuarios_paginados(self, limit, offset):
        """
        Devuelve usuarios con paginación.
        limit -> cantidad por página
        offset -> desde qué registro empieza
        """
        try:
            query = """
                SELECT id_usuario, nombre, apellido, celular, correo, usuario, rol_id
                FROM Usuario
                ORDER BY id_usuario ASC
                LIMIT %s OFFSET %s
            """
            self.cursor.execute(query, (limit, offset))
            return self.cursor.fetchall()
        except Exception as e:
            print("❌ Error al obtener usuarios paginados:", e)
            return []
        
    def contar_usuarios(self):
        """
        Devuelve el número total de usuarios en la tabla.
        """
        try:
            self.cursor.execute("SELECT COUNT(*) AS total FROM Usuario")
            resultado = self.cursor.fetchone()
            return resultado["total"] if resultado else 0
        except Exception as e:
            print("❌ Error al contar usuarios:", e)
            return 0
        
    def cambiar_rol(self, id_usuario, nuevo_rol):
        """
        Cambia el rol del usuario.
        nuevo_rol:
        1 -> Admin
        2 -> Empleado
        """
        try:
            query = "UPDATE Usuario SET rol_id = %s WHERE id_usuario = %s"
            self.cursor.execute(query, (nuevo_rol, id_usuario))
            self.conexion.commit()
            return True
        except Exception as e:
            print("❌ Error al cambiar rol:", e)
            return False





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