import os
import time
import csv

INVENTARIO_FILE = 'inventario.csv'
PEDIDOS_FILE = 'pedidos.csv'
SALES_HISTORY_FILE = 'historial_ventas.csv'

def cargar_inventario():
    inventario = []
    if os.path.exists(INVENTARIO_FILE):
        with open(INVENTARIO_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['stock'] = int(row['stock'])
                row['stock_min'] = int(row['stock_min'])
                row['consumo_historico'] = int(row['consumo_historico'])
                row['precio_unitario_promedio'] = float(row['precio_unitario_promedio'])
                inventario.append(row)
    else:
        inventario = [
            {'id': '001', 'nombre': 'Tornillo M5', 'stock': 50, 'stock_min': 200, 'consumo_historico': 1200, 'precio_unitario_promedio': 0.10},
            {'id': '002', 'nombre': 'Tuerca M5', 'stock': 300, 'stock_min': 150, 'consumo_historico': 1000, 'precio_unitario_promedio': 0.08},
            {'id': '003', 'nombre': 'Arandela Plana', 'stock': 150, 'stock_min': 100, 'consumo_historico': 800, 'precio_unitario_promedio': 0.05},
            {'id': '004', 'nombre': 'Llave Allen 5mm', 'stock': 20, 'stock_min': 30, 'consumo_historico': 50, 'precio_unitario_promedio': 1.50},
            {'id': '005', 'nombre': 'Cable HDMI 1m', 'stock': 120, 'stock_min': 100, 'consumo_historico': 250, 'precio_unitario_promedio': 5.00},
        ]
        guardar_inventario(inventario)
    return inventario

def guardar_inventario(inventario):
    with open(INVENTARIO_FILE, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['id', 'nombre', 'stock', 'stock_min', 'consumo_historico', 'precio_unitario_promedio']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(inventario)

def cargar_pedidos():
    pedidos = []
    if os.path.exists(PEDIDOS_FILE):
        with open(PEDIDOS_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            current_pedido = None
            for row in reader:
                if current_pedido is None or current_pedido['fecha'] != row['fecha']:
                    if current_pedido is not None:
                        pedidos.append(current_pedido)
                    current_pedido = {
                        'fecha': row['fecha'],
                        'responsable': row['responsable'],
                        'items': []
                    }
                item = {
                    'id': row['id'],
                    'nombre': row['nombre'],
                    'cantidad_a_pedir': int(row['cantidad_a_pedir']),
                    'precio_unitario': float(row['precio_unitario']),
                    'precio_total': float(row['precio_total'])
                }
                current_pedido['items'].append(item)
            if current_pedido is not None:
                pedidos.append(current_pedido)
    return pedidos

def guardar_pedido(pedido_nuevo):
    file_exists = os.path.exists(PEDIDOS_FILE)
    with open(PEDIDOS_FILE, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['fecha', 'responsable', 'id', 'nombre', 'cantidad_a_pedir', 'precio_unitario', 'precio_total']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for item in pedido_nuevo['items']:
            writer.writerow({
                'fecha': pedido_nuevo['fecha'],
                'responsable': pedido_nuevo['responsable'],
                'id': item['id'],
                'nombre': item['nombre'],
                'cantidad_a_pedir': item['cantidad_a_pedir'],
                'precio_unitario': item['precio_unitario'],
                'precio_total': item['precio_total']
            })

def cargar_historial_ventas():
    ventas = []
    if os.path.exists(SALES_HISTORY_FILE):
        with open(SALES_HISTORY_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ventas.append(row)
    return ventas

def guardar_venta(venta):
    file_exists = os.path.exists(SALES_HISTORY_FILE)
    with open(SALES_HISTORY_FILE, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['fecha', 'item', 'cantidad']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(venta)

inventario = cargar_inventario()
pedidos_proveedor = cargar_pedidos()
ventas_realizadas = cargar_historial_ventas()

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def verificar_stock_bajo():
    articulos_bajos = [item['nombre'] for item in inventario if item['stock'] < item['stock_min']]
    if articulos_bajos:
        print("\n🚨 ¡ALERTA DE STOCK BAJO! 🚨")
        print("Los siguientes materiales están por debajo de su umbral de reorden:")
        for articulo in articulos_bajos:
            print(f"- {articulo}")
        print("Considera generar un pedido a proveedor.")
        input("Presiona Enter para continuar...")
        return True
    return False

def mostrar_inventario(filtro=None):
    limpiar_pantalla()
    print("--- Inventario de Materiales ---")
    
    if filtro == 'mas_vendidos':
        inventario_filtrado = sorted(inventario, key=lambda x: x['consumo_historico'], reverse=True)
        print("Ordenado por los más vendidos:")
    elif filtro == 'mayor_stock':
        inventario_filtrado = sorted(inventario, key=lambda x: x['stock'], reverse=True)
        print("Ordenado por mayor cantidad en stock:")
    elif filtro == 'menor_stock':
        inventario_filtrado = sorted(inventario, key=lambda x: x['stock'])
        print("Ordenado por menor cantidad en stock:")
    else:
        inventario_filtrado = inventario
        print("Mostrando todos los materiales:")

    print("-" * 70)
    print(f"{'ID':<5}{'Nombre':<20}{'Stock':<10}{'Stock Min':<12}{'Consumo Hist.':<15}")
    print("-" * 70)
    for item in inventario_filtrado:
        print(f"{item['id']:<5}{item['nombre']:<20}{item['stock']:<10}{item['stock_min']:<12}{item['consumo_historico']:<15}")
    print("-" * 70)
    input("\nPresiona Enter para continuar...")

def configurar_umbrales():
    limpiar_pantalla()
    print("--- Configurar Umbrales de Reorden ---")
    print("-" * 50)
    print(f"{'ID':<5}{'Nombre':<20}{'Stock Actual':<15}{'Stock Mínimo':<15}")
    print("-" * 50)
    for item in inventario:
        print(f"{item['id']:<5}{item['nombre']:<20}{item['stock']:<15}{item['stock_min']:<15}")
    print("-" * 50)

    item_id = input("\nIngresa el ID del material a configurar: ")
    item_encontrado = next((item for item in inventario if item['id'] == item_id), None)
    
    if item_encontrado:
        try:
            nuevo_umbral = int(input(f"Ingresa el nuevo umbral para '{item_encontrado['nombre']}': "))
            if nuevo_umbral >= 0:
                item_encontrado['stock_min'] = nuevo_umbral
                guardar_inventario(inventario)
                print(f"Umbral de reorden de '{item_encontrado['nombre']}' actualizado a {nuevo_umbral}.")
            else:
                print("El umbral debe ser un número positivo.")
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número entero.")
    else:
        print(f"No se encontró ningún material con el ID '{item_id}'.")
    input("\nPresiona Enter para continuar...")

def generar_pedido_proveedor():
    limpiar_pantalla()
    print("--- Generar y Enviar Pedido a Proveedor ---")
    responsable = input("Ingresa tu nombre para el registro del pedido: ")
    print("\nAnalizando niveles de stock y consumo histórico...")

    pedido_sugerido = []
    for item in inventario:
        if item['stock'] < item['stock_min']:
            cantidad_ideal = (item['consumo_historico'] / 10) if item['consumo_historico'] > 0 else 50
            if cantidad_ideal < item['stock_min']:
                cantidad_ideal = item['stock_min'] * 1.5
            
            cantidad_a_pedir = int(cantidad_ideal - item['stock']) if (cantidad_ideal - item['stock']) > 0 else 0
            
            if cantidad_a_pedir > 0:
                precio_total = cantidad_a_pedir * item['precio_unitario_promedio']
                pedido_sugerido.append({
                    'id': item['id'],
                    'nombre': item['nombre'],
                    'cantidad_a_pedir': cantidad_a_pedir,
                    'precio_unitario': item['precio_unitario_promedio'],
                    'precio_total': precio_total
                })
    
    if pedido_sugerido:
        print("\nAlerta! Se detectó stock bajo y se sugiere un pedido:")
        print("-" * 80)
        print(f"{'ID':<5}{'Nombre':<20}{'Cantidad a Pedir':<20}{'Precio Unitario':<20}{'Precio Total':<20}")
        print("-" * 80)
        for pedido in pedido_sugerido:
            print(f"{pedido['id']:<5}{pedido['nombre']:<20}{pedido['cantidad_a_pedir']:<20}{f'${pedido['precio_unitario']:.2f}':<20}{f'${pedido['precio_total']:.2f}':<20}")
        print("-" * 80)

        confirmacion = input("\n¿Deseas generar y enviar esta orden al proveedor? (s/n): ")
        if confirmacion.lower() == 's':
            pedido_nuevo = {
                'fecha': time.strftime("%Y-%m-%d %H:%M:%S"),
                'responsable': responsable,
                'items': pedido_sugerido
            }
            guardar_pedido(pedido_nuevo)
            pedidos_proveedor.append(pedido_nuevo)
            print("Orden generada y enviada al proveedor.")
        else:
            print("Pedido cancelado.")
    else:
        print("Todos los materiales están en niveles de stock adecuados. No se requieren pedidos.")
    
    input("\nPresiona Enter para continuar...")

def ver_pedidos_anteriores():
    limpiar_pantalla()
    print("--- Historial de Pedidos a Proveedor ---")
    if pedidos_proveedor:
        for pedido in pedidos_proveedor:
            print("\n" + "=" * 80)
            print(f"Pedido generado el: {pedido['fecha']} por {pedido['responsable']}")
            print("=" * 80)
            print(f"{'ID':<5}{'Nombre':<20}{'Cantidad Pedida':<20}{'Precio Unitario':<20}{'Precio Total':<20}")
            print("-" * 80)
            for item in pedido['items']:
                print(f"{item['id']:<5}{item['nombre']:<20}{item['cantidad_a_pedir']:<20}{f'${item['precio_unitario']:.2f}':<20}{f'${item['precio_total']:.2f}':<20}")
            print("-" * 80)
    else:
        print("No hay pedidos anteriores registrados.")
    input("\nPresiona Enter para continuar...")

def realizar_compra():
    limpiar_pantalla()
    print("--- Realizar una Venta ---")
    item_id = input("Ingresa el ID del material a vender: ")
    
    item_encontrado = next((item for item in inventario if item['id'] == item_id), None)
    
    if item_encontrado:
        try:
            cantidad_venta = int(input(f"Ingresa la cantidad de '{item_encontrado['nombre']}' a vender: "))
            if cantidad_venta > 0 and cantidad_venta <= item_encontrado['stock']:
                item_encontrado['stock'] -= cantidad_venta
                item_encontrado['consumo_historico'] += cantidad_venta
                guardar_inventario(inventario)
                guardar_venta({
                    'fecha': time.strftime("%Y-%m-%d"),
                    'item': item_encontrado['nombre'],
                    'cantidad': cantidad_venta
                })
                print(f"Venta de {cantidad_venta} unidades de '{item_encontrado['nombre']}' completada con éxito.")
            elif cantidad_venta <= 0:
                print("La cantidad debe ser un número positivo.")
            else:
                print(f"Stock insuficiente. Solo quedan {item_encontrado['stock']} unidades de '{item_encontrado['nombre']}'.")
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número.")
    else:
        print(f"No se encontró ningún material con el ID '{item_id}'.")
    
    input("\nPresiona Enter para continuar...")

def analisis_sugerencias():
    limpiar_pantalla()
    print("--- Análisis de Sugerencias Automáticas ---")
    print("Basado en el comportamiento de consumo histórico, aquí hay algunas recomendaciones:")
    print("-" * 60)
    print(f"{'Material':<20}{'Cantidad Vendida':<20}{'Fecha/Mes':<20}")
    print("-" * 60)
    
    if ventas_realizadas:
        for venta in ventas_realizadas:
             print(f"{venta['item']:<20}{venta['cantidad']:<20}{venta['fecha']:<20}")
    else:
        print("No hay datos de ventas recientes para analizar.")
    
    input("\nPresiona Enter para continuar...")

def menu_gestionar_stock():
    while True:
        limpiar_pantalla()
        print("\n--- Menú de Gestión de Stock y Pedidos ---")
        print("1. Ver Inventario")
        print("2. Realizar un Pedido a Proveedor")
        print("3. Ver Pedidos Anteriores")
        print("4. Configurar Umbrales de Reorden")
        print("5. Volver al Menú Principal")

        opcion = input("Selecciona una opción: ")
        if opcion == '1':
            while True:
                limpiar_pantalla()
                print("\n--- Ver Inventario ---")
                print("1. Filtrar por los más vendidos")
                print("2. Filtrar por mayor stock")
                print("3. Filtrar por menor stock")
                print("4. Ver sin filtro")
                print("5. Volver al menú anterior")
                filtro_op = input("Selecciona un filtro: ")
                if filtro_op == '1':
                    mostrar_inventario(filtro='mas_vendidos')
                elif filtro_op == '2':
                    mostrar_inventario(filtro='mayor_stock')
                elif filtro_op == '3':
                    mostrar_inventario(filtro='menor_stock')
                elif filtro_op == '4':
                    mostrar_inventario()
                elif filtro_op == '5':
                    break
                else:
                    print("Opción de filtro no válida.")
                    time.sleep(1.5)
        elif opcion == '2':
            generar_pedido_proveedor()
        elif opcion == '3':
            ver_pedidos_anteriores()
        elif opcion == '4':
            configurar_umbrales()
        elif opcion == '5':
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
            time.sleep(1.5)

def main():
    limpiar_pantalla()
    verificar_stock_bajo()
    
    while True:
        limpiar_pantalla()
        print("\n==============================================")
        print("  Menú Principal del Sistema de Inventario    ")
        print("==============================================")
        print("1. Gestionar Stock y Pedidos")
        print("2. Realizar una Venta")
        print("3. Análisis de Datos y Sugerencias")
        print("4. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            menu_gestionar_stock()
        elif opcion == '2':
            realizar_compra()
        elif opcion == '3':
            analisis_sugerencias()
        elif opcion == '4':
            print("Adiós, gracias por usar el sistema!")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
            time.sleep(1.5)

if __name__ == "__main__":
    main()