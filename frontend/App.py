from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import sys
import os
import pandas as pd
from fpdf import FPDF

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
from Backend.Recuperacion_contraseña import recuperacion_contraseña
from Backend.Recuperacion_contraseña import  actualizar_contrasena_usuario
from Backend.Encuestas import Encuestas
from Backend.salida_inventario import SalidaInventario
from datetime import date
from Backend.inventario_herramientas import Herramientas

app = Flask(__name__)
app.secret_key = 'wjson'  

gestor_compras = GestorCompras()
gestor_stock = GestorStock()
app.register_blueprint(dashboard_bp)

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
        # En casos sin contexto de solicitud, evita romper.
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
@app.route('/clientes_domicilio')
def listar_clientes():
    cliente = Cliente()
    clientes = cliente.listar_clientes()
    cliente.cerrar()
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
    return redirect(url_for('listar_clientes'))

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
            session['usuario'] = usuario['nombre']
            session['rol'] = usuario['rol_id']

            if usuario['rol_id'] == 1:
                # La ruta de admin tiene endpoint="admin"
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('admin'))
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
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        new_password = request.form.get('new-password')
    
        actualizar_contrasena_usuario(usuario, new_password)
    else:
        pass
    return render_template('Recuperacion_contraseña.html')
        
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

@app.route('/Empleado')
def empleado():
    return render_template('index.html')

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
    return redirect(url_for("clientes"))  # o la ruta de gestión clientes



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


# ==========================================
# INVENTARIO DE HERRAMIENTAS 
# ==========================================

@app.route('/agregar_herramienta', methods=['GET', 'POST'])
def agregar_herramienta():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cantidad = int(request.form['cantidad'])
        estado = request.form['estado']
        usuario_id = int(request.form['usuario_id'])

        herramienta = Herramientas(
            nombre=nombre,
            descripcion=descripcion,
            cantidad=cantidad,
            estado=estado,
            usuario_id=usuario_id
        )
        if herramienta.insertar_herramienta():
            return redirect(url_for('inventario'))
        else:
            return "Error al registrar herramienta"
    
    return render_template('inventario_herramientas.html')

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
            return redirect(url_for('inventario'))
        else:
            herramienta.cerrar()
            return "Error al registrar la salida de la herramienta"

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
            return redirect(url_for('inventario'))
        else:
            herramienta.cerrar()
            return "Error al reintegrar la herramienta"

    return render_template('reintegro_herramientas.html')

# ==========================================
# HERRAMIENTAS 
# ==========================================
@app.route('/inventario')
def inventario():
        return render_template('inventario_herramientas.html')  

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

    # Consulta base: solo transacciones completadas y sin duplicados
    query = """
        SELECT  id_venta, cliente_id, cantidad, descripcion, fecha_venta, encargado_id, monto
        FROM venta
        
    """
    valores = []

    # Si hay filtro por fecha
    if fecha:
        query += " AND fecha = %s"
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


# ----------- IMPORTAR INVENTARIO -----------
@app.route("/importar", methods=["POST"])
def importar():
    archivo = request.files.get("archivo")  # ← más seguro que usar directamente request.files["archivo"]

    if not archivo:
        return "❌ No se ha enviado ningún archivo."

    if archivo.filename.endswith(".csv"):
        df = pd.read_csv(archivo)
        df.to_csv("inventario.csv", index=False)
        return "✅ Inventario importado desde CSV."
    
    if archivo.filename.endswith(".xlsx"):
        df = pd.read_excel(archivo)
        df.to_csv("inventario.csv", index=False)
        return "✅ Inventario importado desde Excel."
    
    return "❌ Formato no válido. Solo se permiten CSV o Excel."


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
        cursor.execute("SELECT id_inve_produ, producto_id, cantidad, categoria_id, rol_id FROM inventarioproductos")
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
# Ceron
# ==========================================

# -----------------------------------------
# REGISTRAR MATERIALESS
# -----------------------------------------
@app.route("/registrar_material", methods=["GET", "POST"])
def registrar_material():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.form.get("nombre")
        codigo = request.form.get("codigo")
        tipo = request.form.get("tipo")
        fecha = request.form.get("fecha")
        descripcion = request.form.get("descripcion")
        cantidad = request.form.get("cantidad")
        precio = request.form.get("precio")

        cursor.execute("""Update  producto set cantidad = sum(cantidad + '%s') where nombre == '%s' and codigo == '%s'""")
        ( cantidad, nombre, codigo,)
        conn.commit()

    cursor.execute("SELECT * FROM InventarioProductos ORDER BY id_inve_produ DESC")
    historial = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("registrarmat.html", historial=historial)


# -----------------------------------------
# ÓRDENES DE SERVICIO
# -----------------------------------------
@app.route("/ordenes", methods=["GET", "POST"])
def ordenes():

    return render_template("ordenes.html")


# -----------------------------------------
# FILTRO DE PRODUCTOS
# -----------------------------------------
@app.route("/filtro", methods=["GET", "POST"])
def filtro():
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




# -----------------------------------------
# CLASE DE BÚSQUEDA
# -----------------------------------------
class BusquedaInventario:
    def __init__(self):
        self.conexion = conectar()
        self.cursor = self.conexion.cursor(dictionary=True)

    def buscar(self, **criterios):
        query = "SELECT * FROM producto WHERE 1=1"
        valores = []
        for campo, valor in criterios.items():
            query += f" AND {campo} LIKE %s"
            valores.append(f"%{valor}%")
        self.cursor.execute(query, valores)
        resultados = self.cursor.fetchall()
        return resultados

    def cerrar(self):
        self.cursor.close()
        self.conexion.close()

# -----------------------------------------
# 🔙 Botón universal de "Volver"
# -----------------------------------------

@app.context_processor
def inject_back_button():
    from flask import request, url_for
    # Si existe una página previa, úsala; si no, vuelve al admin
    prev = request.referrer or url_for('admin')
    return {"back_button_url": prev}


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