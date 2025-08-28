from flask import Flask, render_template, request, redirect, url_for, session
import sys
import os

# Agrega la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BD.conexion import  ConexionUsuario, verificar_usuario

app = Flask(__name__)
app.secret_key = 'wjson'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        

        usuario = verificar_usuario(username, password)  


        if usuario:
            session['usuario'] = usuario['nombre']
            session['rol'] = usuario['rol_id']

            if usuario['rol_id'] == 1:
                return redirect(url_for('home'))
            else:
                return redirect(url_for('Empleado'))
        else:
            return "Usuario o contraseña incorrectos"

    return render_template('login.html')


@app.route('/Admin')
def home():
    return render_template('index.html')

@app.route('/Empleado')
def Empleado():
    return render_template('empleado.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        username = request.form.get('username')
        celular = request.form.get('celular')
        contrasena = request.form.get('password')
        correo = request.form.get('email')

        # Instancia tu clase y registra usuario
        usuario = ConexionUsuario(nombre, apellido,celular,correo,username,contrasena)
        usuario.insertar_usuario()
        usuario.cerrar()

        return redirect(url_for('login'))

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)