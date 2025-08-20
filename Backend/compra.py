from datetime import datetime

inventario = {}
historial_compras = []

def print_header(text):
    print("\n" + "="*50)
    print(text)
    print("="*50)


class Material:
    def __init__(self, id_material, nombre, referencia, precio):
        self.id_material = id_material
        self.nombre = nombre
        self.referencia = referencia
        self.precio = precio


class Compra(Material):
    def __init__(self, id_material, nombre, referencia, precio, cantidad, proveedor):
        super().__init__(id_material, nombre, referencia, precio)
        self.cantidad = cantidad
        self.proveedor = proveedor
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        
        if id_material in inventario:
            inventario[id_material]['cantidad'] += cantidad
        else:
            inventario[id_material] = {
                'nombre': nombre,
                'referencia': referencia,
                'cantidad': cantidad,
                'precio': precio,
                'proveedor': proveedor
            }

        
        historial_compras.append({
            'id_material': id_material,
            'nombre': nombre,
            'cantidad': cantidad,
            'proveedor': proveedor,
            'fecha': self.fecha
        })

        print_header("COMPRA REALIZADA")
        print(f"{cantidad} unidades de {nombre} pedidas a {proveedor}")
        print(f"Referencia: {referencia} | Precio unitario: ${precio}")
        print(f"Fecha de pedido: {self.fecha}")
        self.revisar_stock()

    def vender(self, cantidad):
        print_header(f"VENTA DE {self.nombre}")
        if self.id_material in inventario:
            if inventario[self.id_material]['cantidad'] >= cantidad:
                inventario[self.id_material]['cantidad'] -= cantidad
                print(f"Se vendieron {cantidad} unidades de {self.nombre}")
            else:
                print(f"No hay suficiente stock para vender {cantidad} de {self.nombre}")
        else:
            print("Producto no encontrado en inventario")
        self.revisar_stock()

    def revisar_stock(self):
        total = inventario[self.id_material]['cantidad']
        if total == 0:
            print(f"ALERTA: El stock de {self.nombre} se ha agotado! Pedir más.")
        elif total < 10:
            print(f"ATENCIÓN: El stock de {self.nombre} está muy bajo ({total} unidades)")
        elif total < 50:
            print(f"Advertencia: El stock de {self.nombre} está al 20-50% ({total} unidades)")
        else:
            print(f"Stock de {self.nombre} suficiente ({total} unidades)")


id_contador = 1


continuar = True
while continuar:
    
    print_header("AGREGAR COMPRA")
    nombre = input("Ingrese el nombre del producto: ")
    referencia = input("Ingrese la referencia del producto: ")
    precio = float(input("Ingrese el precio unitario: "))
    cantidad = int(input("Ingrese la cantidad a comprar: "))
    proveedor = input("Ingrese el proveedor: ")

    compra = Compra(id_contador, nombre, referencia, precio, cantidad, proveedor)
    id_contador += 1

    vender_op = input(f"¿Desea vender alguna unidad de {nombre}? (s/n): ").lower()
    if vender_op == 's':
        cantidad_venta = int(input(f"Ingrese la cantidad de {nombre} a vender: "))
        compra.vender(cantidad_venta)

    otra = input("¿Desea agregar otra compra? (s/n): ").lower()
    if otra != 's':
        continuar = False

print_header("INVENTARIO FINAL")
for id_mat, info in inventario.items():
    print(f"{info['nombre']} | Cantidad: {info['cantidad']} | Proveedor: {info['proveedor']}")

print_header("HISTORIAL DE COMPRAS")
for compra_hist in historial_compras:
    print(f"{compra_hist['nombre']} | Cantidad: {compra_hist['cantidad']} | Proveedor: {compra_hist['proveedor']} | Fecha: {compra_hist['fecha']}")
