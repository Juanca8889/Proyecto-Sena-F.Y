import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pepito1234", 
        database="montallantasfy",
        charset="utf8mb4"
    )



