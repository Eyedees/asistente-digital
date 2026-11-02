import tempfile
import wave
from pathlib import Path

from jarvis.config import (
    WHISPER_COMPUTE_TYPE,
    WHISPER_DEVICE,
    WHISPER_LANGUAGE,
    WHISPER_MODEL,
)

FRECUENCIA = 16000
CANALES = 1
ANCHO_MUESTRA = 2  # 16 bits

_modelo = None


def _cargar_modelo():
    """Carga faster-whisper una sola vez y reutiliza el modelo."""
    global _modelo
    if _modelo is None:
        from faster_whisper import WhisperModel

        _modelo = WhisperModel(
            WHISPER_MODEL,
            device=WHISPER_DEVICE,
            compute_type=WHISPER_COMPUTE_TYPE,
        )
    return _modelo


def _escribir_wav(audio, ruta):
    with wave.open(str(ruta), "wb") as wav:
        wav.setnchannels(CANALES)
        wav.setsampwidth(ANCHO_MUESTRA)
        wav.setframerate(FRECUENCIA)
        wav.writeframes(audio.tobytes())


def grabar_audio():
    """Graba del micrófono hasta que el usuario pulse Enter y devuelve un WAV."""
    import numpy as np
    import sounddevice as sd

    fragmentos = []

    def callback(indata, frames, time, status):
        if status:
            print(f"[audio] {status}")
        fragmentos.append(indata.copy())

    with sd.InputStream(
        samplerate=FRECUENCIA,
        channels=CANALES,
        dtype="int16",
        callback=callback,
    ):
        input("Grabando... pulsa Enter para terminar. ")

    if not fragmentos:
        raise RuntimeError("No se ha grabado audio.")

    audio = np.concatenate(fragmentos, axis=0).flatten()
    if audio.size == 0:
        raise RuntimeError("No se ha grabado audio.")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temporal:
        ruta = Path(temporal.name)
    _escribir_wav(audio, ruta)
    return ruta


def transcribir(ruta):
    """Transcribe un archivo de audio y devuelve el texto completo."""
    segmentos, _ = _cargar_modelo().transcribe(
        str(ruta),
        language=WHISPER_LANGUAGE,
        vad_filter=True,
    )
    return " ".join(segmento.text.strip() for segmento in segmentos).strip()


def grabar_y_transcribir():
    ruta = grabar_audio()
    print("Transcribiendo...")
    try:
        return transcribir(ruta)
    finally:
        ruta.unlink(missing_ok=True)
