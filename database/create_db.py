import sqlite3
import os

os.makedirs("database", exist_ok=True)

conexion = sqlite3.connect("database/database.db")
cursor = conexion.cursor()


# =========================
# CLIENTES
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    correo TEXT,
    direccion TEXT,
    ine TEXT,
    notas TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")


# =========================
# EQUIPOS
# =========================

# Tabla de equipos
cursor.execute("""
CREATE TABLE IF NOT EXISTS equipos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    cliente_id INTEGER NOT NULL,

    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    color TEXT,
    capacidad TEXT,

    imei TEXT,
    numero_serie TEXT,

    compania TEXT,
    nivel_bateria INTEGER,

    tipo_bloqueo TEXT,
    clave_bloqueo TEXT,

    cuenta_google TEXT,
    cuenta_apple TEXT,

    observaciones_estado TEXT,

    foto_frontal TEXT,
    foto_trasera TEXT,
    foto_lateral TEXT,
    foto_dano TEXT,

    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(cliente_id) REFERENCES clientes(id)
)
""")


# =========================
# REPARACIONES
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS reparaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    folio TEXT UNIQUE,

    equipo_id INTEGER NOT NULL,

    observaciones TEXT,

    costo_estimado REAL DEFAULT 0,
    anticipo REAL DEFAULT 0,

    fecha_entrega TEXT,

    tecnico TEXT,

    prioridad TEXT DEFAULT 'Normal',

    estado TEXT DEFAULT 'Recibido',

    fecha_ingreso DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(equipo_id) REFERENCES equipos(id)
)
""")


# =========================
# DIAGNOSTICOS
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS diagnosticos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    reparacion_id INTEGER NOT NULL,

    falla TEXT,

    FOREIGN KEY(reparacion_id) REFERENCES reparaciones(id)
)
""")


# =========================
# ACCESORIOS
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS accesorios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    reparacion_id INTEGER NOT NULL,

    nombre TEXT,

    FOREIGN KEY(reparacion_id) REFERENCES reparaciones(id)
)
""")


# =========================
# IMAGENES
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS imagenes_equipo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    reparacion_id INTEGER NOT NULL,

    ruta_imagen TEXT,

    tipo TEXT,

    FOREIGN KEY(reparacion_id) REFERENCES reparaciones(id)
)
""")


# =========================
# USUARIOS
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre TEXT NOT NULL,

    usuario TEXT UNIQUE,

    password TEXT,

    rol TEXT
)
""")


conexion.commit()
conexion.close()

print("✅ Base de datos creada correctamente.")