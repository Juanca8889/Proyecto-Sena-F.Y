from flask import Flask, render_template, request, redirect, url_for
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Backend')))
from pedido_compra import GestorCompras

app = Flask(__name__, static_folder='static', template_folder='templates')

gestor = GestorCompras()

@app.route('/')
def index():
    filtro = request.args.get('filtro', 'MAS VENDIDO')

    cursor = gestor.conexion_bd.conexion.cursor()

    query_base = """
    SELECT p.id_producto, p.nombre, p.descripcion, p.cantidad, p.precio, IFNULL(SUM(dv.cantidad), 0) AS vendidos
    FROM producto p
    LEFT JOIN detalleventa dv ON p.id_producto = dv.producto_id
    GROUP BY p.id_producto, p.nombre, p.descripcion, p.cantidad, p.precio
    """

    if filtro == 'MENOR CANTIDAD':
        query = query_base + " ORDER BY p.cantidad ASC"
    elif filtro == 'MAYOR CANTIDAD':
        query = query_base + " ORDER BY p.cantidad DESC"
    else:
        query = query_base + " ORDER BY vendidos DESC"

    cursor.execute(query)
    productos = cursor.fetchall()

    cursor.execute("SELECT id_proveedor, nombre FROM proveedor")
    proveedores = cursor.fetchall()

    sugerencias = gestor.sugerir_pedido_y_alertar()

    return render_template('pedido_compra.html', 
                           vista='lista_materiales', 
                           productos=productos, 
                           proveedores=proveedores, 
                           sugerencias=sugerencias,
                           filtro=filtro)

@app.route('/realizar_pedido', methods=['GET', 'POST'])
def realizar_pedido():
    cursor = gestor.conexion_bd.conexion.cursor()
    
    cursor.execute("SELECT id_proveedor, nombre FROM proveedor")
    proveedores = cursor.fetchall()
    
    cursor.execute("SELECT id_producto, nombre FROM producto")
    productos = cursor.fetchall()

    if request.method == 'POST':
        id_proveedor = int(request.form['id_proveedor'])
        id_producto = int(request.form['id_producto'])
        cantidad = int(request.form['cantidad'])
        fecha_entrega = request.form['fecha_entrega']
        descripcion = request.form.get('descripcion', '')  

        gestor.realizar_pedido(id_proveedor, id_producto, descripcion, cantidad, fecha_entrega)
        return redirect(url_for('index'))

    return render_template('pedido_compra.html', 
                           vista='form_pedido', 
                           proveedores=proveedores,
                           productos=productos)

@app.route('/ver_pedidos')
def ver_pedidos():
    cursor = gestor.conexion_bd.conexion.cursor()
    query = """
        SELECT c.id_compra, p.nombre AS proveedor_nombre, pr.nombre AS producto_nombre, c.descripcion, c.cantidad, c.fecha_pedido, c.fecha_entrega
        FROM compra c
        JOIN proveedor p ON c.proveedor_id = p.id_proveedor
        JOIN producto pr ON c.producto_id = pr.id_producto
        ORDER BY c.fecha_pedido DESC
        """

    cursor.execute(query)
    pedidos = cursor.fetchall()
    return render_template('pedido_compra.html', vista='ver_pedidos', pedidos=pedidos)

if __name__ == '__main__':
    app.run(debug=True)
