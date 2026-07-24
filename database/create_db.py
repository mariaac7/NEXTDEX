import sqlite3
import os

# Crear la carpeta si no existe
os.makedirs("database", exist_ok=True)

# Conectar a la base de datos
conexion = sqlite3.connect("database/database.db")
cursor = conexion.cursor()

# Tabla de clientes
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    correo TEXT,
    direccion TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conexion.commit()
conexion.close()

print("✅ Base de datos creada correctamente.")