import mysql.connector

class BusquedaInventario:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",        # cambia por tu usuario
            password="",        # cambia por tu contraseña
            database="montallantasfy"
        )
        self.cursor = self.conexion.cursor(dictionary=True)

    def buscar(self, **criterios):
        """
        Permite buscar productos en la tabla Producto filtrando por:
        nombre, codigo, categoria_id.
        Ejemplo:
            buscar(nombre="Llanta")
            buscar(categoria_id=1)
            buscar(precio= 350000)
        """
        query = "SELECT * FROM Producto WHERE 1=1"
        valores = []

        for campo, valor in criterios.items():
            query += f" AND {campo} LIKE %s"
            valores.append(f"%{valor}%")

        self.cursor.execute(query, valores)
        resultados = self.cursor.fetchall()
        return resultados


# Ejemplo de uso
if __name__ == "__main__":
    buscador = BusquedaInventario()

    print("🔎 Buscar por nombre:")
    resultados = buscador.buscar(nombre="Llanta")
    for r in resultados:
        print(r)

    print("\n🔎 Buscar por iD")
    resultados = buscador.buscar(id=4)
    for r in resultados:
        print(r)
    
    print("\n🔎 Buscar por iD Categoria")
    resultados = buscador.buscar(categoria_id=1)
    for r in resultados:
        print(r)

    print("\n🔎 Buscar por precio")
    resultados = buscador.buscar(precio=350000)
    for r in resultados:
        print(r)
