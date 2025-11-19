
from BD.conexion import conectar

class DetalleCompra:
    def __init__(self, id_detalle=None, producto=None, descripcion=None, cantidad=None, monto=None, estado=None, fecha=None):
        self.id_detalle = id_detalle
        self.producto = producto
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.monto = monto
        self.estado = estado
        self.fecha = fecha


    def insertar(self):
        conexion = conectar()
        cursor = conexion.cursor()
        sql = """
            INSERT INTO detalle_compra (producto, descripcion, cantidad, monto, estado, fecha)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (self.producto, self.descripcion, self.cantidad, self.monto, self.estado, self.fecha)
        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()


    @staticmethod
    def obtener_todos():
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM detalle_compra")
        resultados = cursor.fetchall()
        conexion.close()
        return resultados

    def actualizar(self):
        conexion = conectar()
        cursor = conexion.cursor()
        sql = """
            UPDATE detalle_compra 
            SET producto=%s, descripcion=%s, cantidad=%s, monto=%s, estado=%s, fecha=%s
            WHERE id_detalle=%s
        """
        valores = (self.producto, self.descripcion, self.cantidad, self.monto, self.estado, self.fecha, self.id_detalle)
        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()

    @staticmethod
    def eliminar(id_detalle):
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM detalle_compra WHERE id_detalle=%s", (id_detalle,))
        conexion.commit()
        conexion.close()
