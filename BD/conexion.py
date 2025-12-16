import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def conectar():
    try:
        conexion = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', ''),
            database=os.environ.get('DB_NAME', 'railway'),
            port=int(os.environ.get('DB_PORT', 3306))
        )
        return conexion
    except Exception as e:
        print(f"Error de conexión: {e}")
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
