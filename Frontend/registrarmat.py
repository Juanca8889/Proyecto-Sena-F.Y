from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulación de base de datos en memoria
historial = []


@app.route("/")
def registrar():
    """
    Página principal: muestra el formulario y el historial.
    """
    return render_template("registrarmat2.html", historial=historial)


@app.route("/agregar", methods=["POST"])
def agregar():
    """
    Procesa el formulario para agregar un nuevo material.
    """
    nombre = request.form.get("nombre")
    codigo = request.form.get("codigo")
    tipo = request.form.get("tipo")
    fecha = request.form.get("fecha")
    descripcion = request.form.get("descripcion")
    cantidad = request.form.get("cantidad")
    precio = request.form.get("precio")

    # Agregamos al historial (lista en memoria)
    historial.append({
        "nombre": nombre,
        "cantidad": cantidad,
        "codigo": codigo,
        "tipo": tipo,
        "precio": precio,
        "fecha": fecha,
        "descripcion": descripcion
    })

    # Volvemos a la página principal para ver el registro
    return redirect(url_for("registrar"))


@app.errorhandler(404)
def pagina_no_encontrada(error):
    """
    Manejo de errores: ruta no encontrada.
    """
    return "Página no encontrada. Verifica la URL.", 404


if __name__ == "__main__":
    app.run(debug=True)
