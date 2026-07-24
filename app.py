from flask import Flask, render_template, request, redirect, session
from database.conexion import conectar
from datetime import datetime

app = Flask(__name__)
app.secret_key = "NEXTDEX_SECRET_2026"


# ==========================
# LOGIN
# ==========================

@app.route("/")
def login():
    return render_template("login.html")


# ==========================
# DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")



# ==========================
# PASO 1 - CLIENTE
# ==========================

@app.route("/nueva_reparacion", methods=["GET", "POST"])
def nueva_reparacion():

    if request.method == "GET":
        session.pop("cliente_id", None)
        session.pop("cliente_creado", None)

    if request.method == "POST":

        accion = request.form.get("accion")


        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        direccion = request.form["direccion"]
        ine = request.form["ine"]
        notas = request.form["notas"]


        conexion = conectar()
        cursor = conexion.cursor()



        # ==========================
        # BOTÓN CREAR CLIENTE
        # ==========================

        if accion == "crear":

            #evita duplicadps
            if session.get("cliente_creado"):

                return render_template(
                    "reparaciones/cliente.html",
                    paso=1,
                    cliente_id=session.get("cliente_id"),
                    mensaje="Ya existe un cliente creado, por favor presiona siguiente para continuar"
                )


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


            session["cliente_id"] = cliente_id
            session["cliente_creado"] = True


            conexion.commit()
            conexion.close()


            return render_template(
                "reparaciones/cliente.html",
                paso=1,
                cliente_id=cliente_id,
                mensaje="Cliente creado correctamente"
            )



        # ==========================
        # BOTÓN SIGUIENTE
        # ==========================

        elif accion == "siguiente":


            cliente_id = session.get("cliente_id")


            # Ya existe cliente creado
            if cliente_id:

                conexion.close()

                return redirect("/equipo")



            # No existe, entonces lo crea

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


            session["cliente_id"] = cliente_id


            conexion.commit()
            conexion.close()


            return redirect("/equipo")



    return render_template(
        "reparaciones/cliente.html",
        paso=1
    )

# ==========================
# PASO 2 - EQUIPO
# ==========================

@app.route("/equipo", methods=["GET", "POST"])
def equipo():

    cliente_id = session.get("cliente_id")

    # Si no hay cliente creado regresamos al paso 1
    if not cliente_id:
        return redirect("/nueva_reparacion")


    conexion = conectar()
    cursor = conexion.cursor()


    if request.method == "POST":

        marca = request.form.get("marca")
        modelo = request.form.get("modelo")
        color = request.form.get("color")
        capacidad = request.form.get("capacidad")
        imei = request.form.get("imei")
        numero_serie = request.form.get("numero_serie")

        compania = request.form.get("compania")
        bateria = request.form.get("bateria")

        tipo_bloqueo = request.form.get("tipo_bloqueo")
        clave_bloqueo = request.form.get("clave_bloqueo")

        cuenta_google = request.form.get("cuenta_google")
        cuenta_apple = request.form.get("cuenta_apple")

        prueba_enciende = request.form.get("prueba_enciende")
        prueba_carga = request.form.get("prueba_carga")
        prueba_imagen = request.form.get("prueba_imagen")
        prueba_tactil = request.form.get("prueba_tactil")


        cursor.execute("""
            INSERT INTO equipos
            (
                cliente_id,
                marca,
                modelo,
                color,
                capacidad,
                imei,
                numero_serie,
                compania,
                nivel_bateria,
                tipo_bloqueo,
                clave_bloqueo,
                cuenta_google,
                cuenta_apple,
                prueba_enciende,
                prueba_carga,
                prueba_imagen,
                prueba_tactil
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            cliente_id,
            marca,
            modelo,
            color,
            capacidad,
            imei,
            numero_serie,
            compania,
            bateria,
            tipo_bloqueo,
            clave_bloqueo,
            cuenta_google,
            cuenta_apple,
            prueba_enciende,
            prueba_carga,
            prueba_imagen,
            prueba_tactil
        ))


        equipo_id = cursor.lastrowid


        año = datetime.now().year


        cursor.execute("""
            SELECT COUNT(*) FROM reparaciones
        """)

        numero = cursor.fetchone()[0] + 1


        folio = f"NX-{año}-{numero:06d}"


        cursor.execute("""
            INSERT INTO reparaciones
            (
                equipo_id,
                folio,
                estado
            )
            VALUES (?, ?, ?)
        """,
        (
            equipo_id,
            folio,
            "Recibido"
        ))


        reparacion_id = cursor.lastrowid


        conexion.commit()
        conexion.close()


        return redirect(
            f"/diagnostico/{reparacion_id}"
        )


    cursor.execute(
        "SELECT * FROM clientes WHERE id=?",
        (cliente_id,)
    )


    cliente = cursor.fetchone()


    conexion.close()


    return render_template(
        "reparaciones/equipo.html",
        cliente=cliente,
        paso=2
    )


# ==========================
# PASO 3 - DIAGNÓSTICO
# ==========================

@app.route("/diagnostico/<int:reparacion_id>")
def diagnostico(reparacion_id):

    conexion = conectar()
    cursor = conexion.cursor()


    cursor.execute("""
        SELECT 
            clientes.*
        FROM reparaciones

        INNER JOIN equipos
        ON reparaciones.equipo_id = equipos.id

        INNER JOIN clientes
        ON equipos.cliente_id = clientes.id

        WHERE reparaciones.id = ?

    """,
    (reparacion_id,))


    cliente = cursor.fetchone()


    conexion.close()



    return render_template(
        "reparaciones/diagnostico.html",
        reparacion_id=reparacion_id,
        cliente=cliente,
        paso=3
    )



# ==========================
# INICIAR APP
# ==========================

if __name__ == "__main__":
    app.run(debug=True)