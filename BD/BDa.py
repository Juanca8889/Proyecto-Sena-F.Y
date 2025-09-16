import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pepito1234", 
        database="montallantasfy",
        charset="utf8mb4"
    )


import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",      
            user="root",           
            password="pepito1234",  
            database="servimaq"    
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error en la conexión: {err}")
        return None
    

import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",        
            user="root",             
            password="",             
            database="montallantas" 
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None

