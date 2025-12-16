import mysql.connector
# from dotenv import load_dotenv # <--- COMENTADA/ELIMINADA
import os

# load_dotenv() # <--- COMENTADA/ELIMINADA

def conectar():
    try:
        conexion = mysql.connector.connect(
            host=os.environ.get('DB_HOST'), 
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            database=os.environ.get('DB_NAME'),
            port=int(os.environ.get('DB_PORT'))
        )
        return conexion
    except Exception as e:
        # Aquí tienes un pequeño error de sintaxis, pero la lógica es buena:
        # print(f"Error de conexión: {e}", file=sys.stderr) # "sys" no está definido
        print(f"Error de conexión: {e}") # Usaremos un print simple por ahora
        return None




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
