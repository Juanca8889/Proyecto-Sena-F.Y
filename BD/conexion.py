import mysql.connector  # Librería oficial de MySQL para conectarse desde Python
from datetime import datetime


# ==========================================
# FUNCIÓN DE CONEXIÓN GENERAL
# ==========================================
def conectar():
    """
    Crea y devuelve una conexión a la base de datos MySQL.
    """
    return mysql.connector.connect(
        host="localhost",          # Dirección del servidor MySQL (local)
        user="root",               # Usuario de MySQL
        password="",               # Contraseña del usuario (vacía por defecto en tu caso)
        database="montallantasfy", # Nombre de la base de datos
        charset="utf8mb4"          # Codificación recomendada para acentos y caracteres especiales
    )