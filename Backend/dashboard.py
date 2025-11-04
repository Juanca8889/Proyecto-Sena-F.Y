import io
import base64
from flask import Blueprint, render_template
import matplotlib.pyplot as plt
import os
import sys
import matplotlib
matplotlib.use('Agg')  # Evita errores GUI en Flask
import matplotlib.pyplot as plt



# Aseguramos importar desde BD/
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from BD.conexion import conectar

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

def query_db(query, params=None):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(query, params or ())
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados

# Función para convertir plot a base64 para embebido HTML
def plot_to_img():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return img_base64

def ventas_por_dia():
    resultados = query_db("""
        SELECT fecha_venta, SUM(monto) AS total_ventas
        FROM venta
        WHERE fecha_venta >= CURDATE() - INTERVAL 7 DAY
        GROUP BY fecha_venta
        ORDER BY fecha_venta ASC
    """)
    fechas = [r['fecha_venta'].strftime("%Y-%m-%d") for r in resultados]
    ventas = [r['total_ventas'] for r in resultados]

    plt.figure(figsize=(8,4))
    plt.plot(fechas, ventas, marker='o', linestyle='-', color='blue')
    plt.title('Ventas Últimos 7 Días')
    plt.xlabel('Fecha')
    plt.ylabel('Ventas (monto)')
    plt.xticks(rotation=45)
    plt.grid(True)
    return plot_to_img()

def ventas_por_semana():
    resultados = query_db("""
        SELECT YEARWEEK(fecha_venta, 1) AS semana, SUM(monto) AS total_ventas
        FROM venta
        WHERE fecha_venta >= CURDATE() - INTERVAL 4 WEEK
        GROUP BY semana
        ORDER BY semana ASC
    """)
    semanas = [str(r['semana']) for r in resultados]
    ventas = [r['total_ventas'] for r in resultados]

    plt.figure(figsize=(8,4))
    plt.bar(semanas, ventas, color='green')
    plt.title('Ventas Últimas 4 Semanas')
    plt.xlabel('Semana (AñoSemana)')
    plt.ylabel('Ventas (monto)')
    plt.grid(axis='y')
    return plot_to_img()

def ventas_por_mes():
    resultados = query_db("""
        SELECT DATE_FORMAT(fecha_venta, '%Y-%m') AS mes, SUM(monto) AS total_ventas
        FROM venta
        WHERE fecha_venta >= CURDATE() - INTERVAL 12 MONTH
        GROUP BY mes
        ORDER BY mes ASC
    """)
    meses = [r['mes'] for r in resultados]
    ventas = [r['total_ventas'] for r in resultados]

    plt.figure(figsize=(10,4))
    plt.plot(meses, ventas, marker='s', linestyle='--', color='orange')
    plt.title('Ventas Últimos 12 Meses')
    plt.xlabel('Mes')
    plt.ylabel('Ventas (monto)')
    plt.xticks(rotation=45)
    plt.grid(True)
    return plot_to_img()

def productos_bajo_stock(umbral=10):
    resultados = query_db("""
        SELECT id_producto, nombre, cantidad
        FROM producto
        WHERE cantidad <= %s
        ORDER BY cantidad ASC
    """, (umbral,))
    # Para mostrar en tabla simple en HTML
    return resultados

def pedidos_activos():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT c.id_compra, c.descripcion, c.cantidad, c.fecha_pedido, c.fecha_entrega,
                   p.nombre AS proveedor_nombre
            FROM compra c
            JOIN proveedor p ON c.proveedor_id = p.id_proveedor
            ORDER BY fecha_pedido DESC
            LIMIT 10
        """)
        resultados = cursor.fetchall()
    except Exception:
        resultados = []
    cursor.close()
    conexion.close()
    return resultados


@dashboard_bp.route('/dashboard')
def dashboard():
    img_ventas_dia = ventas_por_dia()
    img_ventas_semana = ventas_por_semana()
    img_ventas_mes = ventas_por_mes()
    bajo_stock = productos_bajo_stock()
    pedidos = pedidos_activos()

    return render_template('dashboard.html',
                           img_ventas_dia=img_ventas_dia,
                           img_ventas_semana=img_ventas_semana,
                           img_ventas_mes=img_ventas_mes,
                           bajo_stock=bajo_stock,
                           pedidos=pedidos)
