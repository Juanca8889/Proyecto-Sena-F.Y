from flask import Flask
from app import app


# Crear la app
app = Flask(__name__)
app.secret_key = "mi_clave_secreta"  # necesario para sesiones

# Importar rutas y modelos para que Flask los conozca
from app import app


