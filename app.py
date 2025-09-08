from flask import Flask, render_template

app = Flask(__name__)

# Ruta principal
@app.route("/")
def registrarmat():
    return render_template("registrarmat.html")  # Busca en templates/index.html
@app.route("/ordenes")
def ordenes():
    return render_template("ordenes.html")
@app.route("/filtro")
def filtro():
    return render_template("filtro.html")




if __name__ == "__main__":
    app.run(debug=True)
