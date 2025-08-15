class Inventario:
    def __init__(self):
        self.materiales = []

    def registrar_material(self,codigo, nombre, cantidad, tipo, proveedor, fecha):
        material = {
            "codigo" : codigo,
            "nombre": nombre,
            "cantidad": cantidad,
            "tipo": tipo,
            "proveedor": proveedor,
            "fecha": fecha
        }
        self.materiales.append(material)
        
    def mostrar_materiales(self):
        return self.materiales


# Ejemplo
inventario = Inventario()
inventario.registrar_material("Parche", 100, "Caucho", "Proveedor A", "14/08/2025")
inventario.registrar_material("Neumatico", 10, "Cp661 165/70r13", "Proveedor B", "15/08/2025")

materiales_guardados =inventario.mostrar_materiales()
print("Lista de materiales registrados:")
for material in materiales_guardados:
    print(material)


