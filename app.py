from flask import Flask, render_template, request, redirect
from database.conexion import conectar

app = Flask(__name__)


@app.route('/')
def login():
    return render_template('login.html')


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/nueva_reparacion", methods=["GET", "POST"])
def nueva_reparacion():

    if request.method == "POST":

        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        direccion = request.form["direccion"]
        ine = request.form["ine"]
        notas = request.form["notas"]

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
        INSERT INTO clientes
        (nombre, telefono, correo, direccion, ine, notas)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            nombre,
            telefono,
            correo,
            direccion,
            ine,
            notas
        ))

        cliente_id = cursor.lastrowid

        conexion.commit()
        conexion.close()

        return redirect(f"/equipo/{cliente_id}")


    return render_template("nueva_reparacion_cliente.html")



@app.route("/equipo/<int:cliente_id>")
def equipo(cliente_id):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM clientes WHERE id=?",
        (cliente_id,)
    )

    cliente = cursor.fetchone()

    conexion.close()

    return render_template(
        "nueva_reparacion_equipo.html",
        cliente=cliente
    )



if __name__ == "__main__":
    app.run(debug=True)