import mysql.connector

def conexion():
    return  mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="montallantasfy"
    )


class Inventario:
    def __init__(self, id, nombre, descripcion, cantidad, categoria_id, precio):

        self.id= id
        self.id= nombre
        self.id= descripcion
        self.id= cantidad
        self.id= categoria_id
        self.id= precio
                
    

    def registrar_producto(self):
        query = """INSERT INTO Inventario (Nombre, Cantidad, Codigo, FechaIngreso, Miniatura) 
                   VALUES (%s, %s, %s, %s, %s)"""
        values = (self.nombre, self.cantidad, self.codigo, self.fecha_ingreso, self.miniatura)
        self.cursor.execute(query, values)
        self.conexion.commit()
        print(f"Se han registrado {self.cantidad} unidades de '{self.nombre}' en el inventario")


    def obtener_productos(self, orden_alfabetico=False):
        query = "SELECT * FROM Inventario"
        if orden_alfabetico:
            query += " ORDER BY Nombre ASC"
        self.cursor.execute(query)
        return self.cursor.fetchall()




    def buscar_producto(self, codigo):
        query = "SELECT * FROM Inventario WHERE Codigo = %s"
        self.cursor.execute(query, (codigo,))
        return self.cursor.fetchall()


    def filtrar_por_fecha(self, fecha):
        query = "SELECT * FROM Inventario WHERE FechaIngreso = %s"
        self.cursor.execute(query, (fecha,))
        return self.cursor.fetchall()


    def actualizar_producto(self, codigo, nuevo_nombre, nueva_cantidad, nueva_fecha, nueva_miniatura):
        query = """
        UPDATE Inventario
        SET Nombre = %s, Cantidad = %s, FechaIngreso = %s, Miniatura = %s
        WHERE Codigo = %s
        """
        values = (nuevo_nombre, nueva_cantidad, nueva_fecha, nueva_miniatura, codigo)
        self.cursor.execute(query, values)
        self.conexion.commit()
        print(f" Producto con código {codigo} actualizado correctamente.")



    def eliminar_producto(self, codigo):
        query = "DELETE FROM Inventario WHERE Codigo = %s"
        self.cursor.execute(query, (codigo,))
        self.conexion.commit()
        print(f"🗑 Producto con código {codigo} eliminado correctamente.")



    def cerrar(self):
        self.cursor.close()
        self.conexion.close()


producto = Inventario(
    nombre="Parche PP4",
    cantidad=5,
    codigo="#0001",
    fecha_ingreso="2025-08-21",
    miniatura="parche_pp4.png"
)

producto.registrar_producto()

productos = producto.obtener_productos(orden_alfabetico=True)
for p in productos:
    print(p)

print(producto.buscar_producto("#0001"))

print(producto.filtrar_por_fecha("2025-08-21"))

producto.actualizar_producto("#0001", "Parche Premium asdadsPP4", 10, "2025-08-22", "pp4_nuevo.png")

producto.cerrar()
