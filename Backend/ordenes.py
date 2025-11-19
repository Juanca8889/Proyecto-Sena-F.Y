from BD.conexion import conectar

class Servicio:
    def __init__(self, 
                 id_servicio=None, 
                 descripcion=None, 
                 tipo=None, 
                 fecha=None, 
                 cliente_id=None, 
                 usuario_id=None,
                 id_domicilio=None,
                 monto=None):
        
        self.conexion = conectar()
        self.cursor = self.conexion.cursor(dictionary=True)
        
        # Campos de servicio
        self.id_servicio = id_servicio
        self.descripcion = descripcion
        self.tipo = tipo
        self.fecha = fecha
        self.cliente_id = cliente_id
        self.usuario_id = usuario_id
        
        # Campos de domicilio
        self.id_domicilio = id_domicilio
        self.monto = monto

    # =====================================================
    #  MÉTODOS PARA TABLA SERVICIO
    # =====================================================

    def insertar_servicio(self):
        """Inserta un nuevo registro en la tabla servicio"""
        query = """
        INSERT INTO servicio (descripcion, tipo, fecha, cliente_id, usuario_id)
        VALUES (%s, %s, %s, %s, %s);
        """
        values = (self.descripcion, self.tipo, self.fecha, self.cliente_id, self.usuario_id)
        self.cursor.execute(query, values)
        self.conexion.commit()
        return True

    def mostrar_servicios(self, orden=None):
        """Devuelve todos los servicios con filtros opcionales"""
        base_query = """
        SELECT id_servicio, descripcion, tipo, fecha, cliente_id, usuario_id
        FROM servicio
        """
        if orden == "recientes":
            base_query += " ORDER BY id_servicio DESC"
        elif orden == "antiguos":
            base_query += " ORDER BY id_servicio ASC"
        elif orden == "taller":
            base_query += " WHERE tipo = 'taller'"
        elif orden == "domicilio":
            base_query += " WHERE tipo = 'domicilio'"
        
        self.cursor.execute(base_query)
        servicios = self.cursor.fetchall()
        return servicios

    def buscar_servicio(self, id_servicio):
        """Busca un servicio por su ID"""
        query = "SELECT * FROM servicio WHERE id_servicio = %s;"
        self.cursor.execute(query, (id_servicio,))
        return self.cursor.fetchone()

    def actualizar_servicio(self, id_servicio, descripcion, tipo, fecha, cliente_id, usuario_id):
        """Actualiza los datos de un servicio"""
        query = """
        UPDATE servicio
        SET descripcion=%s, tipo=%s, fecha=%s, cliente_id=%s, usuario_id=%s
        WHERE id_servicio=%s;
        """
        values = (descripcion, tipo, fecha, cliente_id, usuario_id, id_servicio)
        self.cursor.execute(query, values)
        self.conexion.commit()

    def eliminar_servicio(self, id_servicio):
        """Elimina un servicio por su ID"""
        query = "DELETE FROM servicio WHERE id_servicio = %s;"
        self.cursor.execute(query, (id_servicio,))
        self.conexion.commit()

    # =====================================================
    #  MÉTODOS PARA TABLA DOMICILIO
    # =====================================================

    def insertar_domicilio(self):
        """Inserta un nuevo registro en la tabla domicilio"""
        query = """
        INSERT INTO domicilio (cliente_id, servicio_id, fecha, monto, usuario_id)
        VALUES (%s, %s, %s, %s, %s);
        """
        values = (self.cliente_id, self.id_servicio, self.fecha, self.monto, self.usuario_id)
        self.cursor.execute(query, values)
        self.conexion.commit()

    def mostrar_domicilios(self):
        """Devuelve todos los registros de la tabla domicilio"""
        query = """
        SELECT d.id_domicilio, d.fecha, d.monto, 
            c.nombre AS cliente, s.descripcion AS servicio, 
            s.tipo, u.nombre AS usuario
        FROM domicilio d
        LEFT JOIN cliente c ON d.cliente_id = c.id_cliente
        LEFT JOIN servicio s ON d.servicio_id = s.id_servicio
        LEFT JOIN usuario u ON d.usuario_id = u.id_usuario
        ORDER BY d.id_domicilio DESC;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def buscar_domicilio(self, id_domicilio):
        """Busca un domicilio por su ID"""
        query = "SELECT * FROM domicilio WHERE id_domicilio = %s;"
        self.cursor.execute(query, (id_domicilio,))
        return self.cursor.fetchone()

    def eliminar_domicilio(self, id_domicilio):
        """Elimina un domicilio por su ID"""
        query = "DELETE FROM domicilio WHERE id_domicilio = %s;"
        self.cursor.execute(query, (id_domicilio,))
        self.conexion.commit()

    # =====================================================
    #  CERRAR CONEXIÓN
    # =====================================================
    def cerrar(self):
        self.cursor.close()
        self.conexion.close()
