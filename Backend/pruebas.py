import mysql.connector

class Inventario:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",        # cambia por tu usuario
            password="",        # cambia por tu contraseña
            database="montallantasfy"
        )
        self.cursor = self.conexion.cursor(dictionary=True)

    def registrar_producto(self, nombre, descripcion, cantidad, categoria_id, precio):
        query = """
        INSERT INTO Producto (nombre, descripcion, cantidad, categoria_id, precio)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (nombre, descripcion, cantidad, categoria_id, precio)
        self.cursor.execute(query, valores)
        self.conexion.commit()
        print("✅ Producto registrado con éxito.")

    def registrar_inventario(self, producto_id, cantidad, categoria_id, rol_id=None):
        query = """
        INSERT INTO InventarioProductos (producto_id, cantidad, categoria_id, rol_id)
        VALUES (%s, %s, %s, %s)
        """
        valores = (producto_id, cantidad, categoria_id, rol_id)
        self.cursor.execute(query, valores)
        self.conexion.commit()
        print("✅ Inventario actualizado.")

    def mostrar_inventario(self):
        query = """
        SELECT p.nombre, p.descripcion, p.precio, ip.cantidad, c.nombre AS categoria, r.nombre AS rol
        FROM InventarioProductos ip
        INNER JOIN Producto p ON ip.producto_id = p.id
        INNER JOIN categoriaProductos c ON ip.categoria_id = c.id
        LEFT JOIN Rol r ON ip.rol_id = r.id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    
# Crear objeto Inventario
inv = Inventario()

# Registrar un producto
inv.registrar_producto("Llanta 185/65 R15", "Llanta para automóvil", 20, 1, 350000)

# Registrar inventario
inv.registrar_inventario(1, 20, 1, 2)

# Mostrar inventario
for fila in inv.mostrar_inventario():
    print(fila)
