from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista simulada de órdenes
ordenes = [
    {
        "modelo": "Modelo A",
        "servicio": "Reparación",
        "fecha_hora": "2025-09-09 10:00",
        "responsable": "Andrés",
        "detalles": "Cambio de batería",
        "garantia": "Sí"
    }
]

@app.route("/", methods=["GET", "POST"])
def ordenes_servicio():
    global ordenes
    if request.method == "POST":
        # Obtener datos del formulario
        nueva_orden = {
            "modelo": request.form.get("modelo"),
            "servicio": request.form.get("servicio"),
            "fecha_hora": request.form.get("fecha_hora"),
            "responsable": request.form.get("responsable"),
            "detalles": request.form.get("detalles"),
            "garantia": request.form.get("garantia")
        }
        ordenes.append(nueva_orden)
        return redirect(url_for("ordenes_servicio"))
    return render_template("ordenes.html", ordenes=ordenes)

if __name__ == "__main__":
    app.run(debug=True)
