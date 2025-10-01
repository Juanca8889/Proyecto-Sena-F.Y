




class Inventario:
    def __init__(self, materiales):
        """
        Recibe una lista de materiales, donde cada material es un diccionario.
        Ejemplo de un material:
        {
            "codigo": "001",
            "nombre": "Tornillo",
            "categoria": "Ferretería",
            "proveedor": "ACME",
            "modelo": "M4"
        }
        """
        self.materiales = materiales

    def buscar(self, **criterios):
        """
        Busca materiales en el inventario según los criterios dados.
        Ejemplo:
            buscar(nombre="tornillo")
            buscar(categoria="herramientas", proveedor="ACME")
        """
        resultados = self.materiales
        for clave, valor in criterios.items():
            resultados = [m for m in resultados if m[clave].lower() == valor.lower()]
        return resultados


# Ejemplo de uso:
if __name__ == "__main__":
    materiales = [
        {"codigo": "001", "nombre": "Tornillo", "categoria": "Ferretería", "proveedor": "ACME", "modelo": "M4"},
        {"codigo": "002", "nombre": "Martillo", "categoria": "Herramientas", "proveedor": "ToolCo", "modelo": "Standard"},
        {"codigo": "003", "nombre": "Taladro", "categoria": "Herramientas", "proveedor": "Bosch", "modelo": "X100"},
    ]

    inv = Inventario(materiales)

    print("🔎 Buscar por nombre:", inv.buscar(nombre="Martillo"))
    print("🔎 Buscar por categoría y proveedor:", inv.buscar(categoria="Herramientas", proveedor="Bosch"))
