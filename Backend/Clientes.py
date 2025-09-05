
from BD.conexion import  conectar


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

    def mostrar_clientes(self, orden=None):
        if orden == "az":
            self.cursor.execute("SELECT id_cliente, nombre, apellido, correo, celular, modelo, placa FROM Cliente ORDER BY nombre ASC")
        elif orden == "recientes":
            self.cursor.execute("SELECT id_cliente, nombre, apellido, correo, celular, modelo, placa FROM Cliente ORDER BY id_cliente DESC")
        elif orden == "antiguos":
            self.cursor.execute("SELECT id_cliente, nombre, apellido, correo, celular, modelo, placa FROM Cliente ORDER BY id_cliente ASC")
        else:
            self.cursor.execute("SELECT id_cliente, nombre, apellido, correo, celular, modelo, placa FROM Cliente")
        
        clientes = self.cursor.fetchall()
        return clientes

        

    def buscar_usuario(self, nombre):
        pass

    def actualizar_usuario(self, id_cliente, nombre, correo, celular):
        self.cursor.execute("""UPDATE Cliente SET nombre=%s, correo=%s, celular=%sWHERE id_cliente=%s""", (nombre, correo, celular, id_cliente))
        self.conexion.commit()
    
    
        
    def eliminar_cliente(self, id_cliente):
        self.cursor.execute("DELETE FROM Cliente WHERE id_cliente = %s", (id_cliente,))
        self.conexion.commit()
        
        
    
    def cerrar(self):
        self.cursor.close()
        self.conexion.close()



