from BD.conexion import  conectar

class ConexionMaterial:
    def __init__(self, nombre, descripcion, cantidad, categoria_id, precio):
        self.conexion = conectar()
        self.cursor = self.conexion.cursor(dictionary=True)
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.categoria_id = categoria_id
        self.precio = precio
        

    def actualizar_material(self, id, new_nombre, new_cantidad,  new_precio):
        query = "UPDATE Producto SET nombre = %s, cantidad = %s, precio = %s WHERE id = %s"
        values = (new_nombre, new_cantidad, new_precio, id)
        self.cursor.execute(query, values)
        self.conexion.commit()
        


