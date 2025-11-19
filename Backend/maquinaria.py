from BD.conexion import conectar

class ConexionMaquinaria:
    def __init__(self, id_maquina=None, nombre=None, descripcion=None, estado=None):
        self.conexion = conectar()
        self.cursor = self.conexion.cursor(dictionary=True)
        self.id_maquina = id_maquina
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado

    # --- Registrar maquinaria ---
    def registrar_maquinaria(self):
        query = "INSERT INTO Maquinaria (nombre, descripcion, estado) VALUES (%s, %s, %s);"
        values = (self.nombre, self.descripcion, self.estado)
        self.cursor.execute(query, values)
        self.conexion.commit()

    # --- Mostrar todas las maquinarias ---
    def mostrar_maquinarias(self, orden=None):
        if orden == "az":
            query = "SELECT * FROM Maquinaria ORDER BY nombre ASC"
        elif orden == "recientes":
            query = "SELECT * FROM Maquinaria ORDER BY id_maquina DESC"
        elif orden == "antiguos":
            query = "SELECT * FROM Maquinaria ORDER BY id_maquina ASC"
        else:
            query = "SELECT * FROM Maquinaria"

        self.cursor.execute(query)
        return self.cursor.fetchall()

    # --- Buscar maquinaria por ID ---
    def buscar_maquinaria(self, id_maquina):
        query = "SELECT * FROM Maquinaria WHERE id_maquina = %s;"
        self.cursor.execute(query, (id_maquina,))
        return self.cursor.fetchone()

    # --- Actualizar maquinaria ---
    def actualizar_maquinaria(self, id_maquina, nombre, descripcion, estado):
        query = """
            UPDATE Maquinaria 
            SET nombre = %s, descripcion = %s, estado = %s 
            WHERE id_maquina = %s
        """
        values = (nombre, descripcion, estado, id_maquina)
        self.cursor.execute(query, values)
        self.conexion.commit()

    # --- Eliminar maquinaria ---
    def eliminar_maquinaria(self, id_maquina):
        query = "DELETE FROM Maquinaria WHERE id_maquina = %s"
        self.cursor.execute(query, (id_maquina,))
        self.conexion.commit()

    # --- Cerrar conexión ---
    def cerrar(self):
        self.cursor.close()
        self.conexion.close()
