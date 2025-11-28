from BD.conexion import conectar

class BusquedaInventario:
    def __init__(self):
        self.conexion = conectar()
        self.cursor = self.conexion.cursor(dictionary=True)

    def buscar(self, **criterios):
        query = "SELECT * FROM producto WHERE 1=1"
        valores = []
        for campo, valor in criterios.items():
            query += f" AND {campo} LIKE %s"
            valores.append(f"%{valor}%")
        self.cursor.execute(query, valores)
        resultados = self.cursor.fetchall()
        return resultados

    def cerrar(self):
        self.cursor.close()
        self.conexion.close()

