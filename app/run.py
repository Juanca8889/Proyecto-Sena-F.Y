from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import os
import sys

# ==========================================
# 1. SETUP DE RUTAS Y PATHS (IMPORTACIONES)
# ==========================================
# Esto asegura que los módulos en Backend y BD sean accesibles
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Importa el Blueprint único desde el archivo de rutas
from routes import routes_bp
# Importa el Blueprint del dashboard (si es que existe y usa Blueprint)
from Backend.dashboard import dashboard_bp 

# ==========================================
# 2. INICIALIZACIÓN DE LA APLICACIÓN
# ==========================================
# Esta variable 'app' es la que Gunicorn buscará y ejecutará.
app = Flask(__name__)
# ¡CRÍTICO PARA PRODUCCIÓN!: Usa una variable de entorno para el secreto.
# En Render, debes configurar la variable 'SECRET_KEY'.
app.secret_key = os.environ.get('SECRET_KEY', 'default-key-dev-only')


# ==========================================
# 3. DECORADORES Y HELPERS GLOBALES
# ==========================================
# Estos son tus helpers y decoradores, mantenidos aquí porque dependen de 'session', 'flash', y 'url_for'.

# DECORADOR: login_required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_usuario' not in session:
            flash("Necesitas iniciar sesión para acceder.", "warning")
            # Redirige a la ruta de login dentro del Blueprint 'auth' (en routes.py)
            return redirect(url_for('auth.login')) 
        return f(*args, **kwargs)
    return decorated_function

# HELPER: is_admin
def is_admin():
    return session.get("rol") == 1

# DECORADOR: admin_required
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin():
            flash("Acceso denegado: solo para administradores.", "danger")
            return redirect(url_for('auth.root')) # Redirige a la raíz del Blueprint
        return f(*args, **kwargs)
    return decorated_function

# HELPER: _menu_url
def _menu_url():
    # Asume que las rutas 'admin' y 'empleado' están en el Blueprint 'auth'
    if session.get("rol") == 1:
        return url_for("auth.admin") 
    else:
        return url_for("auth.empleado")

# Context Processor: Hace _menu_url accesible en todas las plantillas
@app.context_processor
def inject_menu_url():
    return dict(menu_url=_menu_url)


# ==========================================
# 4. REGISTRO DE BLUEPRINTS
# ==========================================
# Aquí enlazamos tu archivo routes.py (como Blueprint) a la aplicación principal
app.register_blueprint(routes_bp)
app.register_blueprint(dashboard_bp) 

# ==========================================
# 5. RUTAS BÁSICAS Y ERRORES
# ==========================================
# Estas rutas son mínimas, solo redirecciones o pruebas.
@app.route('/check')
def check():
    # Ruta de prueba de sesión
    return str(session)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return "Página no encontrada. Verifica la URL.", 404


# ==========================================
# 6. INICIO (SOLO PARA DESARROLLO LOCAL)
# ==========================================
# ESTE BLOQUE ES IGNORADO POR GUNICORN/RENDER, pero es necesario para probar en tu máquina.
if __name__ == '__main__':
    # Configura para entorno de desarrollo local
    app.run(debug=True, host='0.0.0.0', port=5000)