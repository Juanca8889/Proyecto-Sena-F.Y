from BD.BDa import conectar

class CreacionReferencia:
    def __init__(self):
    
        self.conn = conectar()
        self.cursor = self.conn.cursor(dictionary=True) 

    def listar_referencias(self):
        """Obtiene todas las referencias de la BD"""
        query = "SELECT codigo, nombre, cantidad, fecha, imagen FROM referencias"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def crear_referencia(self, nombre, cantidad, codigo, fecha, imagen=None):
        """Inserta una nueva referencia en la BD"""
        query = """
            INSERT INTO referencias (nombre, cantidad, codigo, fecha, imagen)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (nombre, cantidad, codigo, fecha, imagen)
        self.cursor.execute(query, valores)
        self.conn.commit()
        return True

    def buscar_por_codigo(self, codigo):
        """Busca una referencia por su código"""
        query = "SELECT * FROM referencias WHERE codigo = %s"
        self.cursor.execute(query, (codigo,))
        return self.cursor.fetchone()

    def cerrar(self):
        """Cierra la conexión"""
        self.cursor.close()
        self.conn.close()
