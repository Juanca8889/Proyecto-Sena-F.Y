import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        database="montallantasfy",
        charset="utf8mb4"
    )

class ConexionClientes:
    def __init__(self,  id_cliente = None ,nombre = None,apellido = None,celular = None ,correo= None ,direccion = None ,placa = None ,modelo = None):
        self.conexion = conectar()
        self.cursor = self.conexion.cursor(dictionary=True)
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.celular = celular
        self.correo = correo
        self.direccion = direccion
        self.placa = placa
        self.modelo = modelo

    def insertar_usuario(self):
        query = "CALL Insertar_cliente(%s, %s, %s, %s, %s, %s, %s);"
        values = (self.id_cliente, self.nombre, self.apellido, self.celular, self.correo, self.direccion, self.placa, self.modelo)
        self.cursor.execute(query, values)
        self.conexion.commit()

    def mostrar_clientes(self):
        self.cursor.execute("SELECT id_cliente, nombre, correo, celular, modelo, placa  FROM Cliente")
        clientes = self.cursor.fetchall()
        return clientes
        

    def buscar_usuario(self, nombre):
        pass

    def actualizar_usuario(self, nombre, nueva_contrasena, nuevo_correo):
        pass
        
    def eliminar_usuario(self, nombre):
        pass
        
        
    
    def cerrar(self):
        self.cursor.close()
        self.conexion.close()



