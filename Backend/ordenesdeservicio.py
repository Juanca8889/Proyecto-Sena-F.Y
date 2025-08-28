import mysql.connector
class Servicios :
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",        # cambia por tu usuario
            password="",        # cambia por tu contraseña
            database="montallantasfy"
        )
        self.cursor = self.conexion.cursor(dictionary=True)
    
    def registrarorden(self,descripcion,tipo,fecha,cliente,usuario):
        query = """
        INSERT INTO Servicios (descripcion,tipo,fecha,cliente,usuario)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (descripcion,tipo,fecha,cliente,usuario)
        self.cursor.execute(query, valores)
        self.conexion.commit()
        print("✅ Servicio registrado con éxito.")

#ejemplo de uso 

serv = Servicios ()

serv.registrarorden("cambio de aceite","taller","2025-01-03","cliente1","usuario1")  