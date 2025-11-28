import mysql.connector
from dotenv import load_dotenv
import os

def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        charset="utf8mb4"
    )



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
