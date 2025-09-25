from flask import Flask, render_template, request, redirect, url_for, session, flash
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Imports de base de datos y backend
from BD.conexion import verificar_usuario, conectar
from Backend.Clientes import ConexionClientes
from Backend.Usuario import ConexionUsuario
from Backend.pedido_compra import GestorCompras
from Backend.stock_inicial import GestorStock
from Backend.cliente_domicilio import Cliente
from Backend.dashboard import dashboard_bp

app = Flask(__name__)
app.secret_key = 'wjson'

# Instancias de gestores
gestor_compras = GestorCompras()
gestor_stock = GestorStock()
gestor_clientes = Cliente()
app.register_blueprint(dashboard_bp)

# ==========================================
# RUTA PRINCIPAL - PEDIDO DE COMPRA
# ==========================================
@app.route("/pedidocompra")
def pedido_compra():
    filtro = request.args.get("filtro", "MAS VENDIDO")
    productos = gestor_compras.obtener_productos(filtro)
    proveedores = gestor_compras.obtener_proveedores()
    sugerencias = gestor_compras.sugerir_pedido_y_alertar()

    return render_template(
        "pedido_compra.html",
        vista="lista_materiales",
        productos=productos,
        proveedores=proveedores,
        sugerencias=sugerencias,
        filtro=filtro
    )

# ==========================================
# RUTA: FORMULARIO PARA REALIZAR PEDIDO
# ==========================================
@app.route("/realizar_pedido", methods=["GET", "POST"], endpoint="realizar_pedido")
def realizar_pedido():
    if request.method == "POST":
        id_proveedor = int(request.form["id_proveedor"])
        id_producto = int(request.form["id_producto"])
        cantidad = int(request.form["cantidad"])
        descripcion = request.form.get("descripcion", "")
        fecha_entrega = request.form["fecha_entrega"]

        exito = gestor_compras.realizar_pedido(id_proveedor, id_producto, descripcion, cantidad, fecha_entrega)

        if exito:
            flash("✅ Pedido realizado con éxito", "success")
        else:
            flash("❌ Error al realizar el pedido", "danger")

        return redirect(url_for("pedido_compra"))

    productos = gestor_compras.obtener_productos()
    proveedores = gestor_compras.obtener_proveedores()

    return render_template(
        "pedido_compra.html",
        vista="form_pedido",
        productos=productos,
        proveedores=proveedores
    )

# ==========================================
# RUTA: VER TODOS LOS PEDIDOS
# ==========================================
@app.route("/ver_pedidos", endpoint="ver_pedidos")
def ver_pedidos():
    pedidos = gestor_compras.obtener_pedidos()
    return render_template("pedido_compra.html", vista="ver_pedidos", pedidos=pedidos)

# ==========================================
# RUTA: CONTROL DE STOCK
# ==========================================
@app.route("/control_stock", endpoint="control_stock")
def control_stock():
    filtro_codigo = request.args.get("filtro_codigo", "").strip()
    filtro_nombre = request.args.get("filtro_nombre", "").strip()
    filtro_tipo = request.args.get("filtro_tipo", "").strip()
    filtro_precio = request.args.get("filtro_precio", "").strip()
    filtro_stock = request.args.get("filtro_stock", "").strip()
    filtro_fecha = request.args.get("filtro_fecha", "").strip()

    ordenar_por = request.args.get("ordenar_por", "codigo")
    orden = request.args.get("orden", "asc")
    pagina = int(request.args.get("pagina", 1))
    limite = 20

    productos, total = gestor_stock.obtener_productos_con_filtros(
        filtro_codigo=filtro_codigo,
        filtro_nombre=filtro_nombre,
        filtro_tipo=filtro_tipo,
        filtro_precio=filtro_precio,
        filtro_stock=filtro_stock,
        filtro_fecha=filtro_fecha,
        pagina=pagina,
        limite=limite,
        ordenar_por=ordenar_por,
        orden=orden
    )

    paginas_totales = (total + limite - 1) // limite
    opciones = gestor_stock.obtener_opciones_filtros()
    sugerencias = gestor_compras.sugerir_pedido_y_alertar()

    return render_template(
        "stock_inicial.html",
        productos=productos,
        filtro_codigo=filtro_codigo,
        filtro_nombre=filtro_nombre,
        filtro_tipo=filtro_tipo,
        filtro_precio=filtro_precio,
        filtro_stock=filtro_stock,
        filtro_fecha=filtro_fecha,
        ordenar_por=ordenar_por,
        orden=orden,
        pagina=pagina,
        paginas_totales=paginas_totales,
        opciones=opciones,
        notificaciones=sugerencias
    )

# ==========================================
# RUTA: STOCK INICIAL (ACTUALIZACIÓN)
# ==========================================
@app.route("/stock_inicial", methods=["GET", "POST"], endpoint="stock_inicial")
def stock_inicial():
    if request.method == "POST":
        id_producto_str = request.form.get("id_producto", "")
        cantidad_str = request.form.get("cantidad", "")

        if not id_producto_str or not cantidad_str:
            flash("❌ Por favor completa todos los campos obligatorios.", "danger")
            return redirect(url_for('stock_inicial'))

        try:
            id_producto = int(id_producto_str)
            cantidad = int(cantidad_str)
        except ValueError:
            flash("❌ Los datos ingresados no son válidos.", "danger")
            return redirect(url_for('stock_inicial'))

        exito = gestor_stock.actualizar_stock_inicial(id_producto, cantidad)

        if exito:
            flash("✅ Stock actualizado correctamente", "success")
        else:
            flash("❌ Error al actualizar el stock", "danger")

        return redirect(url_for("control_stock"))

    return redirect(url_for("control_stock"))

# ==========================================
# RUTA: FORMULARIO DE CREAR REFERENCIA
# ==========================================
@app.route("/crear_referencia", methods=["GET", "POST"], endpoint="crear_referencia")
def crear_referencia():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        categoria = request.form.get("categoria", "").strip()
        precio = request.form.get("precio", "0").strip()
        stock = request.form.get("stock", "0").strip()
        descripcion = request.form.get("descripcion", "").strip()

        exito = gestor_stock.crear_producto(nombre, categoria, precio, stock, descripcion)
        if exito:
            flash("✅ Referencia creada", "success")
        else:
            flash("❌ Error al crear la referencia", "danger")
        return redirect(url_for("control_stock"))

    return render_template("crear_referencia.html")

# ==========================================
# RUTA: NOTIFICACIONES (CAMPANA)
# ==========================================
@app.route("/notificaciones", endpoint="notificaciones")
def notificaciones():
    sugerencias = gestor_compras.sugerir_pedido_y_alertar()
    productos_recientes, _ = gestor_stock.obtener_productos_con_filtros(
        pagina=1,
        limite=10,
        ordenar_por="fecha",
        orden="desc"
    )

    return render_template(
        "notificaciones_stock.html",
        sugerencias=sugerencias,
        productos_recientes=productos_recientes
    )

# ==========================================
# RUTAS DE CLIENTES
# ==========================================
@app.route('/clientes_domicilio')
def listar_clientes():
    cliente = Cliente()
    clientes = cliente.listar_clientes()
    cliente.cerrar()
    return render_template("cliente_domicilio.html", clientes=clientes)

@app.route('/form_cliente', endpoint="form_cliente")
def form_cliente():
    return render_template("form_cliente.html")

@app.route('/guardar_cliente', methods=['POST'], endpoint="guardar_cliente")
def guardar_cliente():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    celular = request.form['celular']
    correo = request.form['correo']
    direccion = request.form['direccion']
    placa = request.form['placa']
    modelo = request.form['modelo']

    nuevo_cliente = Cliente(
        nombre=nombre,
        apellido=apellido,
        celular=celular,
        correo=correo,
        direccion=direccion,
        placa=placa,
        modelo=modelo
    )
    nuevo_cliente.registrar_cliente()
    nuevo_cliente.cerrar()

    return redirect(url_for('listar_clientes'))

# ==========================================
# LOGIN Y REGISTRO
# ==========================================
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
                return redirect(url_for('empleado'))
        else:
            return "Usuario o contraseña incorrectos"

    return render_template('login.html')


@app.route('/olvidaste-contraseña', methods=['GET', 'POST'])
def olvidaste_contraseña():
    if request.method == 'POST':
        email = request.form.get('email')
        # Aquí agregas la lógica para recuperación de contraseña
        return "Se ha enviado un correo para restablecer la contraseña a " + email
    return render_template('olvidaste_contraseña.html')


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
        usuario = ConexionUsuario(nombre, apellido, celular, correo, username, contrasena)
        usuario.insertar_usuario()
        usuario.cerrar()

        return redirect(url_for('login'))

    return render_template('register.html')


# ==========================================
# RUTAS DE ADMIN Y EMPLEADO
# ==========================================
@app.route('/Admin', endpoint="home")
def home():
    return render_template('index.html')


@app.route('/Empleado', endpoint="empleado")
def empleado():
    return render_template('empleado.html')

# ==========================================
# RUTAS DE GESTIÓN DE CLIENTES
# ==========================================
@app.route("/clientes", endpoint="clientes")
def mostrar_clientes():
    orden = request.args.get("orden", None)  
    conexion = ConexionClientes()
    clientes = conexion.mostrar_clientes(orden)
    conexion.cerrar()
    return render_template("Gestion_clientes.html", usuarios=clientes)

@app.route("/eliminar_cliente/<int:id_cliente>", methods=["POST"], endpoint="eliminar_cliente")
def eliminar_cliente(id_cliente):
    conexion = ConexionClientes()
    conexion.cerrar()
    return redirect(url_for("clientes"))

@app.route("/editar_cliente/<int:id_cliente>", methods=["GET", "POST"], endpoint="editar_cliente")
def editar_cliente(id_cliente):
    conexion = ConexionClientes()
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        celular = request.form["celular"]
        conexion.actualizar_usuario(id_cliente, nombre, correo, celular)
        conexion.cerrar()
        return redirect(url_for("clientes"))
    else:
        cliente = conexion.obtener_usuario(id_cliente)
        conexion.cerrar()
        return render_template("editar_cliente.html", cliente=cliente)

# ==========================================
# RUTAS PARA LA AGENDA DE MANTENIMIENTO
# ==========================================
@app.route('/Agenda', methods=['GET'], endpoint="agenda")
def agenda():
    vista = request.args.get('vista', 'mensual')
    dia_seleccionado = request.args.get('dia')
    dias = range(1, 32) if vista == 'mensual' else range(1, 8)
    return render_template('agenda.html', dias=dias, vista=vista, dia_seleccionado=dia_seleccionado)

@app.route('/agregar', methods=['POST'], endpoint="agregar")
def agregar():
    dia = request.form.get('dia')
    maquina = request.form.get('maquina')
    personal = request.form.get('personal')
    hora = request.form.get('hora')
    descripcion = request.form.get('descripcion')
    return redirect(url_for('agenda', vista='mensual'))

# ==========================================
# RUTA DE GESTIÓN DE TICKETS
# ==========================================
@app.route('/gestion_tickets', endpoint="gestion_tickets")
def gestion_tickets():
    return render_template('gestion_tickets.html')

@app.route('/gestion_tickets/es', endpoint="gestion_tickets_es")
def gestion_tickets_es():
    return render_template('gestion_tickets_es.html')

# ==========================================
# INICIO DE APP
# ==========================================



db = conectar()


# Página principal
@app.route("/inventario_herramientas/" )
def inventario():
    herramientas = db.get_herramientas()
    return render_template("inventario_herramientas.html", herramientas=herramientas)

# Registrar herramienta
@app.route("/registrar_herramienta", methods=["POST"])
def registrar_herramienta():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    codigo = request.form["codigo"]
    cantidad = request.form["cantidad"]

    ok, msg = db.registrar_herramienta(nombre, descripcion, codigo, cantidad)
    flash(msg, "success" if ok else "error")

    return redirect(url_for("inventario"))

# Retirar herramienta
@app.route("/retiro", methods=["POST"])
def retiro():
    codigo = request.form["codigo"]
    cantidad = int(request.form["cantidad"])
    usuario = request.form["usuario"]
    fecha = request.form["fecha"]

    ok, msg = db.retirar_herramienta(codigo, cantidad, usuario, fecha)
    flash(msg, "success" if ok else "error")
    return redirect(url_for("inventario"))

# Reintegrar herramienta
@app.route("/reintegro", methods=["POST"])
def reintegro():
    codigo = request.form["codigo"]
    cantidad = int(request.form["cantidad"])
    usuario = request.form["usuario"]

    ok, msg = db.reintegrar_herramienta(codigo, cantidad, usuario)
    flash(msg, "success" if ok else "error")
    return redirect(url_for("inventario"))

# Salida inventario
@app.route("/salida_inventario")
def salida_inventario():
    salidas = db.get_salidas()  # asegúrate de definirlo en Database
    return render_template("salida_inventario.html", salidas=salidas)

@app.route("/registrar_salida", methods=["POST"])
def registrar_salida():
    fecha = request.form["fecha"]
    codigo = request.form["codigo"]
    nombre = request.form["nombre"]
    cantidad = request.form["cantidad"]
    motivo = request.form["motivo"]
    responsable = request.form["responsable"]

    ok, msg = db.registrar_salida(fecha, codigo, nombre, cantidad, motivo, responsable)
    flash(msg, "success" if ok else "error")

    return redirect(url_for("salida_inventario"))



# ==========================================
# INICIO DE APP
# ==========================================
if __name__ == '__main__':
    app.run(debug=True)
