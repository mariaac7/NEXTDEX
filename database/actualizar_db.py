import sqlite3

conexion = sqlite3.connect("database/database.db")
cursor = conexion.cursor()


campos = [

"ALTER TABLE equipos ADD COLUMN cuenta_google TEXT",

"ALTER TABLE equipos ADD COLUMN cuenta_apple TEXT",

"ALTER TABLE equipos ADD COLUMN estado_fisico TEXT",

"ALTER TABLE equipos ADD COLUMN prueba_enciende TEXT",

"ALTER TABLE equipos ADD COLUMN prueba_carga TEXT",

"ALTER TABLE equipos ADD COLUMN prueba_imagen TEXT",

"ALTER TABLE equipos ADD COLUMN prueba_tactil TEXT"

"ALTER TABLE equipos ADD COLUMN foto_frontal TEXT"

"ALTER TABLE equipos ADD COLUMN foto_trasera TEXT"

"ALTER TABLE equipos ADD COLUMN foto_dano TEXT"

]


for campo in campos:

    try:
        cursor.execute(campo)
        print("Agregado:", campo)

    except Exception as e:
        print("Ya existe o error:", e)


conexion.commit()
conexion.close()


print("Actualización terminada")