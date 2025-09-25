from flask import Flask, render_template, request, redirect, url_for, session, flash
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Imports de base de datos y backend
from BD.conexion import verificar_usuario, conectar
from Backend.Clientes import ConexionClientes  # se mantiene si sigues usando la vista de gestión masiva
from Backend.Usuario import ConexionUsuario
from Backend.pedido_compra import GestorCompras
from Backend.stock_inicial import GestorStock
from Backend.cliente_domicilio import Cliente
from Backend.dashboard import dashboard_bp

app = Flask(__name__)
app.secret_key = 'wjson'  # En prod: usa variable de entorno

# Instancias de gestores principales
gestor_compras = GestorCompras()
gestor_stock = GestorStock()
app.register_blueprint(dashboard_bp)

# ------------------------------------------
# Helper global: URL del menú según la sesión
# ------------------------------------------
def _menu_url() -> str:
    """
    Devuelve la URL del menú adecuado según el rol en sesión:
      - admin si rol == 1
      - empleado si hay otro rol
      - login si no hay sesión
    """
    destino = 'admin' if session.get('rol') == 1 else ('empleado' if session.get('rol') else 'login')
    return url_for(destino)

@app.context_processor
def inject_menu_url():
    """
    Inyecta menu_url en todas las plantillas para poder usar
    <a href="{{ menu_url }}">Volver</a> sin tener que pasarlo siempre.
    """
    try:
        return {"menu_url": _menu_url()}
    except Exception:
        # En casos sin contexto de solicitud, evita romper.
        return {}

# ==========================================
# HEALTH CHECK E INICIO
# ==========================================
@app.route("/healthz")
def healthz():
    return {"status": "ok"}, 200

@app.route("/")
def root():
    # Redirige según sesión
    if session.get("rol") == 1:
        return redirect(url_for("admin"))
    if session.get("rol"):
        return redirect(url_for("empleado"))
    return redirect(url_for("login"))

# ==========================================
# RUTA PRINCIPAL - PEDIDO DE COMPRA
# ==========================================
@app.route("/pedido_compra")
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
        filtro=filtro,
        menu_url=_menu_url(),  # para la flecha Volver
    )

# ==========================================
# RUTA: FORMULARIO PARA REALIZAR PEDIDO
# ==========================================
@app.route("/realizar_pedido", methods=["GET", "POST"], endpoint="realizar_pedido")
def realizar_pedido():
    if request.method == "POST":
        # Validación robusta de entrada
        try:
            id_proveedor = int(request.form.get("id_proveedor", "0"))
            id_producto = int(request.form.get("id_producto", "0"))
            cantidad = int(request.form.get("cantidad", "0"))
        except (TypeError, ValueError):
            flash("❌ Datos inválidos en el formulario de pedido.", "danger")
            return redirect(url_for("pedido_compra"))

        descripcion = (request.form.get("descripcion") or "").strip()
        fecha_entrega = (request.form.get("fecha_entrega") or "").strip()

        if id_proveedor <= 0 or id_producto <= 0 or cantidad <= 0 or not fecha_entrega:
            flash("❌ Completa todos los campos obligatorios correctamente.", "warning")
            return redirect(url_for("pedido_compra"))

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
        proveedores=proveedores,
        menu_url=_menu_url(),  # para la flecha Volver
    )

# ==========================================
# RUTA: VER TODOS LOS PEDIDOS
# ==========================================
@app.route("/ver_pedidos", endpoint="ver_pedidos")
def ver_pedidos():
    pedidos = gestor_compras.obtener_pedidos()
    return render_template(
        "pedido_compra.html",
        vista="ver_pedidos",
        pedidos=pedidos,
        menu_url=_menu_url(),  # para la flecha Volver
    )

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
        notificaciones=sugerencias,
        menu_url=_menu_url(),  # para la flecha Volver (si el template la incluye)
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

    return render_template("crear_referencia.html", menu_url=_menu_url())

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
        productos_recientes=productos_recientes,
        menu_url=_menu_url(),
    )

# ==========================================
# RUTAS DE CLIENTES A DOMICILIO (DAO robusto)
# ==========================================
@app.route('/clientes_domicilio', endpoint='listar_clientes')
def listar_clientes():
    cliente = Cliente()
    clientes = cliente.listar_clientes()
    cliente.cerrar()
    # Destino: Admin si rol==1, Empleado si hay otro rol, y Login si no hay sesión
    destino = 'admin' if session.get('rol') == 1 else ('empleado' if session.get('rol') else 'login')
    return render_template("cliente_domicilio.html", clientes=clientes, menu_url=url_for(destino))

@app.route('/form_cliente', endpoint="form_cliente")
def form_cliente():
    return render_template("form_cliente.html", menu_url=_menu_url())

@app.route('/guardar_cliente', methods=['POST'], endpoint="guardar_cliente")
def guardar_cliente():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    celular = request.form.get('celular') or None
    correo = (request.form.get('correo') or '').strip() or None
    direccion = request.form.get('direccion') or None
    placa = request.form.get('placa') or None
    modelo = request.form.get('modelo') or None

    nuevo_cliente = Cliente(
        nombre=nombre,
        apellido=apellido,
        celular=celular,
        correo=correo,
        direccion=direccion,
        placa=placa,
        modelo=modelo
    )
    ok = nuevo_cliente.registrar_cliente()
    nuevo_cliente.cerrar()

    flash("✅ Cliente registrado correctamente" if ok else "❌ No se pudo registrar el cliente", "success" if ok else "danger")
    return redirect(url_for('clientes_domicilio'))

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
                # La ruta de admin tiene endpoint="admin"
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('empleado'))
        else:
            flash("Usuario o contraseña incorrectos", "danger")

    return render_template('login.html')

@app.route('/olvidaste-contraseña', methods=['GET', 'POST'])
def olvidaste_contraseña():
    if request.method == 'POST':
        email = request.form.get('email')
        flash(f"Se ha enviado un correo para restablecer la contraseña a {email}", "info")
        return redirect(url_for('login'))
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

        flash("Usuario registrado. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# ==========================================
# RUTAS DE ADMIN Y EMPLEADO
# ==========================================
@app.route('/admin', endpoint="admin")
def home():
    return render_template('index.html')

@app.route('/Empleado', endpoint="Empleado")
def empleado():
    return render_template('empleado.html')

# ==========================================
# RUTAS DE GESTIÓN DE CLIENTES (vista general)
# ==========================================
@app.route("/clientes", endpoint="clientes")
def mostrar_clientes():
    orden = request.args.get("orden", None)
    conexion = ConexionClientes()
    clientes = conexion.mostrar_clientes(orden)
    conexion.cerrar()
    return render_template("Gestion_clientes.html", usuarios=clientes, menu_url=_menu_url())

@app.route("/eliminar_cliente/<int:id_cliente>", methods=["POST"], endpoint="eliminar_cliente")
def eliminar_cliente(id_cliente):
    # Usamos el DAO robusto
    cli = Cliente()
    ok = cli.eliminar_cliente(id_cliente)
    cli.cerrar()
    flash("Cliente eliminado" if ok else "No se pudo eliminar el cliente", "success" if ok else "danger")
    return redirect(url_for("clientes"))

@app.route("/editar_cliente/<int:id_cliente>", methods=["GET", "POST"], endpoint="editar_cliente")
def editar_cliente(id_cliente):
    # Usamos el DAO robusto que sí tiene obtener/actualizar
    cli = Cliente()
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form.get("correo")
        celular = request.form.get("celular")
        ok = cli.actualizar_cliente(id_cliente, nombre=nombre, correo=correo, celular=celular)
        cli.cerrar()
        flash("Cliente actualizado" if ok else "No se pudo actualizar el cliente", "success" if ok else "danger")
        return redirect(url_for("clientes"))
    else:
        cliente = cli.obtener_cliente(id_cliente)
        cli.cerrar()
        if not cliente:
            flash("Cliente no encontrado", "warning")
            return redirect(url_for("clientes"))
        return render_template("editar_cliente.html", cliente=cliente, menu_url=_menu_url())

# ==========================================
# RUTAS PARA LA AGENDA DE MANTENIMIENTO
# ==========================================
@app.route('/Agenda', methods=['GET'], endpoint="agenda")
def agenda():
    vista = request.args.get('vista', 'mensual')
    dia_seleccionado = request.args.get('dia')
    dias = range(1, 32) if vista == 'mensual' else range(1, 8)
    return render_template('agenda.html', dias=dias, vista=vista, dia_seleccionado=dia_seleccionado, menu_url=_menu_url())

@app.route('/agregar', methods=['POST'], endpoint="agregar")
def agregar():
    # TODO: implementar persistencia con Backend.Agenda_Mantenimiento si lo habilitas
    dia = request.form.get('dia')
    maquina = request.form.get('maquina')
    personal = request.form.get('personal')
    hora = request.form.get('hora')
    descripcion = request.form.get('descripcion')
    flash("Actividad registrada (demo). Implementa persistencia en Backend.Agenda_Mantenimiento.", "info")
    return redirect(url_for('agenda', vista='mensual'))

# ==========================================
# RUTA DE GESTIÓN DE TICKETS
# ==========================================
@app.route('/gestion_tickets', endpoint="gestion_tickets")
def gestion_tickets():
    return render_template('gestion_tickets.html', menu_url=_menu_url())

@app.route('/gestion_tickets/es', endpoint="gestion_tickets_es")
def gestion_tickets_es():
    return render_template('gestion_tickets_es.html', menu_url=_menu_url())

# ==========================================
# INVENTARIO DE HERRAMIENTAS (protegido)
# ==========================================
# Nota: conectar() retorna una conexión MySQL que NO expone métodos de inventario.
# Protegemos estas rutas para que no revienten si no tienes un DAO específico.
def _inv_has(obj, name):
    return hasattr(obj, name) and callable(getattr(obj, name, None))

@app.route("/inventario_herramientas/")
def inventario():
    db = conectar()
    if not _inv_has(db, "get_herramientas"):
        flash("Módulo de inventario no implementado en la conexión actual.", "warning")
        return render_template("inventario_herramientas.html", herramientas=[], menu_url=_menu_url())
    herramientas = db.get_herramientas()
    return render_template("inventario_herramientas.html", herramientas=herramientas, menu_url=_menu_url())

@app.route("/registrar_herramienta", methods=["POST"])
def registrar_herramienta():
    db = conectar()
    if not _inv_has(db, "registrar_herramienta"):
        flash("No está disponible el registro de herramientas en este entorno.", "warning")
        return redirect(url_for("inventario"))
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    codigo = request.form["codigo"]
    cantidad = request.form["cantidad"]
    ok, msg = db.registrar_herramienta(nombre, descripcion, codigo, cantidad)
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("inventario"))

@app.route("/retiro", methods=["POST"])
def retiro():
    db = conectar()
    if not _inv_has(db, "retirar_herramienta"):
        flash("No está disponible el retiro de herramientas en este entorno.", "warning")
        return redirect(url_for("inventario"))
    codigo = request.form["codigo"]
    cantidad = int(request.form["cantidad"])
    usuario = request.form["usuario"]
    fecha = request.form["fecha"]
    ok, msg = db.retirar_herramienta(codigo, cantidad, usuario, fecha)
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("inventario"))

@app.route("/reintegro", methods=["POST"])
def reintegro():
    db = conectar()
    if not _inv_has(db, "reintegrar_herramienta"):
        flash("No está disponible el reintegro de herramientas en este entorno.", "warning")
        return redirect(url_for("inventario"))
    codigo = request.form["codigo"]
    cantidad = int(request.form["cantidad"])
    usuario = request.form["usuario"]
    ok, msg = db.reintegrar_herramienta(codigo, cantidad, usuario)
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("inventario"))

@app.route("/salida_inventario")
def salida_inventario():
    db = conectar()
    if not _inv_has(db, "get_salidas"):
        flash("No está disponible la salida de inventario en este entorno.", "warning")
        return render_template("salida_inventario.html", salidas=[], menu_url=_menu_url())
    salidas = db.get_salidas()
    return render_template("salida_inventario.html", salidas=salidas, menu_url=_menu_url())

@app.route("/registrar_salida", methods=["POST"])
def registrar_salida():
    db = conectar()
    if not _inv_has(db, "registrar_salida"):
        flash("No está disponible el registro de salidas en este entorno.", "warning")
        return redirect(url_for("salida_inventario"))
    fecha = request.form["fecha"]
    codigo = request.form["codigo"]
    nombre = request.form["nombre"]
    cantidad = request.form["cantidad"]
    motivo = request.form["motivo"]
    responsable = request.form["responsable"]
    ok, msg = db.registrar_salida(fecha, codigo, nombre, cantidad, motivo, responsable)
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("salida_inventario"))

# ==========================================
# INICIO DE APP
# ==========================================
if __name__ == '__main__':
    app.run(debug=True)