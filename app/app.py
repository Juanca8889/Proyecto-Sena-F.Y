from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import os
import sys

# ==========================================
# 1. SETUP DE PATHS (Para encontrar Backend/ y BD/)
# ==========================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# ==========================================
# 2. INICIALIZACIÓN DE LA ÚNICA INSTANCIA DE FLASK
# ==========================================
app = Flask(__name__)
# ¡CRÍTICO!: Usar variable de entorno en producción
app.secret_key = os.environ.get('SECRET_KEY', 'wjson') 

# ==========================================
# 3. LÓGICA DE SEGURIDAD Y ROLES (MOVIDA DE routes.py AQUÍ)
# ==========================================
# Define TODAS las funciones y decoradores aquí.
# ¡Asegúrate de cambiar TODOS los url_for() para usar el prefijo 'auth'!

def is_admin():
    """Verifica si el usuario es administrador."""
    return session.get('rol') == 1

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_usuario' not in session:
            flash("Debes iniciar sesión para acceder.", "danger")
            # CRÍTICO: Usa 'auth.login'
            return redirect(url_for('auth.login')) 
        return f(*args, **kwargs)
    return decorated_function

# ... (Definir admin_required, get_current_admin_id, etc., aquí con el prefijo 'auth') ...

def _menu_url() -> str:
    """Helper global: URL del menú según la sesión."""
    rol = session.get('rol')
    # CRÍTICO: Usa el prefijo 'auth' para las rutas
    destino = 'auth.admin' if rol == 1 else ('auth.empleado' if rol else 'auth.login')
    return url_for(destino)

@app.context_processor
def inject_menu_url():
    try:
        return {"menu_url": _menu_url()}
    except Exception:
        return {}


# ==========================================
# 4. REGISTRO DE BLUEPRINTS
# ==========================================
# Importa y registra los Blueprints.

from routes import routes_bp
from Backend.dashboard import dashboard_bp 

# Registra tu módulo de rutas, usando 'auth' como prefijo para url_for
app.register_blueprint(routes_bp)
app.register_blueprint(dashboard_bp)

# ==========================================
# 5. MANEJO DE ERRORES Y PRUEBA (MANTENER AQUÍ)
# ==========================================
@app.errorhandler(404)
def pagina_no_encontrada(error):
    return "Página no encontrada. Verifica la URL.", 404

# Bloque de ejecución solo para desarrollo.
if __name__ == '__main__':
    app.run(debug=True)