import sqlite3


def conectar():
    conexion = sqlite3.connect("database/database.db")
    conexion.row_factory = sqlite3.Row
    return conexion