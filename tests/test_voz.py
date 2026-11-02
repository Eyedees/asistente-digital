import sys
import types
import wave
from types import SimpleNamespace

import numpy as np
import pytest

from jarvis import voz


class _StreamFalso:
    def __init__(self, *, samplerate, channels, dtype, callback):
        self.callback = callback

    def __enter__(self):
        self.callback(np.array([[1]], dtype=np.int16), 1, None, "overflow")
        self.callback(np.array([[2]], dtype=np.int16), 1, None, None)
        return self

    def __exit__(self, *args):
        return False


class _StreamSinFragmentos(_StreamFalso):
    def __enter__(self):
        return self


class _StreamVacio(_StreamFalso):
    def __enter__(self):
        self.callback(np.empty((0, 1), dtype=np.int16), 0, None, None)
        return self


class _ModeloFalso:
    def transcribe(self, ruta, **kwargs):
        assert ruta == "audio.wav"
        assert kwargs["language"] == voz.WHISPER_LANGUAGE
        assert kwargs["vad_filter"] is True
        return iter(
            [SimpleNamespace(text=" hola "), SimpleNamespace(text="mundo")]
        ), None


def _instalar_sounddevice(monkeypatch, stream):
    monkeypatch.setitem(
        sys.modules,
        "sounddevice",
        types.SimpleNamespace(InputStream=stream),
    )
    monkeypatch.setattr("builtins.input", lambda _="": "")


def test_grabar_audio_escribe_un_wav(monkeypatch):
    _instalar_sounddevice(monkeypatch, _StreamFalso)

    ruta = voz.grabar_audio()
    try:
        with wave.open(str(ruta), "rb") as wav:
            assert wav.getnchannels() == 1
            assert wav.getsampwidth() == 2
            assert wav.getframerate() == 16000
            assert wav.readframes(2) == np.array(
                [1, 2], dtype=np.int16
            ).tobytes()
    finally:
        ruta.unlink(missing_ok=True)


@pytest.mark.parametrize("stream", [_StreamSinFragmentos, _StreamVacio])
def test_grabar_audio_sin_audio_falla(monkeypatch, stream):
    _instalar_sounddevice(monkeypatch, stream)

    with pytest.raises(RuntimeError, match="No se ha grabado audio"):
        voz.grabar_audio()


def test_transcribir_une_los_segmentos(monkeypatch):
    monkeypatch.setattr(voz, "_cargar_modelo", lambda: _ModeloFalso())

    assert voz.transcribir("audio.wav") == "hola mundo"


def test_cargar_modelo_lo_reutiliza(monkeypatch):
    creados = []

    class _WhisperFalso:
        def __init__(self, *args, **kwargs):
            creados.append((args, kwargs))

    monkeypatch.setitem(
        sys.modules,
        "faster_whisper",
        types.SimpleNamespace(WhisperModel=_WhisperFalso),
    )
    monkeypatch.setattr(voz, "_modelo", None)

    primero = voz._cargar_modelo()
    segundo = voz._cargar_modelo()

    assert primero is segundo
    assert len(creados) == 1
    assert creados[0][0] == (voz.WHISPER_MODEL,)
    assert creados[0][1] == {
        "device": voz.WHISPER_DEVICE,
        "compute_type": voz.WHISPER_COMPUTE_TYPE,
    }


def test_grabar_y_transcribir_elimina_el_wav(monkeypatch, tmp_path):
    ruta = tmp_path / "audio.wav"
    ruta.write_bytes(b"x")
    monkeypatch.setattr(voz, "grabar_audio", lambda: ruta)
    monkeypatch.setattr(voz, "transcribir", lambda _: "hola")

    assert voz.grabar_y_transcribir() == "hola"
    assert not ruta.exists()
