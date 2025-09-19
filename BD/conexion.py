import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        database="montallantasfy",
        charset="utf8mb4"
    )