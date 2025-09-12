from BD.conexion import  conectar

class ConexionAgenda:
    def __init__(self, fecha, descripcion):
        self.conexion = conectar()
        self.fecha = fecha
        self.descripcion = descripcion
        self.cursor = self.conexion.cursor(dictionary=True)
        
    def insertar_dia(self):
        pass
    # falta hacer la tabla agenda en la base de datos IMPORTANTE