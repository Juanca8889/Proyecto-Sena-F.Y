import io
import base64
from flask import Blueprint, render_template
import matplotlib.pyplot as plt
import os
import sys
import matplotlib
matplotlib.use('Agg')  # Evita errores GUI en Flask
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker




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

# Formatear números grandes en el eje Y (20.000 - 1.200.000 - 10.000.000)
def formatear_eje_y():
    plt.gca().yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: format(int(x), ",").replace(",", "."))
    )


def ventas_por_dia():
    resultados = query_db("""
        SELECT fecha_venta, SUM(monto) AS total_ventas
        FROM venta
        WHERE fecha_venta >= CURDATE() - INTERVAL 7 DAY
        GROUP BY fecha_venta
        ORDER BY fecha_venta ASC
    """)
    meses_es = {
    "01": "Enero",
    "02": "Febrero",
    "03": "Marzo",
    "04": "Abril",
    "05": "Mayo",
    "06": "Junio",
    "07": "Julio",
    "08": "Agosto",
    "09": "Septiembre",
    "10": "Octubre",
    "11": "Noviembre",
    "12": "Diciembre"
}


    dias_es = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }

    fechas = []
    ventas = []

    for r in resultados:
        fecha = r["fecha_venta"]
        if not fecha:
            continue  # Evita errores si fecha = NULL

        dia_ing = fecha.strftime('%A')
        dia = dias_es.get(dia_ing, dia_ing)

        fechas.append(f"{dia} {fecha.strftime('%d')}")
        ventas.append(r["total_ventas"])

    plt.figure(figsize=(8,4))
    plt.plot(fechas, ventas, marker='o')
    plt.xticks(rotation=45)
    plt.grid(True)

    formatear_eje_y()
    plt.ylim(20000, 10000000)

    return plot_to_img()




def ventas_por_semana():
    resultados = query_db("""
        SELECT YEARWEEK(fecha_venta, 1) AS semana_id, SUM(monto) AS total_ventas
        FROM venta
        WHERE fecha_venta >= CURDATE() - INTERVAL 4 WEEK
        GROUP BY semana_id
        ORDER BY semana_id ASC
    """)

    semanas = []
    ventas = []

    numero = 1
    for r in resultados:
        semanas.append(f"Semana {numero}")
        ventas.append(r["total_ventas"])
        numero += 1

    plt.figure(figsize=(8,4))
    plt.bar(semanas, ventas)
    plt.title("Ventas por Semana (Últimas 4)")
    plt.xlabel("Semana")
    plt.ylabel("Ventas (monto)")
    plt.grid(axis='y')

    plt.ylim(20000, 10000000)
    formatear_eje_y()

    return plot_to_img()



def productos_bajo_stock(umbral=10):
    resultados = query_db("""
        SELECT id_producto, nombre, cantidad
        FROM producto
        WHERE cantidad <= %s
        ORDER BY cantidad ASC
    """, (umbral,))
    return resultados


def ventas_por_mes():
    resultados = query_db("""
        SELECT DATE_FORMAT(fecha_venta, '%Y-%m') AS mes, SUM(monto) AS total_ventas
        FROM venta
        WHERE fecha_venta >= CURDATE() - INTERVAL 12 MONTH
        GROUP BY mes
        ORDER BY mes ASC
    """)

    meses_es = {
        "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril",
        "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
        "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
    }

    meses = []
    ventas = []

    for r in resultados:
        mes = r["mes"]
        numero = mes.split("-")[1]  # → "01"
        meses.append(meses_es[numero])  # → "Enero"
        ventas.append(r["total_ventas"])

    plt.figure(figsize=(10,4))
    plt.plot(meses, ventas, marker='s', linestyle='--')
    plt.title("Ventas por Mes (Últimos 12 Meses)")
    plt.xlabel("Mes")
    plt.ylabel("Ventas (monto)")
    plt.xticks(rotation=45)
    plt.grid(True)

    plt.ylim(20000, 10000000)
    formatear_eje_y()

    return plot_to_img()

  


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
