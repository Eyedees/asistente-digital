import sqlite3
from pathlib import Path

RUTA_DB = Path(__file__).resolve().parent.parent / "data" / "asistente.db"


def _conectar():
    RUTA_DB.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(RUTA_DB)


def iniciar():
    with _conectar() as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rol TEXT NOT NULL,
                contenido TEXT NOT NULL,
                creado_en TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )


def cargar_historial(limite):
    iniciar()
    with _conectar() as con:
        filas = con.execute(
            "SELECT rol, contenido FROM mensajes ORDER BY id DESC LIMIT ?",
            (limite,),
        ).fetchall()
    return [{"role": rol, "content": contenido} for rol, contenido in reversed(filas)]


def guardar_mensaje(rol, contenido):
    with _conectar() as con:
        con.execute(
            "INSERT INTO mensajes (rol, contenido) VALUES (?, ?)",
            (rol, contenido),
        )

def borrar_memoria():
    """Borra todos los mensajes de la base de datos."""
    iniciar() #con esto hacemos que la función sea segura de llamar incluso si la base de datos no existe todavía
    with _conectar() as con:
        con.execute("DELETE FROM mensajes")
