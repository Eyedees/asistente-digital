import builtins

import jarvis.core as core
import jarvis.memoria as memoria
from jarvis.interfaces import cli


def _ejecutar_cli(monkeypatch, entradas, voz_inicial=False):
    it = iter(entradas)
    monkeypatch.setattr(builtins, "input", lambda _="": next(it))
    cli.main(voz_inicial=voz_inicial)


def _generar_falso(*textos):
    def generar(mensajes):
        yield from textos

    return generar


def test_salir_termina(monkeypatch, db_temporal, capsys):
    _ejecutar_cli(monkeypatch, ["salir"])

    assert "Gero Arte!" in capsys.readouterr().out


def test_exit_termina(monkeypatch, db_temporal, capsys):
    _ejecutar_cli(monkeypatch, ["exit"])

    assert "Gero Arte!" in capsys.readouterr().out


def test_entrada_vacia_se_ignora(monkeypatch, db_temporal):
    _ejecutar_cli(monkeypatch, ["", "salir"])

    assert memoria.cargar_historial(20) == []


def test_mensaje_normal_se_responde_y_guarda(monkeypatch, db_temporal, capsys):
    monkeypatch.setattr(core, "generar", _generar_falso("respuesta"))
    _ejecutar_cli(monkeypatch, ["hola", "salir"])

    assert "respuesta" in capsys.readouterr().out
    assert memoria.cargar_historial(20) == [
        {"role": "user", "content": "hola"},
        {"role": "assistant", "content": "respuesta"},
    ]


def test_borrar_memoria_confirmado(monkeypatch, db_temporal, capsys):
    monkeypatch.setattr(core, "generar", _generar_falso("respuesta"))
    _ejecutar_cli(monkeypatch, ["hola", "borrar memoria", "s", "salir"])

    salida = capsys.readouterr().out
    assert "Memoria borrada" in salida
    assert memoria.cargar_historial(20) == []


def test_borrar_memoria_cancelado(monkeypatch, db_temporal, capsys):
    monkeypatch.setattr(core, "generar", _generar_falso("respuesta"))
    _ejecutar_cli(monkeypatch, ["hola", "borrar memoria", "n", "salir"])

    salida = capsys.readouterr().out
    assert "Memoria no borrada" in salida
    assert len(memoria.cargar_historial(20)) == 2


def test_keyboard_interrupt_termina(monkeypatch, db_temporal, capsys):
    def lanzar(_=""):
        raise KeyboardInterrupt

    monkeypatch.setattr(builtins, "input", lanzar)

    cli.main()

    assert "Gero Arte!" in capsys.readouterr().out


def test_error_del_modelo_se_muestra(monkeypatch, db_temporal, capsys):
    def generar(mensajes):
        raise RuntimeError("fallo simulado")
        yield  # pragma: no cover

    monkeypatch.setattr(core, "generar", generar)
    _ejecutar_cli(monkeypatch, ["hola", "salir"])

    assert "[Error: fallo simulado]" in capsys.readouterr().out


def test_comando_voz_transcribe_y_responde(monkeypatch, db_temporal, capsys):
    monkeypatch.setattr(core, "generar", _generar_falso("respuesta"))
    monkeypatch.setattr(
        cli, "grabar_y_transcribir", lambda: "hola por voz"
    )

    _ejecutar_cli(monkeypatch, ["voz", "salir"])

    salida = capsys.readouterr().out
    assert "Tú (voz): hola por voz" in salida
    assert memoria.cargar_historial(20) == [
        {"role": "user", "content": "hola por voz"},
        {"role": "assistant", "content": "respuesta"},
    ]


def test_modo_voz_inicial(monkeypatch, db_temporal, capsys):
    monkeypatch.setattr(core, "generar", _generar_falso("respuesta"))
    monkeypatch.setattr(
        cli, "grabar_y_transcribir", lambda: "hola por voz"
    )

    _ejecutar_cli(monkeypatch, ["", "salir"], voz_inicial=True)

    assert "Modo voz" in capsys.readouterr().out
    assert len(memoria.cargar_historial(20)) == 2


def test_modo_voz_permite_escribir(monkeypatch, db_temporal):
    monkeypatch.setattr(core, "generar", _generar_falso("respuesta"))

    _ejecutar_cli(
        monkeypatch,
        ["hola escrita", "salir"],
        voz_inicial=True,
    )

    assert memoria.cargar_historial(20)[0] == {
        "role": "user",
        "content": "hola escrita",
    }


def test_voz_vacia_avisa(monkeypatch, db_temporal, capsys):
    monkeypatch.setattr(cli, "grabar_y_transcribir", lambda: "")

    _ejecutar_cli(monkeypatch, ["voz", "salir"])

    assert "No se ha detectado voz" in capsys.readouterr().out
    assert memoria.cargar_historial(20) == []


def test_error_de_voz_se_muestra(monkeypatch, db_temporal, capsys):
    def fallar():
        raise RuntimeError("sin micrófono")

    monkeypatch.setattr(cli, "grabar_y_transcribir", fallar)

    _ejecutar_cli(monkeypatch, ["voz", "salir"])

    assert "[Error de voz: sin micrófono]" in capsys.readouterr().out
    assert memoria.cargar_historial(20) == []


def test_voz_puede_decir_salir(monkeypatch, db_temporal):
    monkeypatch.setattr(cli, "grabar_y_transcribir", lambda: "salir")

    _ejecutar_cli(monkeypatch, ["voz"])

    assert memoria.cargar_historial(20) == []
