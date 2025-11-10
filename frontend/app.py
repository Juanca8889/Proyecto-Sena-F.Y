from flask import Flask, render_template, request, redirect, url_for, flash, session

from datetime import date, datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
app.secret_key = "clave_secreta"
from BD. bda import conectar
from backend.devolucion_material import Devolucion

# -----------------------------
# DEVOLUCION DE MATERIAL
# -----------------------------

@app.route("/devolucion_de_material", methods=["GET", "POST"])
def devoluciones():
    if request.method == "POST":
        compra_id = request.form.get("compra_id")
        razon = request.form.get("razon")
        fecha = "2024/09/12"
        estado = 1  

        try:
            # Crear instancia de la clase Devolucion
            nueva_devolucion = Devolucion(
                compra_id=compra_id,
                razon=razon,
                estado=estado,
                fecha=fecha
            )

            # Llamar al método que guarda la devolución en BD
            nueva_devolucion.registrar_devolucion()

            flash("✅ Devolución registrada correctamente.", "success")
            return redirect(url_for("devoluciones"))

        except Exception as e:
            print(f"Error al registrar devolución: {e}")
            flash(f"❌ Error al registrar devolución: {e}", "danger")

    return render_template("devolucionmaterial.html")


# -----------------------------
# EDITAR MATERIALES
# -----------------------------
@app.route('/editar_material/<int:id_producto>', methods=['GET', 'POST'])
def editar_material(id_producto):
    
    material = material()

    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        cantidad = request.form["cantidad"]
        categoria_id = request.form["categoria_id"]
        precio = request.form["precio"]

        actualizado = material.actualizar_producto(
            id_producto=id_producto,
            nombre=nombre,
            descripcion=descripcion,
            cantidad=cantidad,
            categoria_id=categoria_id,
            precio=precio
        )

        if actualizado:
            flash("Material actualizado correctamente.", "success")
        else:
            flash("Error al actualizar el material.", "danger")

        return redirect(url_for("material.listar_materiales"))


    producto = material.obtener_producto_por_id(id_producto)
    categorias = material.consultar_todas_las_categorias()

    return render_template(
        "editar_material.html",
        producto=producto,
        categorias=categorias
    )


# -----------------------------
# REGISTRAR ADMINISTRAR PROVEEDORES
# -----------------------------

@app.route("/registrar_administrar_proveedores")
def registrar_proveedor():
    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        direccion = request.form["direccion"]
        tipo = request.form["tipo"]
        nit = request.form["nit"]

        gestor_proveedores.registrar_proveedor(
            nombre, telefono, correo, direccion, tipo, nit
        )

        flash("Proveedor registrado correctamente", "success")
        return redirect(url_for("vista_proveedores"))

    return render_template("proveedor_form.html", accion="nuevo")


@app.route("/proveedores/<int:id_proveedor>")
def ver_proveedor(id_proveedor):
    proveedor = gestor_proveedores.obtener_proveedor_por_id(id_proveedor)
    return render_template("proveedor_detalle.html", proveedor=proveedor)


@app.route("/proveedores/editar/<int:id_proveedor>", methods=["GET", "POST"])
def actualizar_proveedor(id_proveedor):
    proveedor = gestor_proveedores.obtener_proveedor_por_id(id_proveedor)

    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        direccion = request.form["direccion"]
        tipo = request.form["tipo"]
        nit = request.form["nit"]

        gestor_proveedores.actualizar_proveedor(
            id_proveedor, nombre, telefono, correo, direccion, tipo, nit
        )

        flash("Proveedor actualizado correctamente", "success")
        return redirect(url_for("vista_proveedores"))

    return render_template("proveedor_form.html", accion="editar", proveedor=proveedor)


@app.route("/proveedores/eliminar/<int:id_proveedor>", methods=["POST"])
def eliminar_proveedor(id_proveedor):
    gestor_proveedores.eliminar_proveedor(id_proveedor)
    flash("Proveedor eliminado correctamente", "success")
    return redirect(url_for("vista_proveedores"))

if __name__ == "__main__":
    app.run(debug=True)

# -----------------------------
# REGISTRAR DEVOLUCION DE MATERIAL
# ----------------------------
@app.route("/registrar_devolucion_material")
def devoluciones():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

   
    if request.method == "POST":
        compra_id = request.form.get("compra_id")
        fecha = request.form.get("fecha")
        estado = request.form.get("estado")
        razon = request.form.get("razon")

        # Validaciones básicas
        if not compra_id or not fecha or not razon:
            flash("Todos los campos son obligatorios.", "error")
        else:
            try:
                # Llamar al procedimiento almacenado para insertar
                cursor.callproc("InsertarDevolucion", (compra_id, fecha, estado, razon))
                conexion.commit()
                flash("Devolución registrada correctamente.", "success")
            except Exception as e:
                flash(f"Error al registrar la devolución: {str(e)}", "error")

        cursor.close()
        conexion.close()
        return redirect(url_for("devoluciones.devoluciones"))

   
    devoluciones = []
    try:
        cursor.callproc("ConsultarDevoluciones")
        for resultado in cursor.stored_results():
            devoluciones = resultado.fetchall()
    except Exception as e:
        flash(f"Error al consultar devoluciones: {str(e)}", "error")

    # Obtener listas auxiliares para el formulario
    cursor.execute("SELECT id_compra, fecha_compra FROM Compra")
    compras = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "devoluciones.html",
        devoluciones=devoluciones,
        compras=compras
    )
     

