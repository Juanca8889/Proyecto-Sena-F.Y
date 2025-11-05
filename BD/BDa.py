import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="montallantasfy",
        charset="utf8mb4"
    )



