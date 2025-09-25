from BD.BDa import conectar

class Devolucion:
    def __init__(self, codigo, nombre, usuario, razon, descripcion):
        self.codigo = codigo
        self.nombre = nombre
        self.usuario = usuario
        self.razon = razon
        self.descripcion = descripcion

    def registrar(self):
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """INSERT INTO devoluciones 
                         (codigo, nombre, usuario, razon, descripcion) 
                         VALUES (%s, %s, %s, %s, %s)"""
                valores = (self.codigo, self.nombre, self.usuario, self.razon, self.descripcion)
                cursor.execute(sql, valores)
                conexion.commit()
                print("Devolución registrada correctamente ✅")
            except Exception as e:
                print("Error al registrar devolución:", e)
            finally:
                cursor.close()
                conexion.close()
