from flask import Flask, render_template, request, redirect, url_for, flash, session
from BD.BDa import conectar
from datetime import date, datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
app.secret_key = "clave_secreta"


# -----------------------------
# 1️⃣ REFERENCIAS
# -----------------------------
@app.route("/creacion_referencias")
def crear_referencia():
    
    producto_id = request.form["producto_id"]
    cantidad = int(request.form["cantidad"])
    categoria_id = request.form["categoria_id"]
    rol_id = request.form["rol_id"]

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO Referencia (producto_id, cantidad, categoria_id, rol_id) VALUES (%s, %s, %s, %s)",
        (producto_id, cantidad, categoria_id, rol_id)
    )
    conexion.commit()
    conexion.close()

    flash(f"Se ha registrado la referencia del producto #{producto_id} con {cantidad} unidades correctamente.")
    return redirect(url_for("referencias"))


if __name__ == "__main__":
    app.run(debug=True)

# -----------------------------
# 2️⃣ REPORTE DE VENTAS
# -----------------------------
@app.route("/reporte_ventas")
def reporte_ventas():

    id_venta = request.form["id_venta"]
    fecha = request.form["fecha"]
    total = request.form["total"]
    vendedor = request.form["vendedor"]

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reporte_ventas (id_venta, fecha, total, vendedor) VALUES (%s, %s, %s, %s)",
        (id_venta, fecha, total, vendedor)
    )
    conn.commit()
    conn.close()

    flash(f"Se ha registrado el reporte de venta #{id_venta} con un total de ${total}.")
    return redirect(url_for("ventas"))


if __name__ == "__main__":
    app.run(debug=True)

# -----------------------------
# 3️⃣ DETALLE DE COMPRA
# -----------------------------
@app.route("/detalle_compra")
def crear_detalle_compra():

    id_compra = request.form["id_compra"]
    id_producto = request.form["id_producto"]
    cantidad = request.form["cantidad"]
    precio_unitario = request.form["precio_unitario"]

    conexion = conectar()
    cursor = conexion.cursor()

    # Insertar el detalle de compra en la tabla
    cursor.execute("""
        INSERT INTO DetalleCompra (id_compra, id_producto, cantidad, precio_unitario)
        VALUES (%s, %s, %s, %s)
    """, (id_compra, id_producto, cantidad, precio_unitario))

    conexion.commit()
    cursor.close()
    conexion.close()

    flash(f"Se ha agregado el producto (ID {id_producto}) a la compra #{id_compra} correctamente.")
    return redirect(url_for("compras"))  # Redirige al listado de compras (ajusta si tu vista se llama distinto)

if __name__ == "__main__":
    app.run(debug=True)



# -----------------------------
# 4️⃣ DEVOLUCIONES
# -----------------------------
@app.route("/devolucion_material")
def devolucion_material():

    id_material = request.form["id_material"]
    cantidad_devuelta = request.form["cantidad_devuelta"]
    motivo = request.form["motivo"]
    fecha = request.form["fecha"]

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO devolucion_material (id_material, cantidad_devuelta, motivo, fecha) VALUES (%s, %s, %s, %s)",
        (id_material, cantidad_devuelta, motivo, fecha)
    )
    conn.commit()
    conn.close()

    flash(f"Se ha registrado la devolución de {cantidad_devuelta} unidades del material #{id_material}.")
    return redirect(url_for("materiales"))


if __name__ == "__main__":
    app.run(debug=True)

# -----------------------------
# 5️⃣ GARANTÍAS
# -----------------------------
@app.route("/registrar_garantias")
def registrar_garantia():
    id_cliente = request.form["id_cliente"]
    id_producto = request.form["id_producto"]
    motivo = request.form["motivo"]
    fecha = request.form["fecha"]

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO garantias (id_cliente, id_producto, motivo, fecha) VALUES (%s, %s, %s, %s)",
        (id_cliente, id_producto, motivo, fecha)
    )
    conn.commit()
    conn.close()

    flash(f"Se ha registrado una garantía para el producto #{id_producto} del cliente #{id_cliente}.")
    return redirect(url_for("garantias"))


if __name__ == "__main__":
    app.run(debug=True)


# -----------------------------
# 6 EDITAR MATERIALES 
# -----------------------------
@app.route("/editar_materiales")
def editar_material(id_material):

    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    cantidad = request.form["cantidad"]
    categoria_id = request.form["categoria_id"]
    proveedor_id = request.form["proveedor_id"]

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE Material
        SET nombre = %s, descripcion = %s, cantidad = %s, categoria_id = %s, proveedor_id = %s
        WHERE id_material = %s
    """, (nombre, descripcion, cantidad, categoria_id, proveedor_id, id_material))
    conexion.commit()
    conexion.close()

    flash(f"Se ha actualizado correctamente el material '{nombre}'.")
    return redirect(url_for("materiales"))


if __name__ == "__main__":
    app.run(debug=True)

# -----------------------------
# 7 INVENTARIO DE HERRAMIENTA
# -----------------------------
@app.route("/inventario_herramienta")
def inventario_herramienta():

    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    cantidad = request.form["cantidad"]
    proveedor_id = request.form["proveedor_id"]
    fecha_ingreso = request.form["fecha_ingreso"]

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO inventario_herramienta (nombre, descripcion, cantidad, proveedor_id, fecha_ingreso)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (nombre, descripcion, cantidad, proveedor_id, fecha_ingreso)
    )
    conn.commit()
    conn.close()

    flash(f"Se ha registrado la herramienta '{nombre}' con {cantidad} unidades en el inventario.")
    return redirect(url_for("inventario_herramienta"))

if __name__ == "__main__":
    app.run(debug=True)


# -----------------------------------
# 8 REGISTRAR ADMINISTRAR PROVEEDORES
# -----------------------------------
@app.route("/registrar_administrar_proveedores")
def registrar_administrar_proveedores():

    nombre = request.form["nombre"]
    telefono = request.form["telefono"]
    correo = request.form["correo"]

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Proveedor (nombre, telefono, correo)
        VALUES (%s, %s, %s)
        """,
        (nombre, telefono, correo)
    )
    conn.commit()
    conn.close()

    flash(f"El proveedor '{nombre}' ha sido registrado correctamente.")
    return redirect(url_for("proveedores"))

if __name__ == "__main__":
    app.run(debug=True)

# -----------------------------------
# 9 REGISTRAR DEVOLUCION DE MATERIAL
# -----------------------------------
@app.route("/registrar_devolucion_de_material")
def registrar_devolucion_material():

    material_id = request.form["material_id"]
    cantidad = request.form["cantidad"]
    motivo = request.form["motivo"]
    fecha_devolucion = request.form["fecha_devolucion"]
    usuario_id = request.form["usuario_id"]

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO DevolucionMaterial (material_id, cantidad, motivo, fecha_devolucion, usuario_id)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (material_id, cantidad, motivo, fecha_devolucion, usuario_id)
    )
    conn.commit()
    conn.close()

    flash(f"Se ha registrado la devolución de {cantidad} unidades del material con ID {material_id}.")
    return redirect(url_for("devoluciones"))

if __name__ == "__main__":
    app.run(debug=True)

# -----------------------------------
# 10 SALIDA DE INVENTARIO
# -----------------------------------
@app.route("/salida_de_inventario")
def salida_inventario():
    producto_id = request.form["producto_id"]
    cantidad_salida = int(request.form["cantidad_salida"])
    fecha_salida = request.form["fecha_salida"]
    usuario_id = request.form["usuario_id"]
    motivo = request.form["motivo"]

    conn = conectar()
    cursor = conn.cursor()

    # 1️⃣ Insertar registro de salida
    cursor.execute(
        """
        INSERT INTO SalidaInventario (producto_id, cantidad_salida, fecha_salida, usuario_id, motivo)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (producto_id, cantidad_salida, fecha_salida, usuario_id, motivo)
    )

    # 2️⃣ Actualizar la cantidad en la tabla Producto
    cursor.execute(
        """
        UPDATE Producto
        SET cantidad = cantidad - %s
        WHERE id_producto = %s
        """,
        (cantidad_salida, producto_id)
    )

    conn.commit()
    conn.close()

    flash(f"Se ha registrado la salida de {cantidad_salida} unidades del producto con ID {producto_id}.")
    return redirect(url_for("inventario"))

if __name__ == "__main__":
    app.run(debug=True)