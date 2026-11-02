import sqlite3

from jarvis import memoria


def test_iniciar_crea_la_tabla(db_temporal):
    memoria.iniciar()

    assert db_temporal.exists()
    con = sqlite3.connect(db_temporal)
    try:
        tablas = con.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    finally:
        con.close()
    assert ("mensajes",) in tablas


def test_guardar_mensaje_crea_la_tabla_si_no_existe(db_temporal):
    memoria.guardar_mensaje("user", "hola")

    assert memoria.cargar_historial(20) == [{"role": "user", "content": "hola"}]


def test_guardar_y_cargar_mantiene_el_orden(db_temporal):
    memoria.guardar_mensaje("user", "hola")
    memoria.guardar_mensaje("assistant", "buenas")

    assert memoria.cargar_historial(20) == [
        {"role": "user", "content": "hola"},
        {"role": "assistant", "content": "buenas"},
    ]


def test_cargar_historial_devuelve_los_ultimos(db_temporal):
    for i in range(10):
        memoria.guardar_mensaje("user", f"u{i}")
        memoria.guardar_mensaje("assistant", f"a{i}")

    historial = memoria.cargar_historial(4)

    assert [m["content"] for m in historial] == ["u8", "a8", "u9", "a9"]


def test_guardar_intercambio_guarda_ambos_mensajes(db_temporal):
    memoria.guardar_intercambio("hola", "buenas")

    assert memoria.cargar_historial(20) == [
        {"role": "user", "content": "hola"},
        {"role": "assistant", "content": "buenas"},
    ]


def test_borrar_memoria_vacia_la_tabla(db_temporal):
    memoria.guardar_intercambio("hola", "buenas")

    memoria.borrar_memoria()

    assert memoria.cargar_historial(20) == []


def test_borrar_memoria_sin_tabla_previa(db_temporal):
    memoria.borrar_memoria()

    assert memoria.cargar_historial(20) == []
