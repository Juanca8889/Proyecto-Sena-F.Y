# ==========================================
# IMPORTACIÓN DE MÓDULOS NECESARIOS
# ==========================================
import sys
import os

# Ajustamos el path para importar desde Backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Backend')))
# Aseguramos también la raíz del proyecto para BD/
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from flask import Flask, render_template, request, redirect, url_for, flash

# Importamos la lógica de negocio
from pedido_compra import GestorCompras
from stock_inicial import GestorStock
from cliente_domicilio import Cliente   # 🔹 CORREGIDO
from dashboard import dashboard_bp

# ==========================================
# CONFIGURACIÓN DE FLASK
# ==========================================
app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "clave_secreta"

# Instancias de gestores
gestor_compras = GestorCompras()
gestor_stock = GestorStock()
gestor_clientes = Cliente()
app.register_blueprint(dashboard_bp)   # 🔹 CORREGIDO


# ==========================================
# RUTA PRINCIPAL - PEDIDO DE COMPRA
# ==========================================
@app.route("/")
def index():
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
@app.route("/realizar_pedido", endpoint="realizar_pedido" methods=["GET", "POST"])
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

        return redirect(url_for("index"))

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
@app.route("/ver_pedidos")
def ver_pedidos():
    pedidos = gestor_compras.obtener_pedidos()
    return render_template("pedido_compra.html", vista="ver_pedidos", pedidos=pedidos)


# ==========================================
# RUTA: CONTROL DE STOCK
# ==========================================
@app.route("/control_stock")
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
@app.route("/stock_inicial", methods=["GET", "POST"])
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
@app.route("/crear_referencia", methods=["GET", "POST"])
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
@app.route("/notificaciones")
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

@app.route('/form_cliente')
def form_cliente():
    return render_template("form_cliente.html")

@app.route('/guardar_cliente', methods=['POST'])
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
# INICIAR LA APLICACIÓN
# ==========================================
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
