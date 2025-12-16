from flask import Flask, session, flash, redirect, url_for
from functools import wraps
import os
import sys

# ==========================================
# 1. SETUP DE RUTAS Y PATHS
# ==========================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# ==========================================
# 2. INICIALIZACIÓN DE LA APLICACIÓN
# ==========================================
app = Flask(__name__)
# Usar variable de entorno para producción (Render)
app.secret_key = os.environ.get('SECRET_KEY', 'wjson') 

# ==========================================
# 3. DECORADORES Y HELPERS GLOBALES
# ==========================================

# Mantenemos los helpers aquí ya que usan 'session' y 'url_for'

def is_admin():
    """Verifica si el usuario logueado tiene el rol de administrador (rol_id = 1)."""
    return session.get('rol') == 1 #

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_usuario' not in session:
            flash("Debes iniciar sesión para acceder.", "danger")
            # Redirige usando el prefijo 'auth' del Blueprint
            return redirect(url_for('auth.login')) 
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin():
            flash("Acceso denegado: Se requiere rol de Administrador.", "danger")
            # Redirige usando el prefijo 'auth' para la ruta principal
            return redirect(url_for('auth.root')) 
        return f(*args, **kwargs)
    return decorated_function

def _menu_url() -> str:
    """Helper global: URL del menú según la sesión"""
    rol = session.get('rol')
    # Usa el prefijo 'auth' para las rutas del Blueprint
    if rol == 1:
        return url_for('auth.admin')
    elif rol:
        return url_for('auth.empleado')
    return url_for('auth.login')

@app.context_processor
def inject_menu_url():
    # Provee el helper a las plantillas
    return {"menu_url": _menu_url()}

# ==========================================
# 4. REGISTRO DE BLUEPRINTS
# ==========================================

# Importa el Blueprint del dashboard (siempre debe ser un Blueprint)
from Backend.dashboard import dashboard_bp
app.register_blueprint(dashboard_bp) 

# Importa el Blueprint ÚNICO de rutas (que está en routes.py)
from routes import routes_bp
# Registra el Blueprint de rutas con el prefijo 'auth' para que las rutas internas
# como login, admin, pedido_compra, se referencien como 'auth.login', 'auth.admin', etc.
# Si no especificas el 'url_prefix', las rutas quedan en la raíz ('/').
app.register_blueprint(routes_bp)


# ==========================================
# 5. MANEJO DE ERRORES Y PRUEBA
# ==========================================
@app.route('/check')
def check():
    return str(session)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return "Página no encontrada. Verifica la URL.", 404

# ==========================================
# 6. INICIO DE APP
# ==========================================
# Bloque de ejecución solo para desarrollo. Gunicorn lo ignora.
if __name__ == '__main__':
    app.run(debug=True)