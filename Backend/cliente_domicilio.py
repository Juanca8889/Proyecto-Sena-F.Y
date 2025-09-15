import sys      # Sirve para interactuar con el intérprete de Python y modificar rutas de búsqueda de módulos
import os       # Sirve para trabajar con rutas de archivos y carpetas de forma compatible en Windows, Linux y Mac
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from BD.conexion import conectar

class Cliente:
    def __init__(self, id_cliente=None, nombre=None, apellido=None, celular=None,
                 correo=None, direccion=None, placa=None, modelo=None):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.celular = celular
        self.correo = correo
        self.direccion = direccion
        self.placa = placa
        self.modelo = modelo

        try:
            self.conexion = conectar()
            self.cursor = self.conexion.cursor(dictionary=True)
        except Exception as e:
            print(f"Error al conectar a la BD: {e}")
            self.conexion = None
            self.cursor = None

    def listar_clientes(self):
        if not self.cursor:
            return []
        try:
            self.cursor.execute("SELECT * FROM Cliente")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener clientes: {e}")
            return []

    def registrar_cliente(self):
        if not self.cursor:
            return False
        try:
            self.cursor.execute("""
                INSERT INTO Cliente (nombre, apellido, celular, correo, direccion, placa, modelo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (self.nombre, self.apellido, self.celular, self.correo,
                  self.direccion, self.placa, self.modelo))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al registrar cliente: {e}")
            self.conexion.rollback()
            return False

    def cerrar(self):
        if self.cursor: self.cursor.close()
        if self.conexion: self.conexion.close()
