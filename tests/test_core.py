import jarvis.core as core
import jarvis.memoria as memoria
from jarvis.core import MAX_MENSAJES, Asistente


def _generar_falso(*textos):
    def generar(mensajes):
        yield from textos

    return generar


def test_carga_el_historial_previo(db_temporal):
    memoria.guardar_intercambio("hola", "buenas")

    asistente = Asistente()

    assert asistente.historial == [
        {"role": "user", "content": "hola"},
        {"role": "assistant", "content": "buenas"},
    ]


def test_responder_hace_streaming_y_persiste(db_temporal, monkeypatch):
    monkeypatch.setattr(core, "generar", _generar_falso("Hola", " mundo"))
    asistente = Asistente()

    trozos = list(asistente.responder("¿qué tal?"))

    assert trozos == ["Hola", " mundo"]
    assert asistente.historial == [
        {"role": "user", "content": "¿qué tal?"},
        {"role": "assistant", "content": "Hola mundo"},
    ]
    assert memoria.cargar_historial(20) == asistente.historial


def test_responder_envia_el_contexto_correcto(db_temporal, monkeypatch):
    capturado = {}

    def generar(mensajes):
        capturado["mensajes"] = mensajes
        yield "ok"

    monkeypatch.setattr(core, "generar", generar)
    memoria.guardar_intercambio("antes", "respuesta anterior")
    asistente = Asistente()

    list(asistente.responder("ahora"))

    assert capturado["mensajes"] == [
        {"role": "system", "content": core.SYSTEM_PROMPT},
        {"role": "user", "content": "antes"},
        {"role": "assistant", "content": "respuesta anterior"},
        {"role": "user", "content": "ahora"},
    ]


def test_respuesta_vacia_no_se_guarda(db_temporal, monkeypatch):
    monkeypatch.setattr(core, "generar", _generar_falso())
    asistente = Asistente()

    assert list(asistente.responder("hola")) == []
    assert asistente.historial == []
    assert memoria.cargar_historial(20) == []


def test_historial_se_recorta_a_max_mensajes(db_temporal, monkeypatch):
    monkeypatch.setattr(core, "generar", _generar_falso("ok"))
    asistente = Asistente()

    for i in range(15):
        list(asistente.responder(f"mensaje {i}"))

    assert len(asistente.historial) == MAX_MENSAJES
    assert asistente.historial[0] == {"role": "user", "content": "mensaje 5"}
    assert asistente.historial[-1] == {"role": "assistant", "content": "ok"}


def test_borrar_memoria_limpia_disco_y_ram(db_temporal, monkeypatch):
    monkeypatch.setattr(core, "generar", _generar_falso("ok"))
    asistente = Asistente()
    list(asistente.responder("hola"))

    asistente.borrar_memoria()

    assert asistente.historial == []
    assert memoria.cargar_historial(20) == []
