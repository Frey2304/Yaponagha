from flask import Flask, render_template, request, redirect, session
from caballos import caballos, Caballo

import json
import os

app = Flask(__name__)

app.secret_key = "yaponagha"


# CARGAR JSON
with open("caballos.json", "r") as archivo:

    datos = json.load(archivo)

    for d in datos:

        caballo = Caballo(
            d["nombre"],
            d["imagen"],
            d["descripcion"]
        )

        caballos.append(caballo)


# GUARDAR JSON
def guardar_json():

    datos = []

    for c in caballos:

        datos.append({
            "nombre": c.nombre,
            "imagen": c.imagen,
            "descripcion": c.descripcion
        })

    with open("caballos.json", "w") as archivo:

        json.dump(
            datos,
            archivo,
            indent=4
        )


# VER SI ADMIN ESTA LOGUEADO
def admin_logueado():

    return session.get("admin") == True


# HOME
@app.route("/")
def inicio():

    return render_template(
        "index.html",
        caballos=caballos,
        admin=admin_logueado()
    )


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        password = request.form["password"]

        if password == "admin123":

            session["admin"] = True

            return redirect("/")

        return "Contraseña incorrecta"

    return render_template("login.html")


# LOGOUT
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# DETALLE
@app.route("/caballo/<nombre>")
def detalle(nombre):

    caballo_encontrado = None

    for c in caballos:

        if c.nombre == nombre:

            caballo_encontrado = c

            break

    return render_template(
        "detalle.html",
        caballo=caballo_encontrado
    )


# PUBLICAR
@app.route("/publicar", methods=["GET", "POST"])
def publicar():

    if not admin_logueado():

        return redirect("/login")

    if request.method == "POST":

        nombre = request.form["nombre"]

        descripcion = request.form["descripcion"]

        archivo_imagen = request.files["imagen"]

        carpeta_uploads = os.path.join(
            "static",
            "uploads"
        )

        os.makedirs(
            carpeta_uploads,
            exist_ok=True
        )

        nombre_archivo = archivo_imagen.filename.replace(
            " ",
            "_"
        )

        ruta = os.path.join(
            carpeta_uploads,
            nombre_archivo
        )

        archivo_imagen.save(ruta)

        imagen = "/" + ruta.replace("\\", "/")

        nuevo = Caballo(
            nombre,
            imagen,
            descripcion
        )

        caballos.append(nuevo)

        guardar_json()

        return redirect("/")

    return render_template("publicar.html")


# EDITAR
@app.route("/editar/<nombre>", methods=["GET", "POST"])
def editar(nombre):

    if not admin_logueado():

        return redirect("/login")

    caballo_encontrado = None

    for c in caballos:

        if c.nombre == nombre:

            caballo_encontrado = c

            break

    if request.method == "POST":

        caballo_encontrado.nombre = request.form["nombre"]

        caballo_encontrado.descripcion = request.form["descripcion"]

        archivo_imagen = request.files["imagen"]

        if archivo_imagen.filename != "":

            carpeta_uploads = os.path.join(
                "static",
                "uploads"
            )

            os.makedirs(
                carpeta_uploads,
                exist_ok=True
            )

            nombre_archivo = archivo_imagen.filename.replace(
                " ",
                "_"
            )

            ruta = os.path.join(
                carpeta_uploads,
                nombre_archivo
            )

            archivo_imagen.save(ruta)

            caballo_encontrado.imagen = "/" + ruta.replace("\\", "/")

        guardar_json()

        return redirect("/")

    return render_template(
        "editar.html",
        caballo=caballo_encontrado
    )


# BORRAR
@app.route("/borrar/<nombre>")
def borrar(nombre):

    if not admin_logueado():

        return redirect("/login")

    caballos[:] = [
        c for c in caballos
        if c.nombre != nombre
    ]

    guardar_json()

    return redirect("/")


if __name__ == "__main__":

    print("ARRANCANDO APP...")

    app.run(debug=True)