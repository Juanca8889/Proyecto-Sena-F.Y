class Inventario:
    def __init__(self):
        self.materiales = []

    def registrar_material(self, nombre, cantidad, tipo, proveedor, fecha):
        material = {
            "nombre": nombre,
            "cantidad": cantidad,
            "tipo": tipo,
            "proveedor": proveedor,
            "fecha": fecha
        }
        self.materiales.append(material)
        print(f"material '{nombre}' registrado con exito.")

    def pedir_material(self):
        while True:
            nombre = input("ingrese el nombre del material: ")
            
            while True:
                try:
                    cantidad = int(input("ingrese la cantidad: "))
                    break
                except ValueError:
                    print("ingrese un numero valido.")
            
            tipo = input("ingrese el tipo de material: ")
            proveedor = input("ingrese el proveedor: ")
            fecha = input("ingrese la fecha de ingreso (DD/MM/AAAA): ")
            
            self.registrar_material(nombre, cantidad, tipo, proveedor, fecha)

            continuar = input("registrar otro material? (s/n): ").lower()
            if continuar != "s":
                break

    def mostrar_materiales(self):
        print("Lista de materiales registrados:")
        for m in self.materiales:
            print(m)


inventario = Inventario()
inventario.pedir_material()
inventario.mostrar_materiales()
