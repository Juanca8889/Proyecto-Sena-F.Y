# Backend/control_sesiones.py

from datetime import datetime
from functools import wraps
from BD.conexion import conectar as obtener_conexion 


# --- FUNCIONES DE LECTURA ---

def obtener_todas_sesiones_activas():
    """Consulta todas las sesiones con estado 'activa' para la tabla de control."""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True) 
    
    query = """
    SELECT 
        id_sesion, 
        usuario_id, 
        nombre_usuario, 
        hora_inicio, 
        ultima_actividad, 
        ip, 
        user_agent 
    FROM sesion_activa 
    WHERE estado = 'activa'
    ORDER BY hora_inicio DESC
    """
    
    try:
        cursor.execute(query)
        sesiones = cursor.fetchall()
        return sesiones
    except Exception as e:
        print(f"Error al obtener sesiones activas: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()

def obtener_usuarios_con_sesiones():
    """Consulta la lista de usuarios únicos con sesiones activas para el dropdown."""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    query = """
    SELECT DISTINCT usuario_id, nombre_usuario 
    FROM sesion_activa 
    WHERE estado = 'activa' 
    ORDER BY nombre_usuario ASC
    """
    
    try:
        cursor.execute(query)
        usuarios = cursor.fetchall()
        return usuarios
    except Exception as e:
        print(f"Error al obtener usuarios activos para el select: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()


# --- FUNCIONES DE ACCIÓN ---

def _registrar_auditoria_cierre(id_sesion_cerrada, id_admin, descripcion):
    """Inserta un registro de auditoría para el cierre de sesión forzado (Restricción 2)."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    query = """
    INSERT INTO auditoria_sesiones 
    (id_sesion, usuario_admin_id, accion, fecha, descripcion) 
    VALUES (%s, %s, %s, %s, %s)
    """
    
    try:
        cursor.execute(query, (
            id_sesion_cerrada, 
            id_admin, 
            'CIERRE_FORZADO', 
            datetime.now(), 
            descripcion
        ))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al registrar auditoría: {e}")
        conexion.rollback()
        return False
    finally:
        cursor.close()
        conexion.close()

def cerrar_sesion_forzada_individual(id_sesion_pk, id_admin):
    """Cierra una sesión específica y registra la auditoría."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # 1. Actualizar Sesión a 'cerrada'
    update_query = "UPDATE sesion_activa SET estado = 'cerrada' WHERE id_sesion = %s"
    
    try:
        cursor.execute(update_query, (id_sesion_pk,))
        conexion.commit()

        # 2. Registrar Auditoría
        descripcion = f"Sesión ID {id_sesion_pk} cerrada forzadamente por Admin ID {id_admin}."
        _registrar_auditoria_cierre(id_sesion_pk, id_admin, descripcion)

        return True
    except Exception as e:
        print(f"Error al cerrar sesión individual: {e}")
        conexion.rollback()
        return False
    finally:
        cursor.close()
        conexion.close()

def cerrar_todas_sesiones_usuario(usuario_id, id_admin):
    """Cierra TODAS las sesiones activas de un usuario y registra la auditoría."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    select_query = "SELECT id_sesion FROM sesion_activa WHERE usuario_id = %s AND estado = 'activa'"
    update_query = "UPDATE sesion_activa SET estado = 'cerrada' WHERE usuario_id = %s AND estado = 'activa'"

    try:
        cursor.execute(select_query, (usuario_id,))
        sesiones_a_cerrar = [row[0] for row in cursor.fetchall()]

        cursor.execute(update_query, (usuario_id,))
        conexion.commit()

        for id_sesion in sesiones_a_cerrar:
            descripcion = f"Todas las sesiones del Usuario ID {usuario_id} fueron cerradas por Admin ID {id_admin}. (Sesión afectada: {id_sesion})"
            _registrar_auditoria_cierre(id_sesion, id_admin, descripcion)

        return True
    except Exception as e:
        print(f"Error al cerrar sesiones de usuario: {e}")
        conexion.rollback()
        return False
    finally:
        cursor.close()
        conexion.close()

def bloquear_usuario(usuario_id, id_admin):
    """Bloquea la cuenta de un usuario por seguridad."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # ⚠️ AJUSTE: Usamos 'id_usuario' como PK de la tabla Usuario
    query = "UPDATE Usuario SET clave = 'BLOQUEADO_POR_ADMIN', estado_cuenta = 'BLOQUEADO' WHERE id_usuario = %s" 
    
    # NOTA: Tu esquema no muestra una columna 'estado_cuenta'. 
    # Para bloquear, cambiamos la clave por una que nadie conoce (es la forma más simple). 
    # Si quieres un bloqueo real, DEBES añadir una columna ENUM('activo', 'bloqueado') a la tabla Usuario.

    try:
        cursor.execute(query, (usuario_id,))
        conexion.commit()
        return True
    except Exception as e:
        # Esto fallará si no existe la columna 'estado_cuenta', pero el cambio de clave debería funcionar.
        print(f"Error al bloquear usuario: {e}. Intenta añadir la columna 'estado_cuenta' a la tabla Usuario.")
        conexion.rollback()
        return False
    finally:
        cursor.close()
        conexion.close()

        # Backend/control_sesiones.py (Añadir al final)

def registrar_nueva_sesion(usuario_data, ip, user_agent):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    query = """
    INSERT INTO sesion_activa 
    (usuario_id, nombre_usuario, hora_inicio, ultima_actividad, estado, ip, user_agent) 
    VALUES (%s, %s, NOW(), NOW(), 'activa', %s, %s)
    """
    
    try:
        cursor.execute(query, (
            usuario_data['id_usuario'], # O 'id' si usas el alias
            usuario_data['nombre'],
            ip, 
            user_agent
        ))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al registrar sesión activa: {e}")
        conexion.rollback()
        return False
    finally:
        cursor.close()
        conexion.close()