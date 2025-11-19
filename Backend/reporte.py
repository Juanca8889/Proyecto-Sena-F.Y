# reporte.py
from BD.BDa import conectar

class Reporte:
    def __init__(self, id_venta=None, cantidad=None, producto=None, fecha=None, hora=None, responsable=None, descripcion=None):
        self.id_venta = id_venta
        self.cantidad = cantidad
        self.producto = producto
        self.fecha = fecha
        self.hora = hora
        self.responsable = responsable
        self.descripcion = descripcion


    @staticmethod
    def obtener_todas(fecha=None, orden=None):
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)

        sql = "SELECT * FROM ventas WHERE estado = 'completada'"
        valores = []

    
        if fecha:
            sql += " AND DATE(fecha) = %s"
            valores.append(fecha)

 
        if orden == "recientes":
            sql += " ORDER BY fecha DESC, hora DESC"
        elif orden == "antiguos":
            sql += " ORDER BY fecha ASC, hora ASC"

        cursor.execute(sql, valores)
        ventas = cursor.fetchall()
        conexion.close()
        return ventas


    @staticmethod
    def obtener_por_id(id_venta):
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ventas WHERE id_venta = %s", (id_venta,))
        venta = cursor.fetchone()
        conexion.close()
        return venta
