import sqlite3
from contextlib import contextmanager
from pathlib import Path

RUTA_DB = Path(__file__).resolve().parent.parent / "data" / "asistente.db"

_ESQUEMA = """
CREATE TABLE IF NOT EXISTS mensajes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rol TEXT NOT NULL,
    contenido TEXT NOT NULL,
    creado_en TEXT NOT NULL DEFAULT (datetime('now'))
)
"""


@contextmanager
def _conexion():
    """Abre una conexión, confirma los cambios y la cierra siempre."""
    RUTA_DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(RUTA_DB)
    try:
        with con:
            yield con
    finally:
        con.close()


def iniciar():
    with _conexion() as con:
        con.execute(_ESQUEMA)


def cargar_historial(limite):
    iniciar()
    with _conexion() as con:
        filas = con.execute(
            "SELECT rol, contenido FROM mensajes ORDER BY id DESC LIMIT ?",
            (limite,),
        ).fetchall()
    return [{"role": rol, "content": contenido} for rol, contenido in reversed(filas)]


def guardar_mensaje(rol, contenido):
    iniciar()
    with _conexion() as con:
        con.execute(
            "INSERT INTO mensajes (rol, contenido) VALUES (?, ?)",
            (rol, contenido),
        )


def guardar_intercambio(mensaje_usuario, respuesta):
    """Guarda pregunta y respuesta en una sola transacción."""
    iniciar()
    with _conexion() as con:
        con.executemany(
            "INSERT INTO mensajes (rol, contenido) VALUES (?, ?)",
            [("user", mensaje_usuario), ("assistant", respuesta)],
        )


def borrar_memoria():
    """Borra todos los mensajes de la base de datos."""
    iniciar()
    with _conexion() as con:
        con.execute("DELETE FROM mensajes")
