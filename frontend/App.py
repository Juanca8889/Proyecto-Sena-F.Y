from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
import sys
import os
import pandas as pd
from fpdf import FPDF
from functools import wraps
from datetime import date, datetime,timedelta




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
from Backend.Recuperacion_contraseña import recuperacion_contraseña
from Backend.Recuperacion_contraseña import  actualizar_contrasena_usuario 
from Backend.Encuestas import Encuestas
from Backend.inventario_herramientas import Herramientas
from Backend.salida_inventario import Venta
from Backend.Tickets import Tickets
from Backend.ordenes import Servicio
from Backend.domicilio import Domicilio
from Backend.busqueda import BusquedaInventario
from Backend.Guardar_material import Guardar_material
from Backend.devoluciones import Devolucion
from Backend.proveedores import ConexionProveedor 
from Backend.material import ConexionMaterial
from Backend.Agenda_Mantenimiento import Agenda 
from Backend.maquinaria import ConexionMaquinaria

from Backend.control_sesiones import (
    obtener_todas_sesiones_activas, 
    obtener_usuarios_con_sesiones,
    cerrar_sesion_forzada_individual,
    cerrar_todas_sesiones_usuario,
    bloquear_usuario, 
    registrar_nueva_sesion
)

app = Flask(__name__)
app.secret_key = 'wjson'  

gestor_compras = GestorCompras()
gestor_stock = GestorStock()
app.register_blueprint(dashboard_bp)




# ==========================================
# LÓGICA DE SEGURIDAD Y ROLES
# ==========================================
def get_current_admin_id():
    """Obtiene el ID del usuario logueado (necesario para auditoría)."""
    return session.get('usuario_id', 0) 

def is_admin():
    """Verifica si el usuario logueado tiene el rol de administrador (rol_id = 1)."""
    return session.get('rol') == 1

def admin_required(f):
    """Decorador para restringir el acceso solo a administradores (Restricción 1)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin():
            flash("Acceso denegado: Se requiere rol de Administrador.", "danger")
            return redirect(url_for('admin' if session.get('rol') else 'login')) 
        return f(*args, **kwargs)
    return decorated_function


# ------------------------------------------
# Helper global: URL del menú según la sesión
# ------------------------------------------
def _menu_url() -> str:
    destino = 'admin' if session.get('rol') == 1 else ('empleado' if session.get('rol') else 'login')
    return url_for(destino)

@app.context_processor
def inject_menu_url():
    try:
        return {"menu_url": _menu_url()}
    except Exception:
        
        return {}


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
    
    if is_admin():
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
    else:
        filtro = request.args.get("filtro", "MAS VENDIDO")
        productos = gestor_compras.obtener_productos(filtro)
        proveedores = gestor_compras.obtener_proveedores()
        sugerencias = gestor_compras.sugerir_pedido_y_alertar()

        return render_template(
            "pedido_compra (EMPLEADO).html",
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
# RUTA: NOTIFICACIONES 
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
# RUTAS DE CLIENTES A DOMICILIO 
# ==========================================


@app.route('/domicilios', methods=['GET', 'POST'])
def domicilios():
    if 'id_usuario' not in session:
        flash("Debes iniciar sesión primero.", "error")
        return redirect(url_for('login'))

    conexion = conectar()
    domicilio_model = Domicilio(conexion)

    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        servicio_id = request.form['servicio_id']
        fecha = request.form['fecha']
        monto = request.form['monto']
        usuario_id = session['id_usuario']

        domicilio_model.registrar(cliente_id, servicio_id, fecha, monto, usuario_id)
        flash("Domicilio registrado exitosamente", "success")
        return redirect(url_for('domicilios'))

    domicilios = domicilio_model.obtener_todos()

    # Para los select del formulario
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id_cliente, nombre FROM cliente")
    clientes = cursor.fetchall()
    cursor.execute("SELECT id_servicio, descripcion FROM servicio")
    servicios = cursor.fetchall()
    cursor.close()

    return render_template('cliente_domicilio.html', domicilios=domicilios, clientes=clientes, servicios=servicios)




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
    return redirect(url_for('clientes'))

# ==========================================
# LOGIN 
# ==========================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        usuario = verificar_usuario(username, password)

        if usuario:
            session['id_usuario'] = usuario['id_usuario']
            session['usuario'] = usuario['nombre']
            session['rol'] = usuario['rol_id']

            if usuario['rol_id'] == 1:
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
        
        recuperacion = recuperacion_contraseña(email)
        
        recuperacion.enviar_correo_verificacion()
        
        flash(f"Se ha enviado un correo para restablecer la contraseña a {email}", "info")
        return redirect(url_for('login'))
    return render_template('olvidaste_contraseña.html')

# -----------------------
# Recupeacion de contraseña
# -----------------------

@app.route("/recuperar_contraseña", methods=["GET", "POST"])
def recuperar_contraseña():
    if request.method == "POST":
        nombre = request.form.get("usuario")
        celular = request.form.get("celular")
        nueva_contrasena = request.form.get("new-password")

        if not nombre or not celular or not nueva_contrasena:
            flash("Por favor, complete todos los campos.", "warning")
            return redirect(url_for("recuperar_contraseña"))

        resultado = actualizar_contrasena_usuario(nombre, celular, nueva_contrasena)

        if resultado:
            flash("Contraseña actualizada correctamente.", "success")
            return redirect(url_for("login"))
        else:
            flash("Usuario o celular incorrecto.", "danger")
            return redirect(url_for("recuperar_contraseña"))

    return render_template("Recuperacion_contraseña.html")
        
# -----------------------
# REGISTRO DE USUARIO
# -----------------------

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

@app.route('/empleado')
def empleado():
    return render_template('empleado.html')

# ==========================================
# RUTAS DE GESTIÓN DE CLIENTES camilo
# ==========================================
@app.route("/clientes", endpoint="clientes")
def mostrar_clientes():
    orden = request.args.get("orden", None)
    conexion = ConexionClientes()
    clientes = conexion.mostrar_clientes(orden)
    conexion.cerrar()
    return render_template("Gestion_clientes.html", usuarios=clientes, menu_url=_menu_url())

@app.route("/enviar-encuesta", methods=["POST"])
def enviar_encuesta():
    correo = request.form.get("correo")
    encuesta = Encuestas(correo)
    encuesta.enviar_correo()
    if not correo:
        flash("No se encontró el correo del usuario", "error")
    else:
        flash("Encuesta enviada correctamente", "success")
    return redirect(url_for("clientes")) 



# ==========================================
# RUTAS PARA LA AGENDA DE MANTENIMIENTO
# ==========================================
@app.route('/Agenda', methods=['GET'], endpoint="agenda")
def agenda():
    if is_admin():
        vista = request.args.get('vista', 'mensual')
        dia_seleccionado = request.args.get('dia')
        dias = range(1, 32) if vista == 'mensual' else range(1, 8)
        return render_template('agenda.html', dias=dias, vista=vista, dia_seleccionado=dia_seleccionado, menu_url=_menu_url())
    else:
        vista = request.args.get('vista', 'mensual')
        dia_seleccionado = request.args.get('dia')
        dias = range(1, 32) if vista == 'mensual' else range(1, 8)
        return render_template('Agenda (EMPLEADO).html', dias=dias, vista=vista, dia_seleccionado=dia_seleccionado, menu_url=_menu_url())
@app.route('/buscar_maquina')
def buscar_maquina():
    id_maquina = request.args.get('id')
    if not id_maquina:
        return jsonify({"error": "ID no proporcionado"})

    agenda = Agenda()
    maquina = agenda.obtener_maquina(id_maquina)
    agenda.cerrar()

    if not maquina:
        return jsonify({"error": "Máquina no encontrada"})
    
    return jsonify(maquina)



@app.route('/agregar', methods=['POST'])
def agregar():
    dia = request.form.get('dia')
    descripcion = request.form.get('descripcion')
    personal = request.form.get('personal')
    maquina_id = request.form.get('id_maquina')
    usuario_id = 1  # Puedes cambiarlo según el usuario logueado
    costo = request.form.get('costo')

    agenda = Agenda()
    exito = agenda.registrar_mantenimiento(descripcion, personal, dia, maquina_id, usuario_id, costo)
    agenda.cerrar()

    if exito:
        flash("✅ Mantenimiento registrado correctamente", "success")
    else:
        flash("❌ Error al registrar mantenimiento", "error")

    return redirect(url_for('agenda', vista='mensual'))

# ==========================================
# RUTA DE GESTIÓN DE TICKETS
# ==========================================


@app.route('/gestion_tickets', methods=['GET', 'POST'])
def gestion_tickets():
    if request.method == 'POST':
        cuerpo = request.form.get('ticket_Descripcion', '')
        header = request.form.get('ticket_problema', '')
        
        ticket = Tickets(cuerpo, header)
        ticket.enviar_ticket()
        
        return render_template('Gestion_tickets.html', enviado=True)
    
    # Si es GET solo muestra el formulario
    return render_template('Gestion_tickets.html')



# ==========================================
# INVENTARIO DE HERRAMIENTAS 
# ==========================================

@app.route('/agregar_herramienta', methods=['GET', 'POST'])
def agregar_herramienta():
    herramienta = Herramientas()  

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cantidad = int(request.form['cantidad'])
        estado = request.form['estado']
        usuario_id = int(request.form['usuario_id'])

        nueva_herramienta = Herramientas(
            nombre=nombre,
            descripcion=descripcion,
            cantidad=cantidad,
            estado=estado,
            usuario_id=usuario_id
        )
        
        if nueva_herramienta.insertar_herramienta():
            flash("Herramienta registrada correctamente", "success")
            return redirect(url_for('agregar_herramienta'))
            
        else:
            return flash("Error al registrar herramienta", "danger")

    items = herramienta.mostrar_herramientas()
    return render_template('inventario_herramientas.html', items=items)


# ==========================================
# RETIRO DE HERRAMIENTAS 
# ==========================================

@app.route('/retiro_herramienta', methods=['GET', 'POST'])
def retiro_herramienta():
    if request.method == 'POST':
        nombre = request.form['id_herr']
        cantidad_salida = int(request.form['cantidad_salida'])

        herramienta = Herramientas()
        if herramienta.salida(nombre, cantidad_salida):
            herramienta.cerrar()
            flash("Retiro de herramienta registrada correctamente", "success")
            return redirect(url_for('inventario'))
        else:
            herramienta.cerrar()
            return flash("Error al registrar el retiro de la herramienta") 

    return render_template('retiro_herramientas.html')

# ==========================================
# REINTEGRO DE HERRAMIENTAS 
# ==========================================

@app.route('/reintegro', methods=['GET', 'POST'])
def reintegro():
    if request.method == 'POST':
        id_herr = int(request.form['id_herr'])
        cantidad_reintegro = int(request.form['cantidad_reintegro'])

        herramienta = Herramientas()
        if herramienta.reintegro(id_herr, cantidad_reintegro):
            herramienta.cerrar()
            flash("Reintegro de herramienta registrado correctamente", "success")
            return redirect(url_for('inventario'))
        else:
            herramienta.cerrar()
            return flash("Error al registrar el reintegro de la herramienta")

    return render_template('reintegro_herramientas.html')

@app.route('/buscar_herramienta', methods=['GET'])
def buscar_herramienta():
    nombre = request.args.get('nombre', '').strip()  
    herramienta = Herramientas()

    if nombre:
        items = herramienta.buscar_herramienta(nombre)
    else:
        flash("Por favor ingrese un nombre de herramienta para buscar.", "warning")
        items = herramienta.mostrar_herramientas()  

    return render_template('inventario_herramientas.html', items=items)

@app.route('/inventario') 
def inventario(): 
    return render_template('inventario_herramientas.html')



# ==========================================
# SALIDA DE INVENTARIO 
# ==========================================
@app.route('/salida_inventario', methods=['GET'])
def salida_inventario():
    page = int(request.args.get('page', 1))
    filtro = request.args.get('filtro', 'recientes')  # por defecto mostrar recientes
    per_page = 6
    offset = (page - 1) * per_page

    venta = Venta()
    ventas = venta.ver_ventas(limit=per_page, offset=offset, filtro=filtro)
    total = venta.contar_ventas()
    venta.cerrar()

    has_next = total > page * per_page

    return render_template(
        'salida_inventario.html',
        ventas=ventas,
        page=page,
        has_next=has_next,
        filtro=filtro
    )


# ==========================================
# RUTA: Mostrar formulario de venta
# ==========================================
@app.route('/venta', methods=['GET'])
def venta_form():
    return render_template('venta.html')  

# ==========================================
# Registrar la venta en la base de datos
# ==========================================
@app.route('/registrar_venta', methods=['POST'])
def registrar_venta():
    id_producto = int(request.form['id_producto'])
    cliente_id = int(request.form['cliente_id'])
    cantidad = int(request.form['cantidad'])
    encargado_id = int(request.form['encargado_id'])
    garantia = int(request.form['garantia'])
    descripcion = request.form['descripcion']

    venta = Venta()
    
    if venta.registrar_venta(cliente_id, id_producto, cantidad, encargado_id, descripcion, garantia):
        print(garantia)
        venta.cerrar()
        return redirect(url_for('venta_form'))
    else:
        venta.cerrar()
        return "Error al registrar la venta"


# ==========================================
#  Buscar producto 
# ==========================================
@app.route('/buscar_producto/<int:id_producto>', methods=['GET'])
def buscar_producto(id_producto):
    venta = Venta()
    producto = venta.obtener_producto(id_producto)
    venta.cerrar()

    if producto:
        return jsonify(producto)
    else:
        return jsonify({'error': 'Producto no encontrado'})
    
    
# ==========================================
#  Formulario para registrar material
# ==========================================
@app.route('/material_form', methods=['GET'])
def material_form():
    return render_template('Guardar_material.html')  





# ==========================================
#  Registrar material (sumar cantidad)
# ==========================================
@app.route('/registrar_material', methods=['POST'])
def registrar_material():
    id_producto = int(request.form['id_producto'])
    cantidad = int(request.form['cantidad'])

    material = Guardar_material()
    exito = material.sumar_cantidad(id_producto, cantidad)
    material.cerrar()

    if exito:
        flash("Material registrado correctamente", "success")
        return redirect(url_for('material_form'))
    else:
        return flash("Error al registrar el material", "danger")
    







# ==========================================
# Laura
# ==========================================

# -----------------------
# RUTA: REPORTE DE VENTAS
# -----------------------
@app.route("/reporte_ventas" ,methods=["GET"])
def reporte_ventas():
    fecha = request.args.get("fecha")
    orden = request.args.get("orden")

    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    query = """
        SELECT  id_venta, cliente_id, cantidad, descripcion, fecha_venta, encargado_id, monto
        FROM venta where 1=1
        
    """
    valores = []

    # Si hay filtro por fecha
    if fecha:
        query += " AND fecha_venta = %s"
        valores.append(fecha)

    # Ordenar según filtro
    if orden == "recientes":
        query += " ORDER BY fecha_venta DESC"
    elif orden == "antiguos":
        query += " ORDER BY fecha_venta ASC"

    cursor.execute(query, valores)
    ventas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("reporteventas.html", ventas=ventas)




# -----------------------
# EXPORTAR A EXCEL
# -----------------------
# ----------- PÁGINA PRINCIPAL -----------
@app.route("/exportar")
def exportar():
    return render_template("Exportar.html")


# ----------- EXPORTAR INVENTARIO (Excel) -----------
@app.route("/exportar/excel")
def exportar_excel():
    try:
        # Conectar a la BD
        conn = conectar()

        # Leer datos con pandas directamente desde la query
        query = "SELECT * FROM inventarioproductos"
        df = pd.read_sql(query, conn)

        # Guardar como CSV temporal
        archivo_xlsx = "inventario.xlsx"
        df.to_excel(archivo_xlsx, index=False)

        conn.close()

        return send_file(archivo_xlsx, as_attachment=True)
    except Exception as e:
        return f"❌ Error al exportar: {str(e)}"

# ----------- EXPORTAR INVENTARIO (PDF) -----------


@app.route("/exportar/pdf")
def exportar_pdf():
    try:
        # Conectar a la BD
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventarioproductos")
        resultados = cursor.fetchall()

        # Crear el PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)

        # Títulos
        columnas = ["Código", "Producto", "Cantidad", "Categoria", "Rol"]
        for col in columnas:
            pdf.cell(32, 10, col, 1, 0, "C")
        pdf.ln()

        # Datos
        pdf.set_font("Arial", "", 10)
        for fila in resultados:
            for dato in fila:
                pdf.cell(32, 10, str(dato), 1, 0, "C")
            pdf.ln()

        archivo_pdf = "inventario.pdf"
        pdf.output(archivo_pdf)

        # Descargar
        return send_file(archivo_pdf, as_attachment=True)

    except Exception as e:
        return f"❌ Error exportando a PDF: {str(e)}"




# ==========================================
# Importar 
# ==========================================

@app.route('/importar/excel', methods=['GET', 'POST'])
def importar_excel():
    if request.method == 'POST':
        archivo = request.files['archivo']

        if not archivo:
            flash('❌ No se seleccionó ningún archivo', 'error')
            return redirect(request.url)

        try:

            df = pd.read_excel(archivo)

            conn = conectar()
            cursor = conn.cursor()

            for _, fila in df.iterrows():
                query = """
                    INSERT INTO producto (nombre, descripcion, cantidad, categoria_id, precio)
                    VALUES (%s, %s, %s, %s, %s)
                """
                valores = (
                    fila['nombre'],
                    fila['descripcion'],
                    int(fila['cantidad']),
                    int(fila['categoria_id']),
                    float(fila['precio'])
                )
                cursor.execute(query, valores)

            conn.commit()
            cursor.close()
            conn.close()

            flash('✅ Datos importados correctamente desde Excel', 'success')
            return redirect(url_for('importar_excel'))

        except Exception as e:
            flash(f'❌ Error al importar: {str(e)}', 'error')
            return redirect(url_for('importar_excel'))

    return render_template('importar_excel.html')



# -----------------------------------------
# ÓRDENES DE SERVICIO
# -----------------------------------------



@app.route("/ordenes", methods=["GET", "POST"])
def ordenes():
    servicio = Servicio()

    if request.method == "POST":
        descripcion = request.form.get("descripcion")
        tipo = request.form.get("tipo")
        fecha = request.form.get("fecha")
        cliente_id = request.form.get("cliente_id")
        usuario_id = request.form.get("usuario_id")

        nuevo = Servicio(
            descripcion=descripcion,
            tipo=tipo,
            fecha=fecha,
            cliente_id=cliente_id,
            usuario_id=usuario_id
        )

        if nuevo.insertar_servicio():
            nuevo.cerrar()
            flash("✅ Orden de servicio creada correctamente", "success")
            return redirect(url_for("ordenes"))
        
        else:
            flash("❌ Error al crear la orden de servicio", "danger")
            return  redirect(url_for("ordenes"))

    # ------ Filtros (GET) ------
    fecha_filtro = request.args.get("fecha")
    tipo_filtro = request.args.get("tipo")

    servicios = servicio.mostrar_servicios()  # trae todos

    # Filtrar manualmente en Python (suficiente para empezar)
    if fecha_filtro:
        hoy = datetime.today().date()

        if fecha_filtro == "hoy":
            servicios = [s for s in servicios if s["fecha"] == hoy]

        elif fecha_filtro == "ayer":
            ayer = hoy - timedelta(days=1)
            servicios = [s for s in servicios if s["fecha"] == ayer]

        elif fecha_filtro == "7dias":
            limite = hoy - timedelta(days=7)
            servicios = [s for s in servicios if s["fecha"] >= limite]

        elif fecha_filtro == "mes":
            limite = hoy - timedelta(days=30)
            servicios = [s for s in servicios if s["fecha"] >= limite]

    if tipo_filtro:
        servicios = [s for s in servicios if s["tipo"] == tipo_filtro]

    servicio.cerrar()

    return render_template(
        "ordenes.html",
        servicios=servicios,
        fecha=fecha_filtro,
        tipo=tipo_filtro
    )



# -----------------------------------------
# INVENTARIO
# -----------------------------------------
@app.route("/filtro", methods=["GET", "POST"])
def filtro():
    
    if is_admin():
        
        materiales = []
        if request.method == "POST":
            criterio = request.form.get("criterio")
            valor = request.form.get("valor")
            busqueda = BusquedaInventario()
            materiales = busqueda.buscar(**{criterio: valor})
            busqueda.cerrar()
        else:
            conexion = conectar()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM producto")
            materiales = cursor.fetchall()
            cursor.close()
            conexion.close()

        return render_template("inventario.html", materiales=materiales)
    
    else:
        materiales = []
        if request.method == "POST":
            criterio = request.form.get("criterio")
            valor = request.form.get("valor")
            busqueda = BusquedaInventario()
            materiales = busqueda.buscar(**{criterio: valor})
            busqueda.cerrar()
        else:
            conexion = conectar()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM producto")
            materiales = cursor.fetchall()
            cursor.close()
            conexion.close()

        return render_template("inventario (EMPLEADO).html", materiales=materiales)





# ==========================================
# RUTAS DE CONTROL DE SESIONES 
# ==========================================


@app.route('/admin/control_sesiones', methods=['GET'])
@admin_required
def control_sesiones():
    """Ruta para cargar la vista HTML del panel de control."""
    return render_template(
        'control_sesiones.html', 
        menu_url=_menu_url(),
        current_date=datetime.now()
    )

@app.route('/api/sesiones_activas', methods=['GET'])
@admin_required
def api_sesiones_activas():
    """API para el Polling de la tabla principal (Restricción 3)."""
    sesiones = obtener_todas_sesiones_activas()
    
    for sesion in sesiones:
        if isinstance(sesion.get('hora_inicio'), datetime):
            sesion['hora_inicio'] = sesion['hora_inicio'].strftime('%I:%M %p').replace(' 0', ' ').lower()
        
        sesion['es_sospechosa'] = sesion['ip'] in ['0.0.0.0', '127.0.0.1'] 
        
    return jsonify(sesiones)

@app.route('/api/usuarios_activos', methods=['GET'])
@admin_required
def api_usuarios_activos():
    """API para cargar el dropdown de 'Selección de Usuario'."""
    usuarios = obtener_usuarios_con_sesiones()
    return jsonify(usuarios)


@app.route('/admin/cerrar_sesion', methods=['POST'])
@admin_required
def cerrar_sesion_endpoint():
    """Endpoint para el cierre forzado (individual o por usuario_id)."""
    data = request.get_json()
    id_admin = get_current_admin_id()

    if 'id_sesion' in data:
        id_sesion = data['id_sesion']
        if cerrar_sesion_forzada_individual(id_sesion, id_admin):
            return jsonify({'message': 'Sesión individual cerrada con éxito'}), 200
        else:
            return jsonify({'error': 'Error al cerrar sesión individual'}), 500

    elif 'usuario_id' in data:
        usuario_id = data['usuario_id']
        if cerrar_todas_sesiones_usuario(usuario_id, id_admin):
            return jsonify({'message': f'Todas las sesiones del usuario {usuario_id} cerradas con éxito'}), 200
        else:
            return jsonify({'error': 'Error al cerrar todas las sesiones del usuario'}), 500
    
    return jsonify({'error': 'Parámetros inválidos'}), 400


@app.route('/admin/bloquear_usuario', methods=['POST'])
@admin_required
def bloquear_usuario_endpoint():
    """Endpoint para bloquear a un usuario."""
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    id_admin = get_current_admin_id()

    if usuario_id and bloquear_usuario(usuario_id, id_admin):
        return jsonify({'message': 'Usuario bloqueado con éxito'}), 200
    
    return jsonify({'error': 'Error al bloquear el usuario o ID no proporcionado'}), 400




# -----------------------------------------
#  Botón "Volver"
# -----------------------------------------

@app.route('/volver')
def volver():
    rol = session.get('rol', 'login')

    if rol == 1:
        return redirect(url_for('admin'))
    elif rol == 2 or 3:
        return redirect(url_for('empleado'))
    elif rol == 4 or 5:
        return redirect(url_for('empleado'))
    else:
        return redirect(url_for('login'))


# -----------------------------------------
# LAURA
# -----------------------------------------

# -----------------------------
# DEVOLUCION DE MATERIAL
# -----------------------------

@app.route("/devolucion_de_material", methods=["GET", "POST"])
def devoluciones():
    if request.method == "POST":
        compra_id = request.form.get("compra_id")
        razon = request.form.get("razon")
        fecha = date.today().strftime("%Y-%m-%d")
        estado = 1  

        try:
            # Crear instancia de la clase Devolucion
            nueva_devolucion = Devolucion(
                compra_id=compra_id,
                razon=razon,
                estado=estado,
                fecha=fecha
            )

            # Llamar al método que guarda la devolución en BD
            nueva_devolucion.registrar_devolucion()

            flash("✅ Devolución registrada correctamente.", "success")
            return redirect(url_for("devoluciones"))

        except Exception as e:
            print(f"Error al registrar devolución: {e}")
            flash(f"❌ Error al registrar devolución: {e}", "danger")

    return render_template("devolucionmaterial.html")


# -----------------------------
# EDITAR MATERIALES
# -----------------------------
@app.route('/editar_material_form', methods=['GET'])
def editar_material_form():
    return render_template('editar_material.html')


@app.route('/editar_material', methods=['POST'])
def editar_material():
    try:
        id_producto = request.form.get('id_producto')
        nombre = request.form.get('nombre_nuevo')
        descripcion = request.form.get('descripcion_nuevo')
        precio = request.form.get('precio_nuevo')

        # Validaciones rápidas
        if not id_producto or not nombre or not precio:
            return jsonify({"error": "Faltan datos"}), 400

        con = ConexionMaterial()
        actualizado = con.actualizar_material(
            id_producto=int(id_producto),
            nombre_nuevo=nombre,
            descripcion_nueva=descripcion,
            precio_nuevo=float(precio)
        )
        con.cerrar()

        if actualizado:
            return jsonify({"success": True, "message": "Material actualizado correctamente"})
        else:
            return jsonify({"success": False, "message": "No se pudo actualizar el material"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# -----------------------------
# REGISTRAR ADMINISTRAR PROVEEDORES
# -----------------------------
@app.route("/agregar_proveedor", methods=["GET", "POST"])
def agregar_proveedor():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        telefono = request.form.get("telefono")
        correo = request.form.get("correo")

        proveedor = ConexionProveedor(nombre, telefono, correo)
        if proveedor.agregar_proveedor():
            flash("✅ Proveedor agregado correctamente.", "success")
            return render_template("proveedores.html")
        else:
            flash("❌ Error al agregar el proveedor.", "danger")

    return render_template("proveedores.html")

# -----------------------------------------
# exportar ventas a excel
# -----------------------------------------

@app.route("/exportar/ventas/excel")
def exportar_ventas_excel():
    fecha = request.args.get("fecha")
    orden = request.args.get("orden")

    conn = conectar()

    query = """
        SELECT id_venta, cliente_id, cantidad, descripcion, fecha_venta, encargado_id, monto
        FROM venta WHERE 1=1
    """

    valores = []

    if fecha:
        query += " AND fecha_venta = %s"
        valores.append(fecha)

    if orden == "recientes":
        query += " ORDER BY fecha_venta DESC"
    elif orden == "antiguos":
        query += " ORDER BY fecha_venta ASC"

    df = pd.read_sql(query, conn, params=valores)
    conn.close()

    archivo_xlsx = "ventas.xlsx"
    df.to_excel(archivo_xlsx, index=False)

    return send_file(archivo_xlsx, as_attachment=True)



@app.route("/exportar/ventas/pdf")
def exportar_ventas_pdf():
    fecha = request.args.get("fecha")
    orden = request.args.get("orden")

    conn = conectar()
    cursor = conn.cursor()

    query = """
        SELECT id_venta, cliente_id, cantidad, descripcion, fecha_venta, encargado_id, monto
        FROM venta WHERE 1=1
    """

    valores = []

    if fecha:
        query += " AND fecha_venta = %s"
        valores.append(fecha)

    if orden == "recientes":
        query += " ORDER BY fecha_venta DESC"
    elif orden == "antiguos":
        query += " ORDER BY fecha_venta ASC"

    cursor.execute(query, valores)
    ventas = cursor.fetchall()

    cursor.close()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 10)

    columnas = ["ID", "Cliente", "Cantidad", "Descripción", "Fecha", "Encargado", "Monto"]

    for col in columnas:
        pdf.cell(28, 10, col, 1, 0, "C")
    pdf.ln()

    pdf.set_font("Arial", "", 8)

    for fila in ventas:
        for dato in fila:
            pdf.cell(28, 10, str(dato), 1, 0, "C")
        pdf.ln()

    archivo_pdf = "ventas.pdf"
    pdf.output(archivo_pdf)

    return send_file(archivo_pdf, as_attachment=True)



# -----------------------------------------
# Maquinaria
# -----------------------------------------
@app.route('/maquinaria', methods=['GET'])
def maquinaria():
    conexion = ConexionMaquinaria()
    maquinarias = conexion.mostrar_maquinarias()
    conexion.cerrar()
    return render_template('maquinaria.html', maquinarias=maquinarias)

# --- Registrar nueva maquinaria ---
@app.route('/registrar_maquinaria', methods=['GET', 'POST'])
def registrar_maquinaria():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        estado = request.form.get('estado')

        # Validar campos
        if not nombre or not descripcion or not estado:
            flash("Por favor complete todos los campos.", "warning")
            return redirect(url_for('maquinaria'))

        # Guardar en la base de datos
        conexion = ConexionMaquinaria(nombre=nombre, descripcion=descripcion, estado=estado)
        conexion.registrar_maquinaria()
        conexion.cerrar()

        flash("✅ Maquinaria registrada correctamente.", "success")
        return redirect(url_for('maquinaria'))

    # Si se accede por GET, redirigir al listado
    return redirect(url_for('maquinaria'))




# -----------------------------------------
# Mantenimientos vista
# -----------------------------------------

@app.route('/mantenimientos', methods=['GET'])
def mantenimientos():
    agenda = Agenda()

    # Obtener todos los mantenimientos
    mantenimientos = agenda.ver_mantenimientos()
    agenda.cerrar()

    # Parámetros de paginación
    por_pagina = 6   # cantidad de cards por página
    pagina = request.args.get('page', 1, type=int)

    total = len(mantenimientos)
    inicio = (pagina - 1) * por_pagina
    fin = inicio + por_pagina
    mantenimientos_pagina = mantenimientos[inicio:fin]

    # Total de páginas
    total_paginas = (total + por_pagina - 1) // por_pagina

    return render_template(
        'mantenimiento.html',
        mantenimientos=mantenimientos_pagina,
        pagina_actual=pagina,
        total_paginas=total_paginas
    )
# -----------------------------------------
# ERRORES
# -----------------------------------------
@app.errorhandler(404)
def pagina_no_encontrada(error):
    return "Página no encontrada. Verifica la URL.", 404



# ==========================================
# INICIO DE APP
# ==========================================
if __name__ == '__main__':
    app.run(debug=True)