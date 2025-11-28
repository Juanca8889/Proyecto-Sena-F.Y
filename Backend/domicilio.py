

class Domicilio:
    def __init__(self,conexion):
        self.conexion = conexion

    def obtener_todos(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vista_domicilios")
        domicilios = cursor.fetchall()
        cursor.close()
        return domicilios

    def registrar(self, cliente_id, servicio_id, fecha, monto, usuario_id):
        cursor = self.conexion.cursor()
        sql = """
            INSERT INTO domicilio (cliente_id, servicio_id, fecha, monto, usuario_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (cliente_id, servicio_id, fecha, monto, usuario_id))
        self.conexion.commit()
        cursor.close()
