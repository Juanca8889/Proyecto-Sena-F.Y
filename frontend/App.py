from flask import Flask, render_template, request, redirect, url_for, session
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#Imports de base de datso y backend
from BD.conexion import  ConexionUsuario, verificar_usuario
from Backend.Clientes import  ConexionClientes


app = Flask(__name__)
app.secret_key = 'wjson'

#login y registro

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
        return 

        return redirect(url_for('login'))

    return render_template('register.html')

#rutas de admin y empleado vistas de los menu inicialmente

@app.route('/Admin')
def home():
    return render_template('index.html')

@app.route('/Empleado')
def Empleado():
    return render_template('empleado.html')

#rutas de gestion de clientes

@app.route("/clientes")
def mostrar_clientes():
    orden = request.args.get("orden", None)  
    
    conexion = ConexionClientes()
    clientes = conexion.mostrar_clientes(orden)
    conexion.cerrar()

    return render_template("Gestion_clientes.html", usuarios=clientes)


@app.route("/eliminar_cliente/<int:id_cliente>", methods=["POST"])
def eliminar_cliente(id_cliente):
    conexion = ConexionClientes()
    conexion.cerrar()
    return redirect(url_for("mostrar_clientes"))

@app.route("/editar_cliente/<int:id_cliente>", methods=["GET", "POST"])
def editar_cliente(id_cliente):
    conexion = ConexionClientes()
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        celular = request.form["celular"]
        conexion.actualizar_usuario(id_cliente, nombre, correo, celular)
        conexion.cerrar()
        return redirect(url_for("mostrar_clientes"))
    else:
        cliente = conexion.obtener_usuario(id_cliente)
        conexion.cerrar()
        return render_template("editar_cliente.html", cliente=cliente)



#para correr la app

if __name__ == '__main__':
    app.run(debug=True)